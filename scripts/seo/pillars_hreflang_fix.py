#!/usr/bin/env python3
"""Complete the hreflang block on Pillars article pages that never got one.

The 2,558 generated Pillars articles (c971d66a91) each carry three <link
rel="alternate"> tags pairing the EN page with its VI twin by ART number. 18 of
them have none at all:

    Tenniskb-10 Pillars/ART-0991..0999_SportsScienceInjuryPreventionFutureMeta.html
    vi/Tenniskb-10 Pillars/ART-991..999_VN.html

Their immediate neighbours (ART-0990/ART-990) are complete, so this is not a
convention gap -- the generator skipped the tail of the batch. The likely cause
is that EN uses a 4-digit ART number and VI uses a 3-digit one (ART-0991 vs
ART-991), and any pairing step that derived the twin's filename by substituting
the same string into a template would miss exactly these.

This tool does not derive the twin from a template. It indexes every VI page by
its ART integer, looks the EN page's integer up, and **refuses the page** if
there is no twin or more than one. So it cannot invent a pairing.

It writes only the three <link rel="alternate"> lines, inserted immediately
after the existing <link rel="canonical">, in the same order and indentation the
neighbouring pages use (en, vi, x-default on the EN side; vi, x-default, en on
the VI side -- that asymmetry is what the generator emitted, and matching it is
what keeps the diff one block per file).

Idempotent: a page that already has any hreflang is skipped.

Usage
  python pillars_hreflang_fix.py --root .            # report
  python pillars_hreflang_fix.py --root . --write    # apply + verify
"""
import argparse
import html
import os
import re
import sys
import urllib.parse

DIRS = [
    ("Tenniskb-5 Pillars", "vi/Tenniskb-5 Pillars"),
    ("Tenniskb-10 Pillars", "vi/Tenniskb-10 Pillars"),
]

LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
ATTR = re.compile(
    r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))"""
)
ART = re.compile(r"ART-(\d+)", re.I)
CANON_LINE = re.compile(r"^([ \t]*)<link\b[^>]*rel\s*=\s*[\"']?canonical[\"']?[^>]*>[ \t]*$",
                        re.I | re.M)


def attrs_of(tag):
    out = {}
    for m in ATTR.finditer(tag):
        v = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        out[m.group(1).lower()] = html.unescape(v or "")
    return out


def meta(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    canon = None
    alts = {}
    for tag in LINK_TAG.findall(text):
        a = attrs_of(tag)
        rels = a.get("rel", "").lower().split()
        if "canonical" in rels and a.get("href"):
            canon = a["href"]
        if "alternate" in rels and a.get("hreflang"):
            alts[a["hreflang"].lower()] = a.get("href")
    return text, canon, alts


def art_num(path):
    m = ART.search(os.path.basename(path))
    return int(m.group(1)) if m else None


def url_of(rel_path):
    """Repo-relative path -> root-relative percent-encoded URL."""
    p = "/" + rel_path.replace(os.sep, "/")
    return urllib.parse.quote(p, safe="/()'!*._~-")


def block(side, en_url, vi_url, indent):
    if side == "en":
        rows = [("en", en_url), ("vi", vi_url), ("x-default", en_url)]
    else:
        rows = [("vi", vi_url), ("x-default", en_url), ("en", en_url)]
    return "\n".join(
        f'{indent}<link rel="alternate" href="{u}" hreflang="{l}">' for l, u in rows
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    total_planned = 0
    for en_dir, vi_dir in DIRS:
        ep = os.path.join(root, en_dir)
        vp = os.path.join(root, vi_dir)
        if not (os.path.isdir(ep) and os.path.isdir(vp)):
            continue

        # index VI pages by ART integer
        vi_by_art = {}
        vi_dupe = set()
        for fn in os.listdir(vp):
            if not fn.endswith(".html") or fn in ("article.html", "index.html"):
                continue
            n = art_num(fn)
            if n is None:
                continue
            if n in vi_by_art:
                vi_dupe.add(n)
            vi_by_art[n] = fn

        planned = []
        for fn in sorted(os.listdir(ep)):
            if not fn.endswith(".html") or fn in ("article.html", "index.html"):
                continue
            n = art_num(fn)
            if n is None:
                continue
            path = os.path.join(ep, fn)
            text, canon, alts = meta(path)
            if alts:
                continue
            if not canon:
                print(f"  skip (no canonical) {en_dir}/{fn}")
                continue
            if n in vi_dupe:
                print(f"  REFUSE (multiple VI twins for ART-{n}) {en_dir}/{fn}")
                continue
            vi_fn = vi_by_art.get(n)
            if vi_fn is None:
                print(f"  REFUSE (no VI twin for ART-{n}) {en_dir}/{fn}")
                continue
            planned.append((path, fn, vi_fn, n))

        # the VI side is the mirror of the same list
        planned_vi = []
        for path, en_fn, vi_fn, n in planned:
            vpath = os.path.join(vp, vi_fn)
            vtext, vcanon, valts = meta(vpath)
            if valts or not vcanon:
                continue
            planned_vi.append(vpath)

        print(f"\n{en_dir}: {len(planned)} EN page(s) to complete, "
              f"{len(planned_vi)} VI page(s)")
        total_planned += len(planned) + len(planned_vi)

        if not args.write:
            for path, en_fn, vi_fn, n in planned:
                print(f"    {en_fn}  <->  {vi_fn}")
            continue

        changed = 0
        for path, en_fn, vi_fn, n in planned:
            text, canon, alts = meta(path)
            en_url = url_of(os.path.join(en_dir, en_fn))
            vi_url = url_of(os.path.join(vi_dir, vi_fn))
            m = CANON_LINE.search(text)
            if not m:
                print(f"  !! canonical line not found in {en_fn}")
                continue
            indent = m.group(1)
            ins = block("en", en_url, vi_url, indent)
            text = text[: m.end()] + "\n" + ins + text[m.end():]
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(text)
            changed += 1

        for vpath in planned_vi:
            vtext, vcanon, valts = meta(vpath)
            vi_fn = os.path.basename(vpath)
            n = art_num(vi_fn)
            en_fn = next((f for f in os.listdir(ep)
                          if art_num(f) == n and f not in ("article.html", "index.html")), None)
            if en_fn is None:
                continue
            en_url = url_of(os.path.join(en_dir, en_fn))
            vi_url = url_of(os.path.join(vi_dir, vi_fn))
            m = CANON_LINE.search(vtext)
            if not m:
                print(f"  !! canonical line not found in {vi_fn}")
                continue
            indent = m.group(1)
            ins = block("vi", en_url, vi_url, indent)
            vtext = vtext[: m.end()] + "\n" + ins + vtext[m.end():]
            with open(vpath, "w", encoding="utf-8", newline="") as f:
                f.write(vtext)
            changed += 1
        print(f"  wrote {changed} file(s)")

    if not args.write:
        print(f"\n(dry run; {total_planned} file(s) to complete, --write to apply)")
        return

    # ---- verify: every Pillars page has a full, reciprocal set
    print("\n-- verify --")
    bad = 0
    for en_dir, vi_dir in DIRS:
        ep = os.path.join(root, en_dir)
        for fn in os.listdir(ep):
            if not fn.endswith(".html") or fn in ("article.html", "index.html"):
                continue
            text, canon, alts = meta(os.path.join(ep, fn))
            missing = [l for l in ("en", "vi", "x-default") if l not in alts]
            if missing:
                print(f"  !! {en_dir}/{fn} missing {missing}")
                bad += 1
                continue
            # reciprocity: the vi twin must point back at this page
            vp = os.path.join(root, urllib.parse.unquote(alts["vi"]).lstrip("/").replace("/", os.sep))
            if not os.path.isfile(vp):
                print(f"  !! {en_dir}/{fn} vi target does not exist: {alts['vi']}")
                bad += 1
                continue
            _, _, valts = meta(vp)
            if urllib.parse.unquote(valts.get("en", "")) != urllib.parse.unquote(alts["en"]):
                print(f"  !! {en_dir}/{fn} not reciprocal: vi.en={valts.get('en')}")
                bad += 1
    print(f"VERIFY {'OK' if bad == 0 else f'FAILED ({bad})'}")
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
