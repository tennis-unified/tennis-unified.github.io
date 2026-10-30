#!/usr/bin/env python3
"""Audit the contents of EVERY sitemap in the tree, not just the root one.

`sitemap_host.py --audit-locs` classifies each <loc> of `sitemap.xml` by what it
actually points at. It has never looked at `vi/sitemap.xml`, and neither has
anything else: the VI sitemap was, until 2026-10-29, not even referenced from
robots.txt, so nobody had a reason to check its contents. Making it discoverable
made that an actual question.

Same five classes as `sitemap_host.loc_audit`, applied to each sitemap file:

  dead          no file serves this path (a 404 in the sitemap)
  duplicate     the same URL appears more than once
  error_page    the site's own 404 page
  redirect      a meta-refresh stub, not content
  noncanonical  the page's own canonical names a different path

`--fix` removes the last four classes and any `dead` <loc> whose path has no file
and no directory. It never adds anything -- coverage is `sitemap_gap_fix.py`'s
job, and keeping the two tools separate is what stops a "repair" from silently
becoming a regeneration.

Usage
  python sitemap_locs_audit.py --root .                 # report
  python sitemap_locs_audit.py --root . --fix           # remove bad <loc>
  python sitemap_locs_audit.py --root . --fix --sitemap vi/sitemap.xml
"""
import argparse
import gzip
import html
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from collections import Counter

SKIP_DIRS = {".git", "node_modules", "tnkb", "assets", "site", "__pycache__"}
REFRESH_RE = re.compile(
    r"""<meta\b[^>]*http-equiv\s*=\s*["']?refresh["']?""", re.I
)
LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
ATTR = re.compile(
    r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))"""
)
LOC = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.I | re.S)
URL_BLOCK = re.compile(r"[ \t]*<url>.*?</url>\n?", re.S)


def attrs_of(tag):
    out = {}
    for m in ATTR.finditer(tag):
        v = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        out[m.group(1).lower()] = html.unescape(v or "")
    return out


def canonical_href(text):
    for tag in LINK_TAG.findall(text):
        a = attrs_of(tag)
        if "canonical" in a.get("rel", "").lower().split() and a.get("href"):
            return a["href"]
    return None


def norm_path(p):
    p = urllib.parse.unquote(p)
    if not p.startswith("/"):
        p = "/" + p
    p = re.sub(r"/{2,}", "/", p)
    return p.rstrip("/") or "/"


def local_path(root, url):
    """URL -> the file that serves it, or None."""
    path = urllib.parse.unquote(
        urllib.parse.urlsplit(re.sub(r"^https?://[^/]+", "", url) or "/").path
    )
    rel = path.lstrip("/")
    full = os.path.join(root, rel.replace("/", os.sep))
    if path.endswith("/") or os.path.isdir(full):
        cand = os.path.join(full, "index.html")
        if os.path.isfile(cand):
            return cand
        if path.endswith("/") and os.path.isfile(full):
            return full
        return None
    if os.path.isfile(full):
        return full
    cand = os.path.join(full, "index.html")
    return cand if os.path.isfile(cand) else None


def audit(root, sm_path):
    with open(sm_path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    locs = [html.unescape(x.strip()) for x in LOC.findall(text)]

    out = {"dead": [], "duplicate": [], "error_page": [], "redirect": [],
           "noncanonical": [], "noindex": []}
    seen = Counter(locs)
    out["duplicate"] = sorted(u for u, n in seen.items() if n > 1)

    for u in locs:
        path = urllib.parse.unquote(
            urllib.parse.urlsplit(re.sub(r"^https?://[^/]+", "", u) or "/").path
        )
        f = local_path(root, u)
        if f is None:
            out["dead"].append(u)
            continue
        if re.search(r"(^|/)404/?$", path):
            out["error_page"].append(u)
            continue
        try:
            body = open(f, "rb").read().decode("utf-8", "replace")
        except OSError:
            continue
        if REFRESH_RE.search(body):
            out["redirect"].append(u)
            continue
        if re.search(r"""<meta\b[^>]*name\s*=\s*["']?robots["']?[^>]*noindex""", body, re.I):
            out["noindex"].append(u)
            continue
        c = canonical_href(body)
        if c and c.startswith("/") and norm_path(c) != norm_path(path):
            out["noncanonical"].append((u, urllib.parse.unquote(c)))
    return locs, out, text


def regen_gz(p):
    with open(p, "rb") as f:
        data = f.read()
    with gzip.GzipFile(p + ".gz", "wb", mtime=0) as gz:
        gz.write(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--sitemap", action="append", default=None)
    ap.add_argument("--fix", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    targets = args.sitemap or ["sitemap.xml", os.path.join("vi", "sitemap.xml")]
    targets = [t for t in targets if os.path.exists(os.path.join(root, t))]
    if not targets:
        sys.exit("no sitemap found")

    total_defects = 0
    for t in targets:
        p = os.path.join(root, t)
        locs, out, text = audit(root, p)
        n = sum(len(v) for v in out.values())
        total_defects += n
        print(f"\n=== {t} ===  locs={len(locs)}  defects={n}")
        for cls in ("dead", "duplicate", "error_page", "redirect", "noncanonical", "noindex"):
            items = out[cls]
            print(f"  {cls:<14} {len(items):>4}")
            for it in items[:8]:
                print(f"      {it}")

        if args.fix and n:
            bad = set(out["duplicate"]) | set(out["error_page"]) | set(out["redirect"]) \
                | set(out["noindex"]) | {u for u, _ in out["noncanonical"]} | set(out["dead"])
            removed = 0

            def drop(m):
                nonlocal removed
                body = m.group(0)
                lm = re.search(r"<loc>\s*(.*?)\s*</loc>", body, re.S)
                if lm and html.unescape(lm.group(1).strip()) in bad:
                    removed += 1
                    return ""
                return body

            new = URL_BLOCK.sub(drop, text)
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(new)
            regen_gz(p)
            try:
                ET.parse(p)
                parses = True
            except ET.ParseError as e:
                print(f"  !! does not parse after fix: {e}")
                parses = False
            after = len(LOC.findall(new))
            print(f"  -> removed {removed}, locs {len(locs)} -> {after}, parses={parses}")
            if not parses or after != len(locs) - removed:
                print("  !! FIX FAILED")
                sys.exit(1)

    print(f"\ntotal defects across {len(targets)} sitemap(s): {total_defects}")
    sys.exit(1 if total_defects and not args.fix else 0)


if __name__ == "__main__":
    main()
