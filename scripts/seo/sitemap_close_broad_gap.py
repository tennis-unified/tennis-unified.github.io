#!/usr/bin/env python3
"""Close the *broad* sitemap gap: add self-canonical pages that no sitemap lists.

This is the conservative companion to sitemap_gap_fix.py (which only handled the
provable article-cluster defects). Here we add every self-canonical page that is
absent from BOTH sitemaps, EXCEPT the deliberately-kept legacy archive under
`tnkb/` (the reachability audit treats it as an archive; 958 redirect stubs
depend on it). VI-language pages go to vi/sitemap.xml, everything else to
sitemap.xml.

Also: handbook pages currently carry NO canonical tag, so they are invisible to
the self-canonical filter. We add a self-canonical link to each en/handbooks
page first (mechanical, idempotent), which then lets them flow into the sitemap.

EN pages -> sitemap.xml ; VI pages (path starts with /vi/) -> vi/sitemap.xml.

Usage:
  python sitemap_close_broad_gap.py --root .            # report
  python sitemap_close_broad_gap.py --root . --write    # apply + verify
"""
import argparse
import gzip
import html
import os
import re
import sys
import xml.etree.ElementTree as ET
import urllib.parse

SKIP_DIRS = {".git", "node_modules", "tnkb", "assets", "site", "__pycache__"}
# Legacy archive we deliberately keep out of the sitemap sweep (the on-disk
# directory is `tenniskb/`; the redirect stubs added in 8db8945fd4a point into it):
EXCLUDE_PREFIXES = ("/tenniskb/",)
HOST = "https://tenniskb.github.io"
SITEMAP = "sitemap.xml"
VI_SITEMAP = os.path.join("vi", "sitemap.xml")

LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
ATTR = re.compile(
    r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))"""
)
LOC = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.I | re.S)


def attrs_of(tag):
    out = {}
    for m in ATTR.finditer(tag):
        val = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4))
        out[m.group(1).lower()] = html.unescape(val or "")
    return out


def canonical_of(path):
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
        p = "/" + rel[:-len("index.html")]
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


def url_for(path_key):
    enc = urllib.parse.quote(path_key, safe="/()'!*._~-")
    return HOST + enc + ("/" if not enc.endswith("/") else "")


def entry(path_key, changefreq="monthly", priority="0.6"):
    return (
        "  <url>\n"
        f"    <loc>{html.escape(url_for(path_key))}</loc>\n"
        f"    <changefreq>{changefreq}</changefreq>\n"
        f"    <priority>{priority}</priority>\n"
        "  </url>\n"
    )


def add_canonical(path, own_key):
    text = open(path, encoding="utf-8", errors="replace").read()
    if re.search(r'<link\b[^>]*rel="[^"]*canonical', text, re.I):
        return False
    canon = f'<link rel="canonical" href="{html.escape(url_for(own_key))}">'
    # insert right after <head ...> or after charset meta
    m = re.search(r"(<head[^>]*>)", text, re.I)
    if m:
        new = text[:m.end()] + "\n    " + canon + text[m.end():]
    else:
        new = canon + "\n" + text
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    sm = os.path.join(root, SITEMAP)
    vsm = os.path.join(root, VI_SITEMAP)

    sm_locs = read_locs(sm)
    vsm_locs = read_locs(vsm)
    listed = {key(p) for p in sm_locs} | {key(p) for p in vsm_locs}

    # 1. handbooks: add self-canonical so they become eligible
    hb_added = 0
    for rel in walk_pages(root):
        rel = rel.replace(os.sep, "/")
        if not rel.startswith("en/handbooks/"):
            continue
        own = key(url_path_of(rel))
        if canonical_of(os.path.join(root, rel)) is None:
            if args.write:
                if add_canonical(os.path.join(root, rel), own):
                    hb_added += 1
            else:
                hb_added += 1
    print(f"handbook pages needing canonical: {hb_added}"
          + (" (added)" if args.write else " (dry run)"))

    # 2. build self-canonical index, excluding legacy archive
    selfcanon = {}  # key -> is_vi
    for rel in walk_pages(root):
        own = key(url_path_of(rel))
        if any(own.startswith(p) for p in EXCLUDE_PREFIXES):
            continue
        try:
            c = canonical_of(os.path.join(root, rel))
        except OSError:
            continue
        if c is None:
            continue
        ck = key(c)
        if ck != own:
            continue  # not self-canonical
        if own in listed:
            continue
        selfcanon[own] = own.startswith("/vi/")

    en_add = sorted(k for k, vi in selfcanon.items() if not vi)
    vi_add = sorted(k for k, vi in selfcanon.items() if vi)
    print(f"self-canonical pages missing from sitemaps (excl. tnkb/): "
          f"{len(selfcanon)}  (en={len(en_add)}, vi={len(vi_add)})")

    if not args.write:
        print("\n(dry run; --write to apply)")
        return

    # 3. append
    for path, add in ((sm, en_add), (vsm, vi_add)):
        text = open(path, encoding="utf-8").read()
        chunk = "".join(entry(k) for k in add)
        text = text.replace("</urlset>", chunk + "</urlset>")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        # regen gz + verify
        with open(path, "rb") as f:
            data = f.read()
        with gzip.GzipFile(path + ".gz", "wb", mtime=0) as gz:
            gz.write(data)
        ET.parse(path)
        new_locs = read_locs(path)
        dupes = len(new_locs) - len(set(new_locs))
        print(f"  {os.path.relpath(path, root)}: +{len(add)} locs, "
              f"total={len(new_locs)}, dupes={dupes}, gz in sync={gzip.open(path+'.gz','rb').read()==data}")
        assert dupes == 0
    print("VERIFY OK")


if __name__ == "__main__":
    main()
