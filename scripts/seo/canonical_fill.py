# -*- coding: utf-8 -*-
"""
Fill the missing self-canonical on pages that already declare hreflang.

seo_fix.py only ever looks at three prefixes (articles/, en/articles/, vi/articles/),
so its "0 failures" says nothing about the rest of the tree. Measured 2026-10-28:
12,063 HTML pages, 8,192 with no canonical, and of those **3,764 declare hreflang but
no canonical** -- a page that tells Google which pages are its translations, yet never
says which URL is authoritative for itself.

Scope: exactly that set, minus the spaces that carry a standing decision to the contrary:

  blog/, vi/blog/   seo_fix.py records a deliberate decision NOT to give the blog
                    blanket self-canonicals (only the 17 extra-title duplicates are
                    canonicalised). Left alone.
  books/            another stream's working tree (seo_fix skips it too).
  tnkb/, tenniskb/  frozen archives / legacy spaces, kept as-is.

Placement matches the tree's existing convention: the canonical goes immediately
before the first alternate tag, with that tag's indentation. Hrefs are root-relative
and percent-encoded (D1: the same tree is served by two hosts, so an absolute host is
wrong on one of them; 1,167 of 1,171 existing canonicals with spaces use %20).

Usage:
  python scripts/seo/canonical_fill.py            # report
  python scripts/seo/canonical_fill.py --write
"""
import os
import re
import sys
from collections import Counter
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", "node_modules", "_tmp", ".workbuddy-ai"}
# Spaces with a standing reason to stay untouched (see module docstring).
EXCLUDE_PREFIX = ("blog/", "vi/blog/", "books/", "tnkb/", "tenniskb/")

CAN_RE = re.compile(r'<link\s+rel="canonical"', re.I)
ALT_RE = re.compile(r'([ \t]*)<link\s+rel="alternate"', re.I)
HEAD_END_RE = re.compile(r"</head>", re.I)


def self_href(rel):
    """Root-relative, percent-encoded self URL, index.html collapsed to its directory."""
    d, base = os.path.split(rel)
    if base.lower() in ("index.html", "index.htm"):
        path = "/" + (d + "/" if d else "")
    else:
        path = "/" + rel
    return quote(path, safe="/")


def iter_html():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if not f.lower().endswith((".html", ".htm")):
                continue
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/")
            yield os.path.join(dp, f), rel


def main():
    write = "--write" in sys.argv
    plan, skipped_no_head, skipped_excluded = [], [], 0
    by_prefix = Counter()

    for full, rel in iter_html():
        if rel.startswith(EXCLUDE_PREFIX):
            skipped_excluded += 1
            continue
        if os.path.basename(rel).lower().startswith("404"):
            continue                      # error page, not content
        with open(full, "rb") as fh:
            text = fh.read().decode("utf-8", "replace")
        if CAN_RE.search(text):
            continue
        alt = ALT_RE.search(text)
        if not alt:
            continue                      # no hreflang: outside this tool's scope
        if not HEAD_END_RE.search(text):
            skipped_no_head.append(rel)
            continue
        href = self_href(rel)
        tag = f'<link rel="canonical" href="{href}">'
        insert = f"{alt.group(1)}{tag}\n"
        new = text[:alt.start()] + insert + text[alt.start():]
        plan.append((rel, full, tag, new, insert))
        by_prefix[rel.split("/")[0]] += 1

    print(f"pages to receive a self-canonical : {len(plan):,}")
    print(f"skipped, excluded space           : {skipped_excluded:,}")
    print(f"skipped, no </head>               : {len(skipped_no_head)}")
    for k, v in by_prefix.most_common(12):
        print(f"    {v:>5}  {k}")
    for rel, _f, tag, _n, _i in plan[:5]:
        print(f"  e.g. {rel}\n       {tag}")

    if not write:
        print("\nREPORT ONLY. Re-run with --write to apply.")
        return

    written = 0
    for rel, full, tag, new, insert in plan:
        with open(full, "rb") as fh:
            before = fh.read()
        after = new.encode("utf-8")
        # the ONLY difference must be the inserted line
        if after.replace(insert.encode("utf-8"), b"", 1) != before:
            print(f"  SKIP (change wider than the insertion): {rel}")
            continue
        if after.count(b'rel="canonical"') != 1:
            print(f"  SKIP (canonical count != 1): {rel}")
            continue
        with open(full, "wb") as fh:
            fh.write(after)
        written += 1
    print(f"\nwrote {written} canonicals")


if __name__ == "__main__":
    main()
