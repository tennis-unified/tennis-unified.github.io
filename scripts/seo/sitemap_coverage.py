#!/usr/bin/env python3
"""Measure sitemap coverage of pages that are actually indexable.

A page is indexable only if it is self-canonical: its own URL is what it
declares as canonical. Pages canonicalised elsewhere (e.g. /articles/ ->
/en/articles/) must NOT be in the sitemap; that is correct behaviour, not a gap.

Reports:
  1. self-canonical pages missing from both sitemaps, grouped by directory
  2. canonical targets that no sitemap lists (the sharper class: the canonical
     destination itself is unlisted, so the whole cluster is invisible)
  3. redirect stubs / non-canonical pages that ARE listed (noise to remove)

Usage:
  python sitemap_coverage.py --root . [--top 25] [--dirs vi en blog]
  python sitemap_coverage.py --root . --paths      # print the actual paths
"""
import argparse
import collections
import html
import os
import re
import sys
import urllib.parse

SKIP_DIRS = {".git", "node_modules", "tnkb", "assets", "site", "__pycache__"}

# attribute-order agnostic: <link rel="canonical" href="..."> or href before rel
LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
ATTR = re.compile(r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))""")
REFRESH = re.compile(
    r"""<meta\b[^>]*http-equiv\s*=\s*["']?refresh["']?[^>]*content\s*=\s*["']\s*\d+\s*;\s*url\s*=\s*([^"'>\s]+)""",
    re.I,
)
LOC = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.I | re.S)


def attrs_of(tag):
    out = {}
    for m in ATTR.finditer(tag):
        val = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        out[m.group(1).lower()] = html.unescape(val or "")
    return out


def url_path_of(rel):
    """Map a repo-relative file path to its served URL path."""
    rel = rel.replace(os.sep, "/")
    if rel.endswith("/index.html"):
        p = "/" + rel[: -len("index.html")]
    elif rel == "index.html":
        p = "/"
    else:
        p = "/" + rel
    return re.sub(r"/{2,}", "/", p)


def norm(p):
    """Normalise a URL path for comparison: decode, drop query/fragment, ensure trailing slash on dirs."""
    p = urllib.parse.unquote(p.split("#")[0].split("?")[0])
    if not p.startswith("/"):
        p = "/" + p
    return re.sub(r"/{2,}", "/", p)


def load_sitemap(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    urls = set()
    for raw in LOC.findall(text):
        u = html.unescape(raw.strip())
        sp = urllib.parse.urlsplit(u)
        urls.add(norm(sp.path or "/"))
    return urls


def walk_html(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                full = os.path.join(dirpath, fn)
                yield os.path.relpath(full, root)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--dirs", nargs="*", default=None,
                    help="restrict the missing-path listing to these prefixes")
    ap.add_argument("--paths", action="store_true", help="print missing paths")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    sm_files = []
    for cand in ("sitemap.xml", os.path.join("vi", "sitemap.xml")):
        full = os.path.join(root, cand)
        if os.path.exists(full):
            sm_files.append(full)
    if not sm_files:
        sys.exit("no sitemap.xml found")

    listed = set()
    for f in sm_files:
        got = load_sitemap(f)
        print(f"sitemap {os.path.relpath(f, root):<22} locs={len(got)}")
        listed |= got
    print(f"union of sitemap URLs: {len(listed)}\n")

    self_canon = []          # (page_path, canonical_path)
    away = []                # canonicalised elsewhere
    no_canon = []
    stubs = []               # meta refresh pages
    canon_targets = collections.Counter()

    for rel in walk_html(root):
        own = norm(url_path_of(rel))
        try:
            with open(os.path.join(root, rel), encoding="utf-8", errors="replace") as f:
                head = f.read(200000)
        except OSError:
            continue

        canon = None
        for tag in LINK_TAG.findall(head):
            a = attrs_of(tag)
            rels = a.get("rel", "").lower().split()
            if "canonical" in rels and a.get("href"):
                canon = norm(a["href"])
                break

        if REFRESH.search(head):
            stubs.append(own)

        if canon is None:
            no_canon.append(own)
        elif canon == own:
            self_canon.append((rel, own))
        else:
            away.append((rel, own, canon))
            canon_targets[canon] += 1

    print(f"pages scanned:            {len(self_canon) + len(away) + len(no_canon)}")
    print(f"  self-canonical:         {len(self_canon)}")
    print(f"  canonicalised away:     {len(away)}")
    print(f"  no canonical tag:       {len(no_canon)}")
    print(f"  meta-refresh stubs:     {len(stubs)}\n")

    # --- 1. self-canonical pages absent from both sitemaps
    missing = [(rel, p) for rel, p in self_canon if p not in listed]
    print(f"== self-canonical pages NOT in either sitemap: {len(missing)}")
    buckets = collections.Counter()
    for rel, p in missing:
        parts = [x for x in p.strip("/").split("/") if x]
        key = "/".join(parts[:2]) if len(parts) >= 2 else (parts[0] if parts else "(root)")
        buckets[key] += 1
    for key, n in buckets.most_common(args.top):
        print(f"   {n:>6}  {key}")
    if args.paths:
        print()
        for rel, p in missing:
            if args.dirs and not any(p.startswith("/" + d.strip("/")) for d in args.dirs):
                continue
            print(f"   {p}")

    # --- 2. canonical targets no sitemap lists
    dead_targets = {t: n for t, n in canon_targets.items() if t not in listed}
    tot_pages = sum(dead_targets.values())
    print(f"\n== canonical targets absent from both sitemaps: {len(dead_targets)} "
          f"(pages pointing at them: {tot_pages})")
    for t, n in sorted(dead_targets.items(), key=lambda kv: -kv[1])[: args.top]:
        print(f"   {n:>5} pages -> {t}")

    # --- 3. pages that are listed but should not be
    away_set = {p for _, p, _ in away}
    stub_set = set(stubs)
    listed_away = sorted(p for p in listed if p in away_set)
    listed_stub = sorted(p for p in listed if p in stub_set)
    print(f"\n== listed but canonicalised elsewhere (should be dropped): {len(listed_away)}")
    for p in listed_away[: args.top]:
        print(f"   {p}")
    print(f"== listed but a meta-refresh stub: {len(listed_stub)}")
    for p in listed_stub[: args.top]:
        print(f"   {p}")

    # --- sanity: listed URLs that match no page at all
    known = {p for _, p in self_canon} | away_set | set(no_canon)
    ghost = sorted(p for p in listed if p not in known)
    print(f"\n== listed URLs with no matching page on disk: {len(ghost)}")
    for p in ghost[: args.top]:
        print(f"   {p}")


if __name__ == "__main__":
    main()
