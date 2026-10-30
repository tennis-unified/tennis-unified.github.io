#!/usr/bin/env python3
"""Add the missing self-canonical to blog pages that already declare hreflang.

114 pages emit <link rel="alternate"> tags but no <link rel="canonical"> at all.
`xdefault_audit` counts them as "missing canonical: 114" and `canonical_audit`
counts the same 114 as "canonical-less but declares hreflang" -- two audits, same
pages, neither of which changes anything.

A page that declares a language cluster but not which URL is canonical for
itself is emitting a contradictory pair: "I am the `vi` member of this cluster"
and "I have not said which copy of me to index".

Eligibility is decided by an ordered evidence hierarchy, strongest first, and the
tool records which rule fired for each page:

  named-canonical  a counterpart's canonical already points at this URL. The
                   which-URL-wins decision was made elsewhere; this side simply
                   never recorded it. Nothing is decided here.
  (duplicate guard)  before any weaker rule is allowed to fire: if a counterpart
                   at the other path is the same article -- word-level
                   similarity >= DUP_THRESHOLD, the same 0.85 the repo uses in
                   find_blog_variants() -- and that counterpart does NOT
                   canonicalise here, the page is a duplicate and is REFUSED.
                   This is the /blog/ which-URL-wins class the handoff marks
                   "do not sweep", and the guard is what keeps this tool out of
                   it.
  declared         the page's own-language alternate points at itself, and no
                   counterpart is a near-duplicate. The page says "I am the copy
                   for my language".
  reciprocal       the page has only the other-language alternate, and that twin
                   names this URL as its alternate for this page's language.

Anything else is refused and printed with the reason. The tool cannot turn a
duplicate into a self-canonical by guessing.

Idempotent: a page with any canonical is skipped.

Usage
  python blog_canonical_fix.py --root .            # report
  python blog_canonical_fix.py --root . --write    # apply + verify
  python blog_canonical_fix.py --root . --threshold 0.85
"""
import argparse
import difflib
import html
import os
import re
import sys
import urllib.parse

ROOTS = [("blog", "en"), ("vi/blog", "vi")]
DUP_THRESHOLD = 0.85

LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
ATTR = re.compile(
    r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))"""
)
LANG = re.compile(r"<html[^>]*\blang\s*=\s*[\"']?([a-zA-Z-]+)", re.I)
TAG = re.compile(r"<[^>]+>")
SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.I | re.S)
FIRST_ALT_LINE = re.compile(
    r"^([ \t]*)<link\b[^>]*\brel\s*=\s*[\"']?alternate[\"']?[^>]*>[ \t]*$", re.I | re.M
)


def attrs_of(tag):
    out = {}
    for m in ATTR.finditer(tag):
        v = m.group(2) if m.group(2) is not None else (
            m.group(3) if m.group(3) is not None else m.group(4)
        )
        out[m.group(1).lower()] = html.unescape(v or "")
    return out


def read_page(path):
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
            alts[a["hreflang"].lower()] = a["href"]
    m = LANG.search(text)
    return text, canon, alts, (m.group(1).lower() if m else "")


def key(p):
    p = urllib.parse.unquote(urllib.parse.urlsplit(p).path)
    if not p.startswith("/"):
        p = "/" + p
    return re.sub(r"/{2,}", "/", p).rstrip("/") or "/"


def fs_path(root, url):
    return os.path.join(root, urllib.parse.unquote(url).lstrip("/").replace("/", os.sep),
                        "index.html")


_words_cache = {}


def words(path):
    if path not in _words_cache:
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                t = f.read()
        except OSError:
            _words_cache[path] = []
        else:
            body = TAG.sub(" ", SCRIPT.sub(" ", t))
            _words_cache[path] = re.findall(r"[^\W\d_]+", body, re.U)
    return _words_cache[path]


def similarity(a, b):
    wa, wb = words(a), words(b)
    if not wa or not wb:
        return 0.0
    return difflib.SequenceMatcher(None, wa, wb, autojunk=False).ratio()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--threshold", type=float, default=DUP_THRESHOLD)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    plan = []
    refused = []

    for rel_root, _ in ROOTS:
        base = os.path.join(root, rel_root)
        if not os.path.isdir(base):
            continue
        for slug in sorted(os.listdir(base)):
            path = os.path.join(base, slug, "index.html")
            if not os.path.isfile(path):
                continue
            text, canon, alts, lang = read_page(path)
            if canon or not alts or not lang:
                continue
            own = key("/" + rel_root + "/" + slug + "/")
            rel = os.path.relpath(path, root).replace(os.sep, "/")

            counterparts = []
            for ol, href in alts.items():
                if ol == "x-default" or ol == lang:
                    continue
                tp = fs_path(root, href)
                if os.path.isfile(tp):
                    counterparts.append((ol, tp))

            # rule 1 -- someone already canonicalises here
            if any(key(tc or "") == own for _, tp in counterparts
                   for _, tc, _, _ in [read_page(tp)]):
                plan.append((path, own, "named-canonical"))
                continue

            # guard -- same article at two paths, and nobody has picked one
            dup = [(ol, tp) for ol, tp in counterparts
                   if similarity(path, tp) >= args.threshold]
            if dup:
                refused.append((rel, f"near-duplicate ({similarity(path, dup[0][1]):.3f}) "
                                     f"of {dup[0][1]} which does not canonicalise here"))
                continue

            # rule 2 -- the page declares itself for its own language
            if key(alts.get(lang, "")) == own:
                plan.append((path, own, "declared"))
                continue

            # rule 3 -- the twin declares this URL as its alternate for `lang`
            if any(key(read_page(tp)[2].get(lang, "")) == own for _, tp in counterparts):
                plan.append((path, own, "reciprocal"))
                continue

            refused.append((rel, "no evidence: not named by any canonical, "
                                 "not self-declared, not reciprocally declared"))

    print(f"eligible: {len(plan)}   refused: {len(refused)}")
    by = {}
    for _, _, g in plan:
        by[g] = by.get(g, 0) + 1
    for g, n in sorted(by.items()):
        print(f"   {g:<16} {n}")
    if refused:
        print("\n-- refused --")
        for rel, why in refused[:10]:
            print(f"   {rel}\n      {why}")

    if not args.write:
        print("\n(dry run; --write to apply)")
        return

    written = 0
    for path, own, grade in plan:
        text, canon, alts, lang = read_page(path)
        if canon:
            continue
        m = FIRST_ALT_LINE.search(text)
        if not m:
            print(f"  !! no alternate line to anchor on: {path}")
            continue
        line = (f'{m.group(1)}<link rel="canonical" href="'
                f'{urllib.parse.quote(own, safe="/()\'!*._~-")}/">')
        text = text[: m.start()] + line + "\n" + text[m.start():]
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        written += 1
    print(f"  wrote {written} file(s)")

    # ---- verify
    print("\n-- verify --")
    refused_set = {r[0] for r in refused}
    bad = 0
    for rel_root, _ in ROOTS:
        base = os.path.join(root, rel_root)
        if not os.path.isdir(base):
            continue
        for slug in sorted(os.listdir(base)):
            path = os.path.join(base, slug, "index.html")
            if not os.path.isfile(path):
                continue
            _, canon, alts, _ = read_page(path)
            if not alts:
                continue
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            if not canon and rel not in refused_set:
                print(f"  !! still no canonical: {rel}")
                bad += 1
    print(f"VERIFY {'OK' if bad == 0 else f'FAILED ({bad})'}")
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
