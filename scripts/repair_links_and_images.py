#!/usr/bin/env python3
"""Audit and repair broken local links/images in the static Tennis Unified site.

Safe repairs only:
- missing local targets repaired when an unambiguous filesystem target exists
- .html <-> directory/index.html canonicalization
- case-only path mismatches
- missing images repaired by unique filename/stem match
- internal same-site absolute URLs are treated as local

External URLs are checked and reported, but never rewritten automatically.
"""
from __future__ import annotations

from html import unescape
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, unquote
import difflib
import re
import sys
import requests

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "SITE_LINK_IMAGE_AUDIT.md"
SITE_HOSTS = {"tennis-unified.github.io", "www.tennis-unified.github.io"}
ATTR_RE = re.compile(r"(?P<attr>href|src)\s*=\s*(?P<q>[\"'])(?P<url>.*?)(?P=q)", re.I)

html_files = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]
all_files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
file_set = {p.relative_to(ROOT).as_posix() for p in all_files}
file_lower = {}
for rel in file_set:
    file_lower.setdefault(rel.lower(), []).append(rel)

fixes = []
unresolved_local = []
external_404 = []
external_redirects = []
checked_external = set()


def source_url_path(src: Path) -> str:
    rel = src.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-10] + "/"
    return "/" + rel


def canonical_candidate(path: str):
    """Return a unique existing repo-relative path for a URL path, if possible."""
    path = unquote(path.split("#", 1)[0].split("?", 1)[0])
    if not path or path == "/":
        return "index.html"
    clean = path.lstrip("/")
    clean = re.sub(r"/{2,}", "/", clean)
    while clean.startswith("../"):
        clean = clean[3:]
    candidates = []
    # Exact file.
    if clean in file_set:
        candidates.append(clean)
    # Pretty URL directory/index.html.
    if clean.endswith("/") and clean[:-1] + "/index.html" in file_set:
        candidates.append(clean[:-1] + "/index.html")
    if (ROOT / clean).is_dir() and clean.rstrip("/") + "/index.html" in file_set:
        candidates.append(clean.rstrip("/") + "/index.html")
    # /foo -> /foo.html or /foo/index.html
    if not clean.endswith(".html"):
        if clean + ".html" in file_set:
            candidates.append(clean + ".html")
        if clean.rstrip("/") + "/index.html" in file_set:
            candidates.append(clean.rstrip("/") + "/index.html")
    # /foo.html -> /foo/index.html
    if clean.endswith(".html") and clean[:-5] + "/index.html" in file_set:
        candidates.append(clean[:-5] + "/index.html")
    # Case-only mismatch.
    if clean.lower() in file_lower:
        candidates.extend(file_lower[clean.lower()])
    # Unique filename fallback for images only; caller controls this separately.
    uniq = sorted(set(candidates))
    return uniq[0] if len(uniq) == 1 else (None if not uniq else "AMBIGUOUS")


def target_for(src: Path, raw: str):
    u = urlsplit(raw)
    path = u.path
    if u.scheme or u.netloc:
        if u.netloc and u.netloc.lower() in SITE_HOSTS and (not u.scheme or u.scheme in {"http", "https"}):
            return ("internal", path or "/", u)
        return ("external", None, u)
    if raw.startswith("//"):
        return ("external", None, u)
    if raw.startswith("/"):
        return ("internal", path or "/", u)
    base = source_url_path(src)
    base_dir = base.rsplit("/", 1)[0] + "/" if not base.endswith("/") else base
    # URL-style relative resolution without touching the filesystem.
    from posixpath import normpath
    resolved = "/" + normpath(base_dir + path).lstrip("/")
    return ("internal", resolved, u)


def replacement_for(src: Path, candidate_rel: str, original_raw: str):
    u = urlsplit(original_raw)
    # Preserve fragment/query.
    if candidate_rel == "index.html":
        target_url = "/"
    elif candidate_rel.endswith("/index.html"):
        target_url = "/" + candidate_rel[:-10] + "/"
    else:
        target_url = "/" + candidate_rel
    # Preserve pretty URL style where possible.
    from posixpath import relpath
    src_url = source_url_path(src)
    base = src_url if src_url.endswith("/") else src_url.rsplit("/", 1)[0] + "/"
    rel = relpath(target_url, base)
    if rel == ".":
        rel = "./"
    if not original_raw.startswith("/"):
        new_path = rel
    else:
        new_path = target_url
    return urlunsplit((u.scheme, u.netloc, new_path, u.query, u.fragment))


def unique_image_by_name(path: str):
    name = Path(path).name.lower()
    exact = [r for r in file_set if Path(r).name.lower() == name]
    if len(exact) == 1:
        return exact[0]
    # Also allow a unique stem match when the extension was changed.
    stem = Path(name).stem
    stem_matches = [r for r in file_set if Path(r).stem.lower() == stem and Path(r).suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif"}]
    return stem_matches[0] if len(stem_matches) == 1 else None


def is_image_attr(src: Path, attr: str, raw: str) -> bool:
    if attr.lower() != "src":
        return False
    ext = Path(urlsplit(raw).path).suffix.lower()
    return ext in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".avif", ".bmp"} or "<img" in ""

