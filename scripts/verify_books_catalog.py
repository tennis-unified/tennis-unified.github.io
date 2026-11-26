#!/usr/bin/env python3
"""Verify the tennis book catalogs, glossary and deep-dive map are internally consistent.

Run from anywhere:  python scripts/verify_books_catalog.py
Exits 1 on any broken local link, duplicate anchor ID, orphan cluster or count drift.
Standard library only, so it can run in CI without extra dependencies.
"""

import glob
import gzip
import html
import json
import os
import posixpath
import re
import subprocess
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VI = os.path.join(ROOT, "vi", "books")
EN = os.path.join(ROOT, "books")
CARD_RE = re.compile(r"<article\s+class=\"book-card-horizontal\"(.*?)>(.*?)</article>", re.S)

# A sparse checkout may not materialise every linked file, so also trust the git tree.
try:
    TRACKED = set(subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=ROOT, text=True,
        encoding="utf-8", stderr=subprocess.DEVNULL).splitlines())
except Exception:
    TRACKED = set()

errors = []


def check(label, actual, expected):
    ok = actual == expected
    print(f"{'PASS' if ok else 'FAIL'}  {label}: {actual} (expected {expected})")
    if not ok:
        errors.append(label)


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def local_exists(href, base=None):
    path = href.split("#", 1)[0].split("?", 1)[0]
    if not path or path.startswith(("http://", "https://", "mailto:")):
        return True
    if path.startswith("/"):
        full = os.path.join(ROOT, path.lstrip("/"))
    else:
        full = os.path.join(base or ROOT, path)
    if os.path.isdir(full):
        index = os.path.join(full, "index.html")
        if os.path.isfile(index):
            return True
        rel = os.path.relpath(index, ROOT).replace("\\", "/")
        return rel in TRACKED
    if os.path.isfile(full):
        return True
    rel = os.path.relpath(full, ROOT).replace("\\", "/")
    return rel in TRACKED or rel + "/index.html" in TRACKED


def cards(html):
    out = []
    for attrs, body in CARD_RE.findall(html):
        ident = re.search(r"\bid=\"([^\"]+)\"", attrs)
        out.append({
            "id": ident.group(1) if ident else None,
            "body": body,
            "links": re.findall(r"\bhref=\"([^\"]+)\"", body),
        })
    return out


# --- Vietnamese catalog ---
vi_html = read(os.path.join(VI, "index.html"))
vi_cards = cards(vi_html)
check("VI catalog card count", len(vi_cards), 96)
bad_vi = [h for c in vi_cards for h in c["links"] if not local_exists(h, VI)]
check("broken links in VI catalog", len(bad_vi), 0)
counter = re.search(r"id=\"tuSearchCounter\"[^>]*>(\d+)\s*/\s*(\d+)", vi_html)
check("VI search counter total", int(counter.group(2)) if counter else -1, len(vi_cards))
intro = re.search(r"trong (\d+) đầu sách", vi_html)
check("VI intro book count", int(intro.group(1)) if intro else -1, len(vi_cards))

# --- English catalog ---
en_html = read(os.path.join(EN, "index.html"))
en_cards = cards(en_html)
ids = [c["id"] for c in en_cards if c["id"]]
check("duplicate anchor IDs on EN catalog", sum(n - 1 for n in Counter(ids).values() if n > 1), 0)
check("path-like anchor IDs on EN catalog", len([i for i in ids if "/" in i or ".." in i]), 0)
anchors = [h.split("#", 1)[1] for c in vi_cards for h in c["links"] if h.startswith("/books/#")]
check("dead VI -> EN anchors", len([a for a in anchors if a not in ids]), 0)

# --- Vietnamese sitemap ---
# Every catalog reader must be discoverable. Links are relative to vi/books/;
# normalise '../doubles/...' to '/vi/doubles/...' before comparing with <loc>.
sitemap = read(os.path.join(ROOT, "vi", "sitemap.xml"))
locs = re.findall(r"<loc>(.*?)</loc>", sitemap)
check("duplicate URLs in VI sitemap", len(locs) - len(set(locs)), 0)
reader_links = {h for c in vi_cards for h in c["links"] if h.endswith("_vi.html")}
expected_locs = {
    "https://tenniskb.github.io/vi/" + posixpath.normpath(posixpath.join("books", link))
    for link in reader_links
}
check("VI readers missing from sitemap", len(expected_locs - set(locs)), 0)
gz_path = os.path.join(ROOT, "vi", "sitemap.xml.gz")
if os.path.isfile(gz_path):
    with gzip.open(gz_path, "rt", encoding="utf-8") as f:
        check("sitemap gzip matches XML", f.read() == sitemap, True)

