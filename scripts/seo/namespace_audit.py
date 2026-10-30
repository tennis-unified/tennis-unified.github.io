#!/usr/bin/env python3
"""Measure which namespace the site itself treats as canonical.

The tree carries parallel copies of the same sections under several prefixes:

    /system/            /en/system/          /vi/system/      /tenniskb/system/
    /handbook/01-.../   /en/chapter/01-.../  /vi/chuong/...   /tenniskb/en/chapter/...

All of them are self-canonical and none of them carries hreflang to its twin, so
every existing check passes: `canonical_audit` sees no defect, `hreflang_*` sees
no pair to compare. The duplication is invisible to the verifier stack because
each copy is individually well-formed.

That leaves one question that a verifier cannot answer and a crawler can: which
copy does the site itself link to? Inbound internal links are the closest thing
to a declaration of intent that exists in a static tree. This tool counts them.

For every directory that exists under both a root path and an `en/` path it
reports, per side: inbound internal links, inbound from nav/landing pages,
whether it is in a sitemap, whether it declares hreflang, and body word count.
Then it says which side wins on inbound links.

Read-only. It changes nothing -- the point is to replace "we don't know which
namespace is canonical" with a number.

Usage
  python namespace_audit.py --root . [--top 40] [--csv out.csv]
"""
import argparse
import csv
import html
import os
import re
import sys
import urllib.parse
from collections import Counter, defaultdict

SKIP_DIRS = {".git", "node_modules", "tnkb", "assets", "site", "__pycache__"}