for html in html_files:
    text = html.read_text(encoding="utf-8", errors="ignore")
    replacements = []
    for m in ATTR_RE.finditer(text):
        attr = m.group("attr").lower()
        raw = unescape(m.group("url").strip())
        if not raw or raw.startswith(("#", "javascript:", "mailto:", "tel:", "data:", "blob:")):
            continue
        kind, path, u = target_for(html, raw)
        if kind == "external":
            ext_url = urlunsplit((u.scheme or "https", u.netloc, u.path, u.query, u.fragment))
            if ext_url in checked_external or not u.netloc:
                continue
            checked_external.add(ext_url)
            try:
                r = requests.head(ext_url, allow_redirects=True, timeout=12, headers={"User-Agent": "Tennis-Unified-Site-Audit/1.0"})
                if r.status_code in {405, 403}:
                    r = requests.get(ext_url, allow_redirects=True, timeout=12, stream=True, headers={"User-Agent": "Tennis-Unified-Site-Audit/1.0"})
                if r.url != ext_url and r.status_code < 400:
                    external_redirects.append((ext_url, r.url, r.status_code))
                elif r.status_code >= 400:
                    external_404.append((html.relative_to(ROOT).as_posix(), raw, r.status_code))
            except requests.RequestException as e:
                external_404.append((html.relative_to(ROOT).as_posix(), raw, f"ERROR {e.__class__.__name__}"))
            continue

        candidate = canonical_candidate(path)
        if candidate and candidate != "AMBIGUOUS":
            # Missing only if the exact resolved target is not already the candidate's URL.
            resolved_clean = unquote(path).lstrip("/").rstrip("/")
            if candidate == "index.html" and path == "/":
                continue
            if resolved_clean == candidate or resolved_clean + "/index.html" == candidate:
                continue
            new_raw = replacement_for(html, candidate, raw)
            if new_raw != raw:
                replacements.append((m.start("url"), m.end("url"), new_raw, raw, candidate, attr))
            continue

        # For broken image references, repair by unique filename/stem.
        if attr == "src":
            img_candidate = unique_image_by_name(path)
            if img_candidate:
                new_raw = replacement_for(html, img_candidate, raw)
                replacements.append((m.start("url"), m.end("url"), new_raw, raw, img_candidate, attr))
                continue

        unresolved_local.append((html.relative_to(ROOT).as_posix(), raw, path, attr))

    if replacements:
        # Apply from right to left.
        for a, b, new, old, candidate, attr in sorted(set(replacements), reverse=True):
            text = text[:a] + new + text[b:]
            fixes.append((html.relative_to(ROOT).as_posix(), old, new, candidate, attr))
        html.write_text(text, encoding="utf-8")

# De-duplicate and make the report deterministic.
fixes = sorted(set(fixes))
unresolved_local = sorted(set(unresolved_local))
external_404 = sorted(set(external_404))
external_redirects = sorted(set(external_redirects))

lines = [
    "# Tennis Unified — Link & Image Audit",
    "",
    f"Scanned **{len(html_files):,} HTML pages**.",
    "",
    f"- Automatic local repairs: **{len(fixes):,}**",
    f"- Unresolved local references: **{len(unresolved_local):,}**",
    f"- External URLs returning 4xx/5xx/errors: **{len(external_404):,}**",
    f"- External URLs redirected: **{len(external_redirects):,}**",
    "",
]
if fixes:
    lines += ["## Automatic repairs", ""]
    for page, old, new, candidate, attr in fixes[:5000]:
        lines.append(f"- `{page}` — `{attr}` `{old}` → `{new}` (target `{candidate}`)")
    if len(fixes) > 5000:
        lines.append(f"- … {len(fixes)-5000:,} more repairs omitted from this report")
    lines.append("")
if unresolved_local:
    lines += ["## Unresolved local references", ""]
    for page, raw, path, attr in unresolved_local[:5000]:
        lines.append(f"- `{page}` — `{attr}` `{raw}` → resolved `{path}`")
    lines.append("")
if external_404:
    lines += ["## External URLs requiring review", ""]
    for page, raw, status in external_404[:5000]:
        lines.append(f"- `{page}` — `{raw}` — **{status}**")
    lines.append("")
if external_redirects:
    lines += ["## External redirects (not rewritten automatically)", ""]
    for old, new, status in external_redirects[:5000]:
        lines.append(f"- `{old}` → `{new}` — {status}")
    lines.append("")

REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"HTML pages: {len(html_files)}")
print(f"Automatic repairs: {len(fixes)}")
print(f"Unresolved local: {len(unresolved_local)}")
print(f"External errors: {len(external_404)}")
print(f"External redirects: {len(external_redirects)}")
# Do not fail the job for external sites; local 404s are the repair target.
sys.exit(0)
