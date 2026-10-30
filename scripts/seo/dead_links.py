#!/usr/bin/env python3
"""
dead_links.py — every local href/src in the tree, resolved against the filesystem.

`link_audit.py` was scoped to 93 surface pages, so a reader-side dead link could not
appear in its report. This one walks the whole tree and resolves each reference:

  - skips tnkb/ (retired 2026-10-29, redirect stubs) and node_modules/.git
  - skips external schemes (http, https, mailto, tel, data, javascript, //)
  - absolute /x/y -> repo root; relative -> the referring file's directory
  - query and fragment stripped; percent-decoding applied (spaces in filenames)
  - a path with no extension, or ending in '/', also tries /index.html
  - a resolved path is only counted once per file (a page repeating a link is
    still one broken link for the reader, but the report keeps the count)

Read-only. Report by default, sorted by how many pages point at the same missing
target — the shape that matters is "one missing page, many referrers", because
that is one repair, not many.

Usage:
  python scripts/seo/dead_links.py --root . [--prefix books/] [--limit 40] [--all]
"""
import argparse
import os
import re
import sys
import urllib.parse
from collections import Counter, defaultdict

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github"}
SKIP_PREFIX = ("tnkb/",)
EXT_SCHEME = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)
ATTR = re.compile(r"""\b(?:href|src|data-src|poster)\s*=\s*["']([^"']+)["']""", re.I)


def local_targets(text):
    for m in ATTR.finditer(text):
        raw = m.group(1).strip()
        if not raw or EXT_SCHEME.match(raw):
            continue
        if raw.startswith("#"):
            continue
        yield raw


def resolve(ref, page, cache):
    t = ref.split("#", 1)[0].split("?", 1)[0]
    if not t:
        return None
    try:
        t = urllib.parse.unquote(t)
    except Exception:
        pass
    if t.startswith("/"):
        p = t.lstrip("/")
    else:
        p = os.path.normpath(os.path.join(os.path.dirname(page), t))
    p = p.replace("\\", "/")
    if p in cache:
        return None if cache[p] else p
    cands = [p]
    if p.endswith("/"):
        cands = [p + "index.html"]
    elif "." not in os.path.basename(p):
        cands = [p, p + "/index.html"]
    ok = any(os.path.exists(c) for c in cands)
    cache[p] = ok
    return None if ok else p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--prefix", action="append", default=None,
                    help="only pages under these prefixes (repeatable)")
    ap.add_argument("--limit", type=int, default=40)
    ap.add_argument("--all", action="store_true", help="list every referring page")
    args = ap.parse_args()

    os.chdir(args.root)
    pages = []
    for dirpath, dirnames, filenames in os.walk("."):
        rel_dir = os.path.relpath(dirpath, ".").replace("\\", "/")
        if rel_dir == ".":
            rel_dir = ""
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.lower().endswith((".html", ".htm")):
                continue
            rel = (rel_dir + "/" + fn) if rel_dir else fn
            if any(rel.startswith(s) for s in SKIP_PREFIX):
                continue
            if args.prefix and not any(rel.startswith(s) for s in args.prefix):
                continue
            pages.append(rel)

    cache = {}
    missing = Counter()             # target -> referrer count
    referrers = defaultdict(list)   # target -> pages
    checked = 0
    for page in pages:
        try:
            text = open(page, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        seen = set()
        for ref in local_targets(text):
            checked += 1
            miss = resolve(ref, page, cache)
            if miss and miss not in seen:
                seen.add(miss)
                missing[miss] += 1
                referrers[miss].append(page)

    total_edges = sum(missing.values())
    print(f"pages: {len(pages)}   references checked: {checked}   "
          f"missing targets: {len(missing)}   dead edges: {total_edges}")

    if not missing:
        print("no dead local references")
        return

    print(f"\n{'pages':>6}  missing target")
    for target, n in missing.most_common(args.limit):
        print(f"{n:>6}  {target}")
        if args.all or n <= 3:
            for r in referrers[target][:8]:
                print(f"          <- {r}")
    if len(missing) > args.limit:
        print(f"\n... {len(missing) - args.limit} more missing targets (raise --limit)")


if __name__ == "__main__":
    main()
