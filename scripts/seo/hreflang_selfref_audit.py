# -*- coding: utf-8 -*-
"""
Measure pages that name their twin but not themselves.

The invariant
-------------
Google's hreflang rule is that the annotation set is *identical on every page of
the cluster*, and "each language version must list itself as well as all other
language versions". A page that emits

    <link rel="alternate" hreflang="en" href="/blog/x/">

on `/vi/blog/x/` is saying "the English version of this article is over there".
It is not saying "and this page is the Vietnamese version". The cluster is
one-sided: the EN page lists two members, the VI page lists one, and the two
annotation sets are not identical.

Why no existing verifier sees it
--------------------------------
Every hreflang check in this repo has a denominator built from pages that already
declare the tag it is checking:

  * `xdefault_audit.py`  -> "pages declaring en AND vi" (7,127). A page with only
    `en` is not in the denominator, so it can never be counted as missing
    `x-default` or `canonical`.
  * `hreflang_reciprocal.py` -> edges between pages that have >=1 alternate. The
    edge `en -> /vi/blog/x/` IS reciprocal by its test: each page names the other
    with the correct language. The absent self-tag is not an edge, so there is
    nothing for it to be non-reciprocal about.
  * `canonical_audit.py` -> presence of `<link rel=canonical>`, unrelated.

So this is the same shape as §32/§33/§34: the verifier is correct about what is
present and silent about what is absent. This tool measures absence directly.

What it reports
---------------
For every page carrying at least one `hreflang` alternate:

  complete    : has an alternate for its OWN language resolving to itself
  missing-self: names the twin, but no own-language tag at all
  wrong-self  : has an own-language tag, but it resolves somewhere else

`wrong-self` is a different (worse) defect and is reported, never repaired here.

Usage
-----
    python scripts/seo/hreflang_selfref_audit.py
    python scripts/seo/hreflang_selfref_audit.py --list
    python scripts/seo/hreflang_selfref_audit.py --json out.json
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github"}

LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
HTML_LANG = re.compile(r"<html\b[^>]*>", re.I)
ATTR = re.compile(
    r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))"""
)


def attrs(tag):
    out = {}
    for m in ATTR.finditer(tag):
        key = m.group(1).lower()
        val = m.group(2)
        if val is None:
            val = m.group(3) if m.group(3) is not None else m.group(4)
        out[key] = val or ""
    return out


def page_url(rel):
    """The URL path a file is served at."""
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def norm(href, base):
    """Resolve `href` against `base` (a page URL) to a comparable path key.

    Relative hrefs are the norm here, not the exception: 3,667 pages carry
    `hreflang="en" href="./"`, which means "this directory" -- i.e. the page
    itself. Treating that as an absolute path reported every one of them as
    pointing somewhere else.
    """
    if not href:
        return ""
    resolved = urllib.parse.urljoin(base, href)
    p = urllib.parse.urlsplit(resolved).path
    p = urllib.parse.unquote(p)
    if not p.startswith("/"):
        p = "/" + p
    if p.endswith("/index.html"):
        p = p[: -len("index.html")]
    return p


def walk():
    """Every .html file in the tree, not just directory indexes.

    The first version of this walker yielded only `index.html`, which silently
    dropped all 2,566 generated Pillars articles (they are `ART-*.html` files
    inside a directory). It reported 4,650 pages where the other audits report
    7,212 -- a coverage gap in the measuring tool, which is the exact failure
    mode this file exists to find.
    """
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            if fn.lower().endswith(".html"):
                yield os.path.join(dirpath, fn)


def page_lang(rel, html):
    """Own language: path prefix, cross-checked against <html lang>.

    Returns (lang, disagreement) where disagreement is the declared lang when it
    contradicts the path, else None.
    """
    path_lang = "vi" if rel.startswith("vi/") else "en"
    m = HTML_LANG.search(html)
    declared = None
    if m:
        declared = (attrs(m.group(0)).get("lang") or "").strip().lower()
    if declared:
        declared = declared.split("-")[0]
        if declared in ("en", "vi") and declared != path_lang:
            return path_lang, declared
    return path_lang, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="print every affected path")
    ap.add_argument("--json", metavar="FILE", help="write machine-readable results")
    args = ap.parse_args()

    complete, missing, wrong = [], [], []
    mismatched = []
    total_alt_pages = 0

    for full in walk():
        rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
        try:
            html = open(full, encoding="utf-8", errors="replace").read()
        except OSError:
            continue

        alts = []
        for m in LINK_TAG.finditer(html):
            a = attrs(m.group(0))
            if "alternate" in (a.get("rel") or "").lower().split() and "hreflang" in a:
                alts.append((a["hreflang"].strip().lower(), a.get("href", "")))

        if not alts:
            continue
        total_alt_pages += 1

        own_path = page_url(rel)
        lang, declared = page_lang(rel, html)
        if declared:
            mismatched.append((rel, lang, declared))

        own_tags = [(l, h) for l, h in alts if l == lang]
        if not own_tags:
            missing.append({"path": rel, "lang": lang, "alts": alts, "own": own_path})
        else:
            hits = [h for _, h in own_tags if norm(h, own_path) == norm(own_path, own_path)]
            if hits:
                complete.append(rel)
            else:
                wrong.append({"path": rel, "lang": lang, "own": own_path, "alts": own_tags})

    print("pages carrying >=1 hreflang alternate : %d" % total_alt_pages)
    print("  complete  (own-language tag -> self) : %d" % len(complete))
    print("  MISSING-SELF (no own-language tag)   : %d" % len(missing))
    print("  WRONG-SELF   (own tag -> elsewhere)  : %d" % len(wrong))
    if mismatched:
        print("  <html lang> contradicts path        : %d" % len(mismatched))
    print()

    if missing:
        buckets = Counter(
            ("vi/" if r["path"].startswith("vi/") else "root")
            + "/"
            + ("/".join(r["path"].split("/")[:2]) if r["path"].count("/") >= 1 else "")
            for r in missing
        )
        print("missing-self by top-level bucket:")
        for k, v in buckets.most_common():
            print("   %-40s %5d" % (k, v))
        print()
        langcount = Counter(r["lang"] for r in missing)
        print("missing-self by own language: %s" % dict(langcount))
        print()
        shape = Counter(len(r["alts"]) for r in missing)
        print("missing-self by alternate count: %s" % dict(sorted(shape.items())))
        print()

    if wrong:
        print("wrong-self (report only, not repaired):")
        for r in wrong[:20]:
            print("   %s  own=%s  tags=%s" % (r["path"], r["own"], r["alts"]))
        print()

    if args.list and missing:
        print("--- every missing-self path ---")
        for r in sorted(missing, key=lambda x: x["path"]):
            print("   %s  [%s]  alts=%s" % (r["path"], r["lang"], r["alts"]))

    if args.json:
        json.dump(
            {
                "total_alt_pages": total_alt_pages,
                "complete": len(complete),
                "missing": missing,
                "wrong": wrong,
                "lang_mismatch": mismatched,
            },
            open(args.json, "w", encoding="utf-8"),
            indent=1,
        )
        print("wrote %s" % args.json)

    return 0


if __name__ == "__main__":
    sys.exit(main())
