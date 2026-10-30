#!/usr/bin/env python3
"""Close the sitemap gaps that are provable, and only those.

Measured 2026-10-29 on the mirrored tree:

  sitemap.xml       6,917 <loc>    robots.txt -> sitemap.xml
  vi/sitemap.xml    1,754 <loc>    referenced by nothing
  root sitemap is a plain <urlset>, not a <sitemapindex>

Three defects, each provable from the tree alone:

  A. ORPHAN   vi/sitemap.xml is reachable only by guessing its path. A crawler
              following robots.txt never learns it exists, so 1,754 VI URLs are
              discoverable by link-crawl only. robots.txt supports repeated
              Sitemap: lines; adding the second one costs nothing.

  B. HALF-MIGRATION
              G1 (commit 77ad7709) made /articles/<slug>/ canonicalise to
              /en/articles/<slug>/ and removed the 201 /articles/ URLs from the
              sitemap. That was right. But only 56 of the 205 EN destinations and
              56 of the 262 VI destinations were ever added, so 355 pages that
              are now the *canonical* copy of an article are unlisted. The
              duplicates are gone from the sitemap and the originals are not
              there either.

  C. STALE    A <loc> whose page declares a different canonical. Listing a URL
              that says "I am not canonical" asks the crawler to fetch and then
              discard it. Removed -- but only where the page's own canonical tag
              proves the point. A page with no canonical tag is *not* touched:
              whether it should have one is a content decision, not a sitemap one.

Explicitly NOT done: adding the other ~1,240 self-canonical pages that no
sitemap lists (sources/tennis-wiki 333, tenniskb/en 98, en/reference 84, ...).
"Never listed" is indistinguishable from "deliberately excluded" without the
owner's intent, so it is recorded, not swept. Only the article cluster is
touched, because there the removal of the source proves the intent to list the
destination.

Usage
  python sitemap_gap_fix.py --root .                 # report
  python sitemap_gap_fix.py --root . --write         # apply + verify
  python sitemap_gap_fix.py --root . --add-prefix en/articles vi/articles
"""
import argparse
import gzip
import html
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET

SKIP_DIRS = {".git", "node_modules", "tnkb", "assets", "site", "__pycache__"}
SITEMAP = "sitemap.xml"
VI_SITEMAP = os.path.join("vi", "sitemap.xml")
ROBOTS = "robots.txt"
HOST = "https://tenniskb.github.io"

DEFAULT_ADD = ("en/articles", "vi/articles")

LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
ATTR = re.compile(
    r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))"""
)
LOC = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.I | re.S)
ROBOTS_SITEMAP = re.compile(r"^\s*Sitemap:\s*(\S+)\s*$", re.I | re.M)


def attrs_of(tag):
    out = {}
    for m in ATTR.finditer(tag):
        val = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        out[m.group(1).lower()] = html.unescape(val or "")
    return out


def canonical_of(path):
    """Return the page's declared canonical URL path, or None."""
    with open(path, encoding="utf-8", errors="replace") as f:
        head = f.read(200000)
    for tag in LINK_TAG.findall(head):
        a = attrs_of(tag)
        if "canonical" in a.get("rel", "").lower().split() and a.get("href"):
            return urllib.parse.unquote(urllib.parse.urlsplit(a["href"]).path)
    return None


def url_path_of(rel):
    rel = rel.replace(os.sep, "/")
    if rel.endswith("/index.html"):
        p = "/" + rel[: -len("index.html")]
    elif rel == "index.html":
        p = "/"
    else:
        p = "/" + rel
    return re.sub(r"/{2,}", "/", p)


def norm(p):
    p = urllib.parse.unquote(p.split("#")[0].split("?")[0])
    if not p.startswith("/"):
        p = "/" + p
    return re.sub(r"/{2,}", "/", p)


def key(p):
    return norm(p).rstrip("/") or "/"


