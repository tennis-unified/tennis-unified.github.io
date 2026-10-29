#!/usr/bin/env python3
"""Audit the x-default invariant: whenever a page declares BOTH an `en` and a `vi`
alternate, it must also declare an `x-default`.

Neither seo_fix.py verify nor hreflang_reciprocal.py checks this, so a page can
satisfy every reciprocity rule and still be missing the fallback Google needs to
choose a URL for unmatched locales.

Report only. Read-only.

  python scripts/seo/xdefault_audit.py            # summary
  python scripts/seo/xdefault_audit.py --list     # + every offending path
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", "node_modules", "site", ".github", "scripts", "sources"}
MAX_BYTES = 1_500_000

HEAD_RE = re.compile(r"<head\b.*?</head>", re.I | re.S)
LINK_RE = re.compile(r"<link\b[^>]*>", re.I)
HREFLANG_RE = re.compile(r"""\shreflang\s*=\s*["']([^"']*)["']""", re.I)
REL_ALT_RE = re.compile(r"""\srel\s*=\s*["']?alternate\b""", re.I)
LANG_RE = re.compile(r"""<html\b[^>]*\slang\s*=\s*["']([^"']*)["']""", re.I)
CANON_RE = re.compile(r"""<link\b[^>]*\srel\s*=\s*["']?canonical""", re.I)


def html_files():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html") or fn.endswith(".htm"):
                yield os.path.join(dirpath, fn)


def main():
    show_list = "--list" in sys.argv
    total = 0
    with_alt = 0
    both = 0
    offenders = []       # has en + vi, no x-default
    no_canon = 0
    by_area = {}

    for path in html_files():
        try:
            if os.path.getsize(path) > MAX_BYTES:
                continue
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        if "hreflang" not in text:
            continue
        m = HEAD_RE.search(text)
        head = m.group(0) if m else text[:20000]
        total += 1

        langs = set()
        for tag in LINK_RE.findall(head):
            if not REL_ALT_RE.search(tag):
                continue
            hm = HREFLANG_RE.search(tag)
            if hm:
                langs.add(hm.group(1).strip().lower())

        if not langs:
            continue
        with_alt += 1
        if not CANON_RE.search(head):
            no_canon += 1
        if "en" in langs and "vi" in langs:
            both += 1
            if "x-default" not in langs:
                rel = os.path.relpath(path, ROOT).replace("\\", "/")
                area = rel.split("/")[0] if "/" in rel else "(root)"
                if rel.startswith("vi/"):
                    area = "vi/" + (rel.split("/")[1] if len(rel.split("/")) > 1 else "")
                offenders.append(rel)
                by_area[area] = by_area.get(area, 0) + 1

    print(f"pages with any alternate      : {with_alt:,}")
    print(f"pages declaring en AND vi     : {both:,}")
    print(f"  missing x-default           : {len(offenders):,}")
    print(f"  missing canonical           : {no_canon:,}")
    if offenders:
        print("\nby area:")
        for area, n in sorted(by_area.items(), key=lambda kv: -kv[1]):
            print(f"  {n:5,d}  {area}")
    if show_list:
        print("\n--- offending paths ---")
        for rel in offenders:
            print(" ", rel)
    else:
        print("\n(run with --list for every path)")


if __name__ == "__main__":
    main()
