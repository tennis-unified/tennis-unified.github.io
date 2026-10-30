#!/usr/bin/env python3
"""
orphan_audit.py — count indexable pages that nothing links to.

A page is "indexable" under the same definition `sitemap_coverage.py` uses:
self-canonical, i.e. its own URL is the one it declares as canonical. Those are
exactly the pages that must be reachable, because they are the ones asking to be
crawled.

An orphan is an indexable page with ZERO inbound internal links from any other
page in the tree. This is the complement of every other audit in this directory:
`canonical_audit`, `hreflang_reciprocal`, `xdefault_audit` and `dead_links` all
check the consistency of what is PRESENT. None of them can see a page that is
correct and unreachable, because there is nothing there to check.

That gap is what made the Pillars class invisible for three passes: 2,558 static
pages were generated, canonicalised, given a full hreflang cluster and added to
both sitemaps — and nothing linked to 1,279 of them, because the catalogs still
pointed at the client-side reader.

Link normalisation (both sides reduced to the same key):
  - strip query and fragment
  - percent-decode
  - strip a trailing "index.html" so `/dir/` and `/dir/index.html` collide
  - leading "/" removed, so a root-relative href and a repo-relative path collide
  - relative hrefs are resolved against the linking page's own URL

Self-links do not count: a page that only links to itself is still an orphan.

Usage:
  python scripts/seo/orphan_audit.py --root .              # summary by top dir
  python scripts/seo/orphan_audit.py --root . --paths      # list the orphans
  python scripts/seo/orphan_audit.py --root . --top 30
"""
import argparse
import collections
import os
import re
import urllib.parse

SKIP_DIRS = {".git", "node_modules", "__pycache__", "sources", ".workbuddy-ai"}

HREF = re.compile(r'href\s*=\s*"([^"]*)"', re.I)
LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
ATTR = re.compile(r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)')""")

# Navigation edges are <a href> ONLY. A first version of this audit scanned every
# href in the file, which counted each page's own <link rel="canonical"> and its
# twin's <link rel="alternate"> as inbound links — so 2,566 real orphans collapsed
# to 28 fake-resolved ones, and every page appeared to link to itself. Head
# metadata describes a page; it does not route to it.
A_TAG = re.compile(r"<a\b[^>]*>", re.I)
A_HREF = re.compile(r"""\bhref\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)


def anchor_hrefs(text):
    for tag in A_TAG.findall(text):
        m = A_HREF.search(tag)
        if m:
            yield m.group(1) if m.group(1) is not None else m.group(2)


def key(path):
    """Reduce a URL path to a comparable key."""
    p = urllib.parse.unquote(path.split("#")[0].split("?")[0])
    if p.endswith("/index.html"):
        p = p[: -len("index.html")]
    p = p.lstrip("/")
    return p


def rel_key(relpath):
    return key(relpath.replace(os.sep, "/"))


def canonical_of(text):
    for tag in LINK_TAG.findall(text):
        attrs = {}
        for k, v1, v2 in ATTR.findall(tag):
            attrs[k.lower()] = v1 or v2
        if "canonical" in (attrs.get("rel", "") or "").lower():
            return attrs.get("href", "")
    return None


def is_self(canon, selfkey):
    if not canon:
        return False
    return key(canon) == selfkey


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--paths", action="store_true")
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    root = args.root
    pages = []       # (relpath, selfkey)
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.lower().endswith(".html"):
                continue
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            pages.append((rel, rel_key(rel)))

    indexable = {}
    texts = {}
    for rel, k in pages:
        try:
            with open(os.path.join(root, rel), "r", encoding="utf-8", errors="replace") as fh:
                t = fh.read()
        except OSError:
            continue
        texts[rel] = t
        c = canonical_of(t)
        if is_self(c, k):
            indexable[k] = rel

    inbound = collections.Counter()
    for rel, selfkey in pages:
        t = texts.get(rel)
        if not t:
            continue
        base = "/" + rel.replace(os.sep, "/")
        for href in anchor_hrefs(t):
            if not href or href.startswith(("mailto:", "javascript:", "tel:", "data:")):
                continue
            h = urllib.parse.urlsplit(href)
            if h.scheme in ("http", "https") and h.netloc not in ("tenniskb.github.io", "tennis-unified.github.io"):
                continue
            target = h.path
            if not target:
                continue
            if not target.startswith("/"):
                target = urllib.parse.urljoin(base, target)
            k = key(target)
            if k and k != selfkey:
                inbound[k] += 1

    orphans = sorted(k for k in indexable if inbound[k] == 0)
    print(f"html files scanned : {len(pages)}")
    print(f"self-canonical     : {len(indexable)}")
    print(f"orphans (0 inbound): {len(orphans)}")

    bydir = collections.Counter()
    for k in orphans:
        top = k.split("/")[0] if "/" in k else "(root files)"
        if k.startswith("vi/") and k.count("/") >= 1:
            parts = k.split("/")
            top = "/".join(parts[:2]) if len(parts) > 2 else "vi/ (files)"
        bydir[top] += 1
    print(f"\ntop {args.top} directories holding orphans:")
    for d, n in bydir.most_common(args.top):
        print(f"  {n:6d}  {d}")

    if args.paths:
        print("\norphan paths:")
        for k in orphans:
            print("  " + k)


if __name__ == "__main__":
    main()
