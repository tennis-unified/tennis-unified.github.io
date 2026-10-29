#!/usr/bin/env python3
"""
canonical_lang_audit.py — flag canonicals that cross a language boundary.

WHY THIS EXISTS
---------------
`canonical_audit.py` checks three things: duplicate canonical tags, absolute
canonicals, and dangling root-relative canonicals. None of them looks at whether the
canonical target is even in the same language. So a page can declare a translation of
itself as the authoritative URL and every existing check stays green — which is exactly
what `books/12_modern_tennis_mechanics_deep_dive_en.html` did (an English book whose
canonical pointed at `/vi/books/..._vi.html`, the Vietnamese edition). Google reads that
as "the Vietnamese page is the canonical version of this English content".

The invariant: a canonical should resolve to a page with the same `<html lang>`. The
legitimate exception is a redirect stub, whose canonical deliberately points at whatever
it redirects to, in whatever language that happens to be.

Run:
  python scripts/seo/canonical_lang_audit.py            # report
  python scripts/seo/canonical_lang_audit.py --explain  # list every hit
"""
import argparse
import os
import posixpath
import re
from urllib.parse import unquote

SKIP_DIRS = {".git", "node_modules", "_tmp", ".workbuddy-ai"}
CAN_RE = re.compile(
    r'<link\b(?=[^>]*\srel\s*=\s*["\']?canonical\b)(?=[^>]*\shref\s*=\s*"([^"]*)")[^>]*>', re.I
)
LANG_RE = re.compile(r'<html[^>]*\blang="([^"]*)"', re.I)
# A redirect stub legitimately canonicalises to a page in another language.
STUB_RE = re.compile(r'<meta[^>]*http-equiv\s*=\s*["\']?refresh["\']?', re.I)


def key(rel):
    p = posixpath.normpath("/" + rel.strip("/"))
    if p.endswith("/index.html"):
        base = p[: -len("/index.html")]
        return base if base.endswith("/") else base + "/"
    return p


def lang_of(text):
    m = LANG_RE.search(text)
    return m.group(1).lower().split("-")[0] if m else None


def walk(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if not f.lower().endswith((".html", ".htm")):
                continue
            full = os.path.join(dp, f)
            rel = os.path.relpath(full, root).replace("\\", "/")
            yield full, rel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--explain", action="store_true")
    args = ap.parse_args()

    pages, stubs = {}, set()
    for full, rel in walk(args.root):
        text = open(full, "rb").read().decode("utf-8", "replace")
        pages[key(rel)] = (rel, lang_of(text))
        if STUB_RE.search(text):
            stubs.add(key(rel))

    cross, stubbed, resolved = [], 0, 0
    for full, rel in walk(args.root):
        text = open(full, "rb").read().decode("utf-8", "replace")
        m = CAN_RE.search(text)
        if not m:
            continue
        href = unquote(m.group(1)).split("#")[0].split("?")[0]
        if href.lower().startswith(("http://", "https://")):
            continue
        if href.startswith("/"):
            tgt = key(href)
        else:
            joined = posixpath.join(posixpath.dirname("/" + rel), href)
            tgt = key(posixpath.normpath(joined))
        if tgt not in pages:
            continue
        resolved += 1
        sl = pages[key(rel)][1]
        tl = pages[tgt][1]
        if not (sl and tl) or sl == tl:
            continue
        if key(rel) in stubs:
            stubbed += 1
            continue
        cross.append((rel, sl, tgt, tl))

    print(f"canonicals resolved to an existing page : {resolved:,}")
    print(f"  exempt: redirect stub                  : {stubbed}")
    print(f"cross-language canonicals (defects)     : {len(cross)}")
    if args.explain:
        for rel, sl, tgt, tl in cross:
            print(f"  [{sl} -> {tl}]  {rel}\n                -> {tgt}")
    return 1 if cross else 0


if __name__ == "__main__":
    raise SystemExit(main())
