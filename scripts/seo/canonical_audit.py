#!/usr/bin/env python3
"""Authoritative measurement of <link rel="canonical"> across the tree.

Why this exists
---------------
Every earlier count of this tree's canonicals was taken with a regex that
required a quoted href:

    href=["']([^"']*)["']

The tree contains 69 pages written by hand as *unquoted* HTML5:

    <link href=https://tennis-unified.github.io/about/ rel=canonical>

Unquoted attribute values are legal, and crawlers parse them, but that regex
returns nothing for them. The result was a recorded figure of "2 absolute
canonicals, both fixed" when the real number is 69. A measurement tool that
silently skips a syntax is worse than no tool, because it produces a confident
wrong number. This one parses attributes properly.

What it checks
--------------
1. coverage        -- how many pages have a canonical at all
2. duplicates      -- more than one canonical tag on one page (always a defect:
                      Google honours the first, so the intent is ambiguous)
3. absolute        -- an absolute URL, which is wrong on one of the two hosts
                      that serve this tree (see D1 in seo_fix.py)
4. dangling        -- a root-relative canonical whose target does not exist on
                      disk, i.e. the page canonicalises to a 404

Exit code is 1 if any defect in classes 2-4 is found, so this can gate CI.

Usage
-----
  python scripts/seo/canonical_audit.py
  python scripts/seo/canonical_audit.py --verbose
"""

import os
import posixpath
import re
import sys
from collections import Counter
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", "node_modules", "_tmp", ".workbuddy-ai"}

LINK_RE = re.compile(r"<link\b[^>]*>", re.I)
ATTR_RE = re.compile(
    r"""([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""",
)


def attrs(tag):
    """Attribute dict for one tag, quote-optional and order-independent."""
    out = {}
    for m in ATTR_RE.finditer(tag):
        name = m.group(1).lower()
        val = m.group(2)
        if val is None:
            val = m.group(3)
        if val is None:
            val = m.group(4)
        out.setdefault(name, val or "")
    return out


def canonicals(text):
    """Every canonical href on the page, in document order."""
    found = []
    for tag in LINK_RE.findall(text):
        a = attrs(tag)
        rel = a.get("rel", "").lower()
        if "canonical" in rel.split():
            found.append(a.get("href", "").strip())
    return found


def has_hreflang(text):
    for tag in LINK_RE.findall(text):
        a = attrs(tag)
        if "alternate" in a.get("rel", "").lower().split() and a.get("hreflang"):
            return True
    return False


def iter_html():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if not f.lower().endswith((".html", ".htm")):
                continue
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/")
            yield os.path.join(dp, f), rel


def resolves(href):
    """Does a root-relative canonical point at something real on disk?"""
    path = unquote(href.split("#")[0].split("?")[0])
    path = posixpath.normpath("/" + path.lstrip("/"))
    target = os.path.join(ROOT, path.lstrip("/").replace("/", os.sep))
    if os.path.isfile(target):
        return True
    if os.path.isdir(target):
        return any(
            os.path.isfile(os.path.join(target, i)) for i in ("index.html", "index.htm")
        )
    return False


def main():
    verbose = "--verbose" in sys.argv
    total = with_canon = 0
    dup, absolute, dangling, no_canon_but_alt = [], [], [], []
    host_counts = Counter()

    for full, rel in iter_html():
        total += 1
        try:
            with open(full, "rb") as fh:
                text = fh.read().decode("utf-8", "replace")
        except OSError:
            continue
        hrefs = canonicals(text)
        if hrefs:
            with_canon += 1
        elif has_hreflang(text):
            no_canon_but_alt.append(rel)

        if len(hrefs) > 1:
            dup.append((rel, hrefs))

        for h in hrefs:
            if h.startswith(("http://", "https://")):
                absolute.append((rel, h))
                m = re.match(r"https?://([^/]+)/", h)
                host_counts[m.group(1) if m else "?"] += 1
            elif h.startswith("/"):
                if not resolves(h):
                    dangling.append((rel, h))

    print(f"html pages                          : {total:,}")
    print(f"  with >=1 canonical                : {with_canon:,}")
    print(f"  with none                         : {total - with_canon:,}")
    print(f"    of those, declare hreflang      : {len(no_canon_but_alt):,}")
    print(f"duplicate canonical tags            : {len(dup)}")
    print(f"absolute canonical tags             : {len(absolute)}")
    for host, n in host_counts.most_common():
        print(f"    {n:>4}  -> {host}")
    print(f"dangling root-relative canonicals   : {len(dangling)}")

    if dup:
        print("\n-- duplicate canonical (first tag wins, so intent is ambiguous)")
        for rel, hrefs in (dup if verbose else dup[:15]):
            print(f"  {rel}\n      {hrefs}")
    if absolute:
        print("\n-- absolute canonical (wrong on the host that is not this one)")
        for rel, h in (absolute if verbose else absolute[:15]):
            print(f"  {rel}\n      {h}")
    if dangling:
        print("\n-- canonical points at a path that does not exist")
        for rel, h in (dangling if verbose else dangling[:15]):
            print(f"  {rel}\n      {h}")

    defects = len(dup) + len(absolute) + len(dangling)
    print(f"\ndefects: {defects}")
    return 1 if defects else 0


if __name__ == "__main__":
    sys.exit(main())
