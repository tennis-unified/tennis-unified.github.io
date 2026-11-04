#!/usr/bin/env python3
"""
canonical_fill_scoped.py — fill self-canonicals on indexable content pages in
dirs that no pass ever covered, using canonical_fill.py's detection machinery.

Scope (2026-11-03 measurement: 1,618 no-canonical pages, of which ~28 are
fragments/noindex/headless and blog/ + books/ carry standing decisions):
  vi/tennis-technical-reference  (453)
  tennis-technical-reference/gemini-notebooks  (449)
  vi/books  (127)   vi/doubles  (6)
  en/articles (5)   vi/articles (5)   vi/cam-nang (5)

Skipped inside scope: pages with a robots noindex meta, no <head>, or a
basename starting with 404. Insertion mirrors canonical_fill.py: before the
first alternate tag (matching indent), else before </head>. Byte-guarded.

Usage: python scripts/seo/canonical_fill_scoped.py [--write]
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from canonical_fill import CAN_RE, ALT_RE, HEAD_END_RE, self_href  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCOPE = (
    "vi/tennis-technical-reference/",
    "tennis-technical-reference/gemini-notebooks/",
    "vi/books/",
    "vi/doubles/",
    "en/articles/",
    "vi/articles/",
    "vi/cam-nang/",
)
SKIP_DIRS = {".git", "node_modules", "_tmp", ".workbuddy-ai"}
NOINDEX_RE = re.compile(r'<meta[^>]*name="robots"[^>]*content="[^"]*noindex', re.I)


def main():
    write = "--write" in sys.argv
    from collections import Counter
    plan, skipped = [], Counter()
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if not f.lower().endswith((".html", ".htm")):
                continue
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/")
            if not rel.startswith(SCOPE):
                continue
            base = os.path.basename(rel).lower()
            if base.startswith("404"):
                continue
            with open(os.path.join(dp, f), "rb") as fh:
                text = fh.read().decode("utf-8", "replace")
            if CAN_RE.search(text):
                continue
            if not HEAD_END_RE.search(text):
                skipped["no </head>"] += 1
                continue
            if NOINDEX_RE.search(text):
                skipped["robots noindex"] += 1
                continue
            href = self_href(rel)
            tag = '<link rel="canonical" href="%s">' % href
            alt = ALT_RE.search(text)
            if alt:
                insert = "%s%s\n" % (alt.group(1), tag)
                pos = alt.start()
            else:
                m = HEAD_END_RE.search(text)
                insert = "%s%s\n" % (" " * 4, tag)
                pos = m.start()
            new = text[:pos] + insert + text[pos:]
            plan.append((rel, os.path.join(dp, f), tag, new, insert))
            skipped["to fill"] += 1

    print("pages to fill:", len(plan))
    for k, v in skipped.most_common():
        print("  %-14s %d" % (k, v))
    for rel, _f, tag, _n, _i in plan[:5]:
        print("  e.g. %s\n       %s" % (rel, tag))
    if not write:
        print("\nREPORT ONLY. Re-run with --write.")
        return

    written = 0
    for rel, full, tag, new, insert in plan:
        with open(full, "rb") as fh:
            before = fh.read()
        after = new.encode("utf-8")
        if after.replace(insert.encode("utf-8"), b"", 1) != before:
            print("  SKIP (change wider than insertion):", rel)
            continue
        if after.count(b'rel="canonical"') != 1:
            print("  SKIP (canonical count != 1):", rel)
            continue
        with open(full, "wb") as fh:
            fh.write(after)
        written += 1
    print("written:", written)


if __name__ == "__main__":
    main()