def read_locs(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    out = []
    for raw in LOC.findall(text):
        u = html.unescape(raw.strip())
        out.append(urllib.parse.urlsplit(u).path or "/")
    return out


def walk_pages(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.relpath(os.path.join(dirpath, fn), root)


def build_index(root):
    """own_url_key -> canonical_key (None when the page declares no canonical)."""
    idx = {}
    for rel in walk_pages(root):
        own = key(url_path_of(rel))
        try:
            c = canonical_of(os.path.join(root, rel))
        except OSError:
            continue
        idx[own] = key(c) if c else None
    return idx


def url_for(path_key):
    enc = urllib.parse.quote(path_key, safe="/()'!*._~-")
    return HOST + enc + ("/" if not enc.endswith("/") else "")


def entry(path_key, changefreq="monthly", priority="0.8"):
    return (
        "  <url>\n"
        f"    <loc>{html.escape(url_for(path_key))}</loc>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def regen_gz(xml_path):
    with open(xml_path, "rb") as f:
        data = f.read()
    with gzip.GzipFile(xml_path + ".gz", "wb", mtime=0) as gz:
        gz.write(data)


def gz_in_sync(xml_path):
    try:
        with gzip.open(xml_path + ".gz", "rb") as f:
            return f.read() == open(xml_path, "rb").read()
    except OSError:
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--add-prefix", nargs="*", default=list(DEFAULT_ADD))
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    sm = os.path.join(root, SITEMAP)
    vsm = os.path.join(root, VI_SITEMAP)
    robots = os.path.join(root, ROBOTS)

    for p in (sm, vsm):
        if not os.path.exists(p):
            sys.exit(f"missing {p}")

    idx = build_index(root)
    print(f"pages indexed: {len(idx)}")

    sm_locs = read_locs(sm)
    vsm_locs = read_locs(vsm)
    listed = {key(p) for p in sm_locs} | {key(p) for p in vsm_locs}
    print(f"sitemap locs: {SITEMAP}={len(sm_locs)}  {VI_SITEMAP}={len(vsm_locs)}")

    # ---- A. robots.txt must name every sitemap that exists
    with open(robots, encoding="utf-8") as f:
        rtxt = f.read()
    declared = {
        norm(urllib.parse.urlsplit(m.group(1)).path or "/")
        for m in ROBOTS_SITEMAP.finditer(rtxt)
    }
    want = {norm("/" + SITEMAP.replace(os.sep, "/")), norm("/" + VI_SITEMAP.replace(os.sep, "/"))}
    missing_decl = sorted(want - declared)
    print(f"\nA. robots.txt declares {len(declared)} sitemap(s); missing {len(missing_decl)}: "
          f"{missing_decl or '-'}")

    # ---- C. locs whose page declares a different canonical
    stale = []
    for loc in sm_locs + vsm_locs:
        k = key(loc)
        if k in idx and idx[k] is not None and idx[k] != k:
            stale.append(k)
    stale = sorted(set(stale))
    print(f"C. locs whose page canonicalises elsewhere: {len(stale)}")
    for s in stale:
        print(f"     {s}  ->  {idx[s]}")

    # ---- B. self-canonical pages under the add-prefixes that are unlisted
    add = []
    for k, c in idx.items():
        if c is None or c != k:
            continue
        if k in listed:
            continue
        if any(k.startswith("/" + p.strip("/") + "/") for p in args.add_prefix):
            add.append(k)
    add.sort()
    print(f"B. self-canonical pages to add under {list(args.add_prefix)}: {len(add)}")

    if not args.write:
        print("\n(dry run; --write to apply)")
        return

    # --- apply A
    if missing_decl:
        lines = [ln for ln in rtxt.splitlines() if ln.strip()]
        for p in missing_decl:
            lines.append(f"Sitemap: {HOST}{p}")
        new_robots = "\n".join(lines) + "\n"
        with open(robots, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_robots)
        print(f"  robots.txt: added {len(missing_decl)} directive(s)")

    # --- apply C + B to sitemap.xml only (article cluster lives there)
    text = open(sm, encoding="utf-8").read()
    removed = 0
    if stale:
        def drop(m):
            nonlocal removed
            body = m.group(0)
            lm = re.search(r"<loc>\s*(.*?)\s*</loc>", body, re.S)
            if lm:
                raw = html.unescape(lm.group(1).strip())
                if key(urllib.parse.urlsplit(raw).path or "/") in set(stale):
                    removed += 1
                    return ""
            return body
        text = re.sub(r"[ \t]*<url>.*?</url>\n?", drop, text, flags=re.S)
    print(f"  {SITEMAP}: removed {removed} stale url block(s)")

    if add:
        chunk = "".join(entry(k) for k in add)
        text = text.replace("</urlset>", chunk + "</urlset>")
    print(f"  {SITEMAP}: appended {len(add)} url block(s)")

    with open(sm, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # --- verify
    ok = True
    for p in (sm, vsm):
        try:
            ET.parse(p)
        except ET.ParseError as e:
            print(f"  !! {p} does not parse: {e}")
            ok = False
    new_locs = read_locs(sm)
    dupes = len(new_locs) - len(set(new_locs))
    if dupes:
        print(f"  !! {SITEMAP} has {dupes} duplicate loc(s)")
        ok = False
    expected = len(sm_locs) - removed + len(add)
    if len(new_locs) != expected:
        print(f"  !! {SITEMAP} loc count {len(new_locs)} != expected {expected}")
        ok = False
    regen_gz(sm)
    if not gz_in_sync(sm):
        print("  !! .gz out of sync")
        ok = False
    print(f"  {SITEMAP}: {len(sm_locs)} -> {len(new_locs)} locs, dupes={dupes}, gz in sync")
    print("VERIFY", "OK" if ok else "FAILED")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