HREF = re.compile(r"""<a\b[^>]*?\bhref\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))""", re.I)
LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
ATTR = re.compile(r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))""")
LOC = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.I | re.S)
TAG = re.compile(r"<[^>]+>")


def attrs_of(tag):
    out = {}
    for m in ATTR.finditer(tag):
        v = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        out[m.group(1).lower()] = html.unescape(v or "")
    return out


def key(p):
    p = urllib.parse.unquote(p.split("#")[0].split("?")[0])
    if not p.startswith("/"):
        p = "/" + p
    return re.sub(r"/{2,}", "/", p).rstrip("/") or "/"


def dir_key(rel):
    """Repo-relative directory -> URL path key (always a directory, no trailing slash)."""
    rel = rel.replace(os.sep, "/")
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    elif rel == "index.html":
        rel = ""
    return key("/" + rel)


def load_sitemap(root):
    listed = set()
    for cand in ("sitemap.xml", os.path.join("vi", "sitemap.xml")):
        p = os.path.join(root, cand)
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8", errors="replace") as f:
            t = f.read()
        for raw in LOC.findall(t):
            listed.add(key(urllib.parse.urlsplit(html.unescape(raw.strip())).path))
    return listed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--csv")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    # ---- enumerate directories that hold an index.html, and detect twins
    dirs = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        if "index.html" in filenames:
            rel = os.path.relpath(dirpath, root)
            dirs.add("" if rel == "." else rel.replace(os.sep, "/"))

    root_side = {d for d in dirs if d and not d.startswith(("en/", "vi/", "tenniskb/"))}
    en_side = {d[len("en/"):] for d in dirs if d.startswith("en/")}
    twins = sorted(root_side & en_side)
    print(f"directories with an index page : {len(dirs)}")
    print(f"  root namespace               : {len(root_side)}")
    print(f"  en/ namespace                : {len(en_side)}")
    print(f"  root dirs with an en/ twin   : {len(twins)}\n")

    twin_paths = set()
    for d in twins:
        twin_paths.add(key("/" + d))
        twin_paths.add(key("/en/" + d))

    # ---- one pass over the tree: count inbound links to twin paths
    inbound = Counter()
    inbound_from_nav = Counter()
    words = {}
    hreflang = {}
    canonical = {}

    nav_re = re.compile(r"mm-top|md-tabs|tu-topnav|site-nav|navbar", re.I)

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            fp = os.path.join(dirpath, fn)
            rel = os.path.relpath(fp, root).replace(os.sep, "/")
            try:
                with open(fp, encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except OSError:
                continue

            own = dir_key(rel)

            # per-page metadata (only needed for twin pages)
            if own in twin_paths:
                canon = None
                alts = []
                for tag in LINK_TAG.findall(text):
                    a = attrs_of(tag)
                    rels = a.get("rel", "").lower().split()
                    if "canonical" in rels and a.get("href"):
                        canon = key(a["href"])
                    if "alternate" in rels and a.get("hreflang"):
                        alts.append(a["hreflang"].lower())
                canonical[own] = canon
                hreflang[own] = sorted(set(alts))
                body = TAG.sub(" ", text)
                words[own] = len(body.split())

            # inbound links: only resolve hrefs that could hit a twin
            is_nav = bool(nav_re.search(text[:20000]))
            for m in HREF.finditer(text):
                raw = m.group(1) if m.group(1) is not None else (
                    m.group(2) if m.group(2) is not None else m.group(3)
                )
                if not raw:
                    continue
                raw = html.unescape(raw.strip())
                if raw.startswith(("http://", "https://", "mailto:", "tel:", "javascript:", "#")):
                    continue
                if not raw.startswith("/"):
                    base = os.path.dirname(rel)
                    raw = "/" + (base + "/" + raw if base else raw)
                tgt = key(raw)
                if tgt in twin_paths:
                    inbound[tgt] += 1
                    if is_nav:
                        inbound_from_nav[tgt] += 1

    listed = load_sitemap(root)

    # ---- per twin pair: compare
    rows = []
    for d in twins:
        r, e = key("/" + d), key("/en/" + d)
        rows.append({
            "dir": d,
            "root_in": inbound.get(r, 0),
            "en_in": inbound.get(e, 0),
            "root_nav": inbound_from_nav.get(r, 0),
            "en_nav": inbound_from_nav.get(e, 0),
            "root_sm": r in listed,
            "en_sm": e in listed,
            "root_hl": ",".join(hreflang.get(r, [])) or "-",
            "en_hl": ",".join(hreflang.get(e, [])) or "-",
            "root_canon_self": canonical.get(r) == r,
            "en_canon_self": canonical.get(e) == e,
            "root_words": words.get(r, 0),
            "en_words": words.get(e, 0),
        })

    rows.sort(key=lambda x: -(x["root_in"] + x["en_in"]))

    root_wins = sum(1 for x in rows if x["root_in"] > x["en_in"])
    en_wins = sum(1 for x in rows if x["en_in"] > x["root_in"])
    tie = sum(1 for x in rows if x["root_in"] == x["en_in"])
    both_zero = sum(1 for x in rows if x["root_in"] == 0 and x["en_in"] == 0)

    print(f"pairs where ROOT has more inbound links : {root_wins}")
    print(f"pairs where EN/  has more inbound links : {en_wins}")
    print(f"pairs tied                              : {tie}")
    print(f"pairs with 0 inbound on BOTH sides      : {both_zero}")
    print(f"root inbound total: {sum(x['root_in'] for x in rows):,}   "
          f"en inbound total: {sum(x['en_in'] for x in rows):,}")
    print(f"in a sitemap: root {sum(1 for x in rows if x['root_sm'])}/{len(rows)}   "
          f"en {sum(1 for x in rows if x['en_sm'])}/{len(rows)}")
    print(f"declares hreflang: root {sum(1 for x in rows if x['root_hl'] != '-')}   "
          f"en {sum(1 for x in rows if x['en_hl'] != '-')}\n")

    hdr = ("dir", "root_in", "en_in", "root_nav", "en_nav", "root_sm", "en_sm",
           "root_hl", "en_hl", "root_words", "en_words")
    print(f"{'dir':<46}{'r_in':>6}{'e_in':>6}{'r_nav':>6}{'e_nav':>6}"
          f"{'r_sm':>5}{'e_sm':>5}{'r_wds':>7}{'e_wds':>7}  hl")
    for x in rows[: args.top]:
        print(f"{x['dir'][:45]:<46}{x['root_in']:>6}{x['en_in']:>6}{x['root_nav']:>6}"
              f"{x['en_nav']:>6}{str(x['root_sm'])[0]:>5}{str(x['en_sm'])[0]:>5}"
              f"{x['root_words']:>7}{x['en_words']:>7}  {x['root_hl']}/{x['en_hl']}")

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=hdr)
            w.writeheader()
            for x in rows:
                w.writerow({k: x[k] for k in hdr})
        print(f"\nwrote {args.csv} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