# --- Glossary ---
gl_html = read(os.path.join(VI, "glossary.html"))
terms = json.loads(re.search(r"const ALL_TERMS = (\[.*?\]);", gl_html, re.S).group(1))
claimed = re.search(r"(\d+)\s*(?:thuật ngữ|Thuật Ngữ)", gl_html)
check("glossary term count", len(terms), int(claimed.group(1)) if claimed else -1)
sources = {s["href"] for t in terms for s in t.get("sources", [])}
broken = [h for h in sources if not local_exists(h, VI)]
check("broken glossary citations", len(broken), 0)

# --- Deep-dive map ---
dd_html = read(os.path.join(VI, "deep-dive", "index.html"))
data = json.loads(re.search(r"const DATA = (\{.*?\});", dd_html, re.S).group(1))
clusters = {c["id"] for c in data["clusters"]}
orphans = [b["id"] for b in data["books"] if b["ch"] not in clusters]
check("orphan mind-map clusters", len(orphans), 0)
paths = [b[k] for b in data["books"] for k in ("vipath", "enpath", "pdf") if b.get(k)]
check("broken mind-map paths", len([p for p in paths if not local_exists(p)]), 0)
claim = re.search(r"(\d+) tác phẩm lớn", dd_html)
check("mind-map work count", len(data["books"]), int(claim.group(1)) if claim else -1)

# Informational: title drift and bilingual pairing anomalies in materialised readers.
# These are warnings, not failures -- they need editorial judgement, not a build break.
def numeric_sequence(fragment):
    """Extract numeric literals, normalising Vietnamese decimal commas to dots."""
    out = []
    for token in re.findall(r"\b\d[\d.,]*\b", fragment):
        token = token.replace(",", ".")
        try:
            out.append(f"{float(token):g}")
        except ValueError:
            pass
    return out

def title_core(value):
    """Normalise cosmetic title differences (HTML entities, subtitles, authors)."""
    text = html.unescape(re.sub(r"<[^>]+>", "", value))
    text = re.sub(r"\([^)]*\)", "", text)  # catalog's English subtitle
    text = re.split(r"[:\-–—·]", text)[0]  # subtitle/author after the first separator
    return re.sub(r"\s+", " ", text).strip().casefold()


title_drift = []
pairing = []
drift = []
canonical_errors = []
for card in vi_cards:
    reader = next((h for h in card["links"] if h.endswith("_vi.html")), None)
    if not reader:
        continue
    path = os.path.join(VI, reader)
    if not os.path.isfile(path):
        continue
    page = read(path)
    is_redirect = bool(
        re.search(r'<meta[^>]+http-equiv=["\']refresh["\']', page, re.I)
        or re.search(r"window\.location\.replace", page, re.I)
    )
    if not is_redirect:
        canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', page, re.I)
        expected_canonical = "/vi/" + posixpath.normpath(posixpath.join("books", reader))
        if not canonical:
            canonical_errors.append((reader, "missing"))
        elif canonical.group(1) != expected_canonical:
            canonical_errors.append((reader, canonical.group(1)))
    card_title = re.search(r"class=\"book-card-title\"[^>]*>(.*?)</h3>", card["body"], re.S)
    h1 = re.search(r"<h1\b[^>]*>(.*?)</h1>", page, re.S)
    if card_title and h1:
        if title_core(card_title.group(1)) != title_core(h1.group(1)):
            title_drift.append(reader)
    blocks = re.findall(r"<div[^>]*class=\"[^\"]*bilingual-block[^\"]*\"[^>]*>(.*?)</div>", page, re.S)
    if blocks:
        en_blocks = sum(1 for b in blocks if "lang-en" in b)
        unpaired = sum(1 for b in blocks if "lang-vi" in b and "lang-en" not in b)
        # Vietnamese-only books are intentional; only mixed pages can be misaligned.
        if en_blocks > 0 and unpaired > 3:
            pairing.append((reader, unpaired))

        # Independent signal: in a correctly aligned pair, numeric literals on the
        # Vietnamese and English sides normally match. Persistent disagreement is
        # evidence of re-chunked paragraph boundaries even when every block is paired.
        tested = identical = 0
        for b in blocks:
            vi_p = re.search(r'class="lang-vi"[^>]*>(.*?)</p>', b, re.S)
            en_p = re.search(r'class="lang-en"[^>]*>(.*?)</p>', b, re.S)
            if not (vi_p and en_p):
                continue
            strip = lambda s: re.sub(r"<[^>]+>", "", s)
            vn = numeric_sequence(strip(vi_p.group(1)))
            en = numeric_sequence(strip(en_p.group(1)))
            if vn and en:
                tested += 1
                if vn == en:
                    identical += 1
        if tested >= 20 and identical / tested < 0.10:
            drift.append((reader, identical, tested))

