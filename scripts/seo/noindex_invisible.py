#!/usr/bin/env python3
"""Add <meta name="robots" content="noindex"> to the pages that are invisible
both ways: unreachable from index.html, not a redirect stub, not listed in
either sitemap, and with no twin at the mirrored path (X <-> vi/X) on disk.

Pages whose twin EXISTS are skipped on purpose: those are the /articles/-
style duplicates, and the right tool there is canonical (already applied by
G1) — noindex + canonical-to-elsewhere is a contradiction Google warns about.

Excludes the tnkb/ meta-refresh stubs (they are correct as-is).

Usage:
  python noindex_invisible.py --root .            # report
  python noindex_invisible.py --root . --write    # apply
"""
import argparse
import html
import os
import re
import urllib.parse

SKIP_DIRS = {".git", "node_modules", "tnkb", "assets", "site", "__pycache__"}
SITEMAPS = ("sitemap.xml", os.path.join("vi", "sitemap.xml"))
LOC = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.I | re.S)
STUB = re.compile(r'<meta[^>]+http-equiv=["\']refresh["\']', re.I)
NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)


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
    return [key(urllib.parse.urlsplit(html.unescape(m.group(1)).strip()).path or "/")
            for m in LOC.finditer(text)]


def twin_exists(root, rel):
    """Mirrored-path twin: strip a leading vi/ to get the EN path, add one to get VI."""
    fwd = rel.replace(os.sep, "/")
    if fwd == "vi" or fwd.startswith("vi/"):
        twin = fwd[3:]
    else:
        twin = "vi/" + fwd
    if not twin:
        return True  # the site root pairs with itself
    return os.path.isfile(os.path.join(root, twin))


def add_noindex(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    if NOINDEX.search(text):
        return False
    meta = '<meta name="robots" content="noindex">'
    m = re.search(r"(<meta[^>]+charset[^>]*>)", text, re.I)
    if m:
        new = text[:m.end()] + "\n" + meta + text[m.end():]
    else:
        m2 = re.search(r"(<head[^>]*>)", text, re.I)
        if not m2:
            return False
        new = text[:m2.end()] + "\n" + meta + text[m2.end():]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--unreachable", default=os.path.join("_tmp", "unreachable.txt"))
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    listed = set()
    for sm in SITEMAPS:
        p = os.path.join(root, sm)
        if os.path.isfile(p):
            listed |= set(read_locs(p))

    with open(os.path.join(root, args.unreachable), encoding="utf-8") as f:
        unreach = []
        for ln in f:
            ln = ln.rstrip("\n")
            if not ln.strip():
                continue
            # file format: "<click-depth>\t<path>"
            unreach.append(ln.split("\t", 1)[1] if "\t" in ln else ln)

    targets = []
    skipped = {"stub": 0, "in-sitemap": 0, "twin-exists": 0, "not-a-page": 0, "canonicalised": 0}
    for rel in unreach:
        rel = rel.replace(os.sep, "/")
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            continue
        head = open(path, encoding="utf-8", errors="replace").read(5000)
        if STUB.search(head):
            skipped["stub"] += 1
            continue
        if key(url_path_of(rel)) in listed:
            skipped["in-sitemap"] += 1
            continue
        if twin_exists(root, rel):
            skipped["twin-exists"] += 1
            continue
        # /articles/ duplicates already canonicalise to /en/articles/ (G1):
        # canonical is the right tool there, and noindex+canonical conflict.
        if rel == "articles" or rel.startswith("articles/"):
            skipped["canonicalised"] += 1
            continue
        # partials/snippets/verification files are not content pages
        if (rel.startswith(("assets/", "theme/", "site/"))
                or re.fullmatch(r"google[a-f0-9]+\.html", os.path.basename(rel))):
            skipped["not-a-page"] += 1
            continue
        targets.append(rel)

    import collections
    bytop = collections.Counter(t.split("/")[0] for t in targets)
    print(f"unreachable pages examined : {len(unreach)}")
    for k in ("stub", "in-sitemap", "twin-exists", "canonicalised", "not-a-page"):
        print(f"  skipped ({k:13s}): {skipped[k]}")
    print(f"NOINDEX targets            : {len(targets)}")
    for k, v in bytop.most_common(10):
        print(f"   {v:5d}  {k}")

    if not args.write:
        print("\n(dry run; --write to apply)")
        return

    done = 0
    for rel in targets:
        if add_noindex(os.path.join(root, rel)):
            done += 1
    print(f"noindex added to {done} pages")


if __name__ == "__main__":
    main()
