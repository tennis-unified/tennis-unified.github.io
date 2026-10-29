# -*- coding: utf-8 -*-
"""
Give a SILENT twin the reciprocal tags it is already named by.

The class this fixes
--------------------
`hreflang_reciprocal.py` counts an edge as non-reciprocal only when the target is a
page it knows about, and `build()` only knows about pages that already carry at
least one alternate. So an edge pointing at a page with *no* hreflang at all is not
counted as broken -- it is not counted at all:

    edges -> target EXISTS but has NO alternates : 1,325  (47 targets)
    edges -> target DOES NOT EXIST               : 0

1,262 of those are the two `tnkb/` homes (archive, deliberately excluded). The rest
are Vietnamese pages naming an English twin that exists and says nothing back, so
reciprocity is impossible until the ENGLISH page gains a tag. That is this tool's
job, and it is deliberately narrow:

  * it only ever touches a page that (a) is the target of at least one alternate
    from a page of the OTHER language, and (b) currently has zero alternates;
  * it never rewrites an existing tag -- that is `hreflang_reciprocal.py`'s D rule;
  * it adds `canonical` too, but only where the page has none. These targets are
    hand-built (`mm-top` nav, absolute `/assets/`) and most predate the D1
    self-canonical pass, so they are a large slice of the 4,453 canonical-less
    pages `canonical_audit.py` counts.

Why the tags it writes are the right ones
-----------------------------------------
The site convention (D1 + the mirrored-path rule in `hreflang_fix.py`) is:

    canonical      root-relative self  ->  resolves per host
    hreflang="en"  this page           (the page is English by construction)
    hreflang="vi"  the mirrored path   /vi/<same path>/
    hreflang="x-default"  this page    (English is the default)

The page is treated as English only because its own `<html lang>` says so and its
twin resolves; if a target's declared language disagrees with its path, the page is
reported and skipped rather than guessed at.

Insertion point
---------------
After the `</title>` line. These pages have no canonical/alternate block to extend
and no generator that will fight the edit, so a stable anchor beats a positional
guess. Existing canonicals are detected attribute-order-independently and left
alone -- `authoritative-sources` has one glued to the end of a stylesheet line.

Usage:
  python scripts/seo/hreflang_complete.py            # report
  python scripts/seo/hreflang_complete.py --explain  # + per-page detail
  python scripts/seo/hreflang_complete.py --write    # apply
"""
import os
import re
import sys

from hreflang_reciprocal import ALT_RE, iter_html, lang_of_key, norm_key, resolve, twin_key

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARCHIVE_PREFIX = "/tnkb"
CANON_RE = re.compile(r'<link\b(?=[^>]*\shref\s*=\s*"[^"]*")(?=[^>]*\srel\s*=\s*["\']?canonical)', re.I)
TITLE_RE = re.compile(r"^[^\n]*</title>[ \t]*\r?\n", re.M)
INDENT = " " * 8


def on_disk(key):
    p = os.path.join(ROOT, key.strip("/").replace("/", os.sep))
    return any(os.path.isfile(c) for c in (os.path.join(p, "index.html"), p, p + ".html"))


def scan():
    """-> {target_key: set(languages of the pages pointing at it)} for silent targets."""
    have, edges = {}, {}
    for full, rel in iter_html():
        with open(full, "rb") as fh:
            text = fh.read().decode("utf-8", "replace")
        ms = list(ALT_RE.finditer(text))
        key = norm_key(rel)
        if ms:
            have[key] = rel
        for m in ms:
            kind, tgt = resolve(os.path.dirname(rel), m.group(2))
            if kind == "REL":
                edges.setdefault(tgt, []).append((rel, m.group(3).lower()))

    silent = {}
    for tgt, srcs in edges.items():
        if tgt in have or tgt.startswith(ARCHIVE_PREFIX) or not on_disk(tgt):
            continue
        # Only count it if a page of the OTHER language names it -- a same-language
        # edge is a duplicate, and canonical is the tool for that, not hreflang.
        other = {lang_of_key("/" + s.split("/")[0] + "/") for s, _l in srcs}
        if lang_of_key(tgt) not in other:
            silent[tgt] = sorted({l for _s, l in srcs})
    return silent, have


def plan(silent):
    adds, skipped = [], []
    for tgt in sorted(silent):
        rel = tgt.strip("/") + "/index.html"
        path = os.path.join(ROOT, rel.replace("/", os.sep))
        if not os.path.isfile(path):
            skipped.append((tgt, "no index.html on disk"))
            continue
        with open(path, "rb") as fh:
            text = fh.read().decode("utf-8")
        if ALT_RE.search(text):
            skipped.append((tgt, "already has alternates"))
            continue
        lang = re.search(r'<html[^>]*\blang="([^"]*)"', text, re.I)
        lang = lang.group(1).lower().split("-")[0] if lang else None
        if lang != "en":
            # The tag we would write declares English; if the page disagrees, stop.
            skipped.append((tgt, f'<html lang="{lang}">, not en'))
            continue
        twin = twin_key(tgt)
        if not on_disk(twin):
            skipped.append((tgt, f"twin {twin} missing"))
            continue
        if not TITLE_RE.search(text):
            skipped.append((tgt, "no </title> anchor"))
            continue
        adds.append(
            {
                "key": tgt,
                "rel": rel,
                "path": path,
                "text": text,
                "canonical": bool(CANON_RE.search(text)),
                "twin": twin,
            }
        )
    return adds, skipped


def block(item):
    p = item["key"]
    lines = []
    if not item["canonical"]:
        lines.append(f'{INDENT}<link rel="canonical" href="{p}">')
    lines.append(f'{INDENT}<link rel="alternate" href="{p}" hreflang="en">')
    lines.append(f'{INDENT}<link rel="alternate" href="{item["twin"]}" hreflang="vi">')
    lines.append(f'{INDENT}<link rel="alternate" href="{p}" hreflang="x-default">')
    return "\n".join(lines) + "\n"


def apply_block(item):
    text = item["text"]
    m = TITLE_RE.search(text)
    end = m.end()
    return text[:end] + block(item) + text[end:]


def main():
    write = "--write" in sys.argv
    explain = "--explain" in sys.argv or write

    silent, have = scan()
    adds, skipped = plan(silent)

    print(f"pages with hreflang            : {len(have):,}")
    print(f"silent targets (non-archive)   : {len(silent)}")
    print(f"  completable                  : {len(adds)}")
    print(f"  skipped (need a human)       : {len(skipped)}")
    n_can = sum(1 for a in adds if not a["canonical"])
    print(f"  of completable, gain a canonical: {n_can}")

    if explain:
        for a in adds:
            print(f"  + {a['key']}  canonical={'existing' if a['canonical'] else 'NEW'}")
        for k, why in skipped:
            print(f"  ! {k}  -- {why}")

    if not write:
        print("\nREPORT ONLY. Re-run with --write to apply.")
        return

    for a in adds:
        with open(a["path"], "wb") as fh:
            fh.write(apply_block(a).encode("utf-8"))
    print(f"\nwrote {len(adds)} pages ({n_can} new canonicals, {len(adds) * 3} alternates)")


if __name__ == "__main__":
    main()