check("wrong or missing reader canonicals", len(canonical_errors), 0)
if canonical_errors:
    for name, value in canonical_errors[:10]:
        print(f"       {name}: {value}")

# --- Links inside readers (not just the catalog cards) ---
reader_pages = glob.glob(os.path.join(VI, "*_vi.html"))
reader_pages += glob.glob(os.path.join(os.path.dirname(VI), "doubles", "*_vi.html"))
broken_reader_links = []
for page_path in reader_pages:
    base = os.path.dirname(page_path)
    for url in re.findall(r'(?:href|src)="([^"]+)"', read(page_path)):
        if not url or url.startswith(("#", "http://", "https://", "mailto:", "data:", "javascript:", "tel:")):
            continue
        path = url.split("#", 1)[0].split("?", 1)[0]
        if path and not local_exists(path, base):
            broken_reader_links.append((os.path.relpath(page_path, ROOT), url))
check("broken links in VI readers", len(broken_reader_links), 0)
if broken_reader_links:
    for name, url in broken_reader_links[:10]:
        print(f"       {name}: {url}")

# --- English readers ---
en_pages = glob.glob(os.path.join(EN, "*_en.html"))
en_errors = []
en_broken = []
en_missing_desc = []
for page_path in en_pages:
    name = os.path.basename(page_path)
    page = read(page_path)
    is_redirect = bool(
        re.search(r'<meta[^>]+http-equiv=["\']refresh["\']', page, re.I)
        or re.search(r"window\.location\.replace", page, re.I)
    )
    if not is_redirect:
        if not re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'][^"\']+', page, re.I):
            en_missing_desc.append(name)
        canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', page, re.I)
        expected = "/books/" + name
        if not canonical:
            en_errors.append((name, "missing"))
        elif canonical.group(1) != expected:
            en_errors.append((name, canonical.group(1)))
    for url in re.findall(r'(?:href|src)="([^"]+)"', page):
        if not url or url.startswith(("#", "http://", "https://", "mailto:", "data:", "javascript:", "tel:")):
            continue
        path = url.split("#", 1)[0].split("?", 1)[0]
        if path and not local_exists(path, os.path.dirname(page_path)):
            en_broken.append((name, url))
check("wrong or missing EN reader canonicals", len(en_errors), 0)
check("broken links in EN readers", len(en_broken), 0)
check("EN readers missing meta description", len(en_missing_desc), 0)
if en_errors:
    for name, value in en_errors[:10]:
        print(f"       {name}: {value}")
if en_broken:
    for name, url in en_broken[:10]:
        print(f"       {name}: {url}")

print(f"INFO  reader title drift (materialised pages only): {len(title_drift)}")
for name in title_drift[:10]:
    print("      ", name)
print(f"INFO  readers with >3 unpaired bilingual blocks: {len(pairing)}")
for name, count in pairing[:10]:
    print(f"       {name}: {count}")
print(f"INFO  readers with <10% paired-number agreement: {len(drift)}")
for name, identical, tested in drift[:10]:
    print(f"       {name}: {identical}/{tested}")

if errors:
    print(f"\n{len(errors)} FAILURES: {errors}")
    sys.exit(1)
print("\nAll book catalog checks passed.")
