# -*- coding: utf-8 -*-
"""
Add the missing `x-default` to a cluster that already declares `en` and `vi`.

The invariant
-------------
A page that offers both an English and a Vietnamese alternate has to say which URL
to serve everyone else. Google's rule is that the annotation set is *identical on
every page of the cluster*: if one page names `x-default` and its twin does not,
the cluster is asymmetric and the fallback is unreliable. So `x-default` is all or
nothing per cluster -- mixed is the one state that is definitely wrong.

The class this fixes
--------------------
Neither verifier checks this. `seo_fix.py verify` asserts reciprocity, and
`hreflang_reciprocal.py` asserts the target/language invariant; both pass on a page
with no `x-default` at all. `xdefault_audit.py` measures the gap:

    pages declaring en AND vi     : 5,425
      missing x-default           : 4,705   (87%)
      of which in tnkb/ (legacy)  :   631

What it writes
--------------
Exactly one line, after the last existing alternate in the head:

    en page :  <link rel="alternate" href="<self>"   hreflang="x-default">
    vi page :  <link rel="alternate" href="<en url>" hreflang="x-default">

The href is copied from the page's own `en` alternate rather than recomputed, so a
cluster whose EN twin lives at a non-mirrored path stays correct.

Safety
------
  * never rewrites or reorders an existing tag; a page that already has
    `x-default` is skipped untouched;
  * only touches pages that already declare BOTH `en` and `vi`;
  * `tnkb/` is excluded unless --include-archive is passed (it is queued for
    retirement, so editing it is wasted work);
  * `--paths-from FILE` restricts the run to an explicit list, for reviewable
    batches;
  * report-only unless --write.

Usage:
  python scripts/seo/xdefault_complete.py                      # report
  python scripts/seo/xdefault_complete.py --explain            # + per-page detail
  python scripts/seo/xdefault_complete.py --write              # apply
  python scripts/seo/xdefault_complete.py --paths-from f.txt --write
"""
import os
import re
import sys

from hreflang_reciprocal import ALT_RE, iter_html

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ARCHIVE_PREFIXES = ("tnkb/", "vi/tnkb/")
MAX_BYTES = 1_500_000
HEAD_RE = re.compile(r"<head\b.*?</head>", re.I | re.S)
HREFLANG_RE = re.compile(r"""\shreflang\s*=\s*["']([^"']*)["']""", re.I)
HREF_RE = re.compile(r'\shref\s*=\s*"([^"]*)"', re.I)


def load_filter():
    """--paths-from FILE -> set of repo-relative paths, or None for no filter."""
    if "--paths-from" not in sys.argv:
        return None
    arg = sys.argv[sys.argv.index("--paths-from") + 1]
    with open(arg, "r", encoding="utf-8") as fh:
        return {ln.strip().replace("\\", "/") for ln in fh if ln.strip()}


def plan(only, include_archive):
    adds, skipped = [], {"already": 0, "not-bilingual": 0, "archive": 0, "no-head": 0}
    for full, rel in iter_html():
        key = rel.replace("\\", "/")
        if only is not None and key not in only:
            continue
        if not include_archive and key.startswith(ARCHIVE_PREFIXES):
            skipped["archive"] += 1
            continue
        try:
            if os.path.getsize(full) > MAX_BYTES:
                continue
            with open(full, "rb") as fh:
                text = fh.read().decode("utf-8", "replace")
        except OSError:
            continue
        if "hreflang" not in text:
            continue

        mh = HEAD_RE.search(text)
        if not mh:
            skipped["no-head"] += 1
            continue
        head = mh.group(0)

        alts = list(ALT_RE.finditer(head))
        if not alts:
            continue
        langs, en_href = set(), None
        for m in alts:
            lm = HREFLANG_RE.search(m.group(0))
            if not lm:
                continue
            code = lm.group(1).strip().lower()
            langs.add(code)
            if code == "en" and en_href is None:
                hm = HREF_RE.search(m.group(0))
                if hm:
                    en_href = hm.group(1)
        if "x-default" in langs:
            skipped["already"] += 1
            continue
        if not ("en" in langs and "vi" in langs):
            skipped["not-bilingual"] += 1
            continue
        if not en_href:
            continue

        adds.append({"rel": key, "path": full, "head": head, "en_href": en_href,
                     "head_start": mh.start(), "last": alts[-1]})
    return adds, skipped


def apply_one(item):
    text = None
    with open(item["path"], "rb") as fh:
        text = fh.read().decode("utf-8", "replace")
    m = item["last"]
    # group(1) is ([ \t]*) -- it matches the EMPTY string on flush-left tags, which
    # is falsy. Defaulting with `or` would indent a 0-indent file by 8 spaces and
    # make every diff in a large batch look wrong; only None means "no indent group".
    indent = m.group(1) if m.group(1) is not None else " " * 8
    tail = m.group(4)
    tag = f'<link rel="alternate" href="{item["en_href"]}" hreflang="x-default">'
    if tail and "\n" in tail:
        ins = f"{indent}{tag}{tail}"
    else:
        ins = f"\n{indent}{tag}"
    # `last` was matched against the <head> substring, so its offsets are relative
    # to head_start -- rebase onto the full document before slicing.
    end = item["head_start"] + m.end()
    new = text[:end] + ins + text[end:]
    # Invariant: removing exactly what we inserted must reproduce the original.
    # A mis-based offset (the bug this guard exists for) splits an existing tag and
    # still leaves a valid-looking file, so byte-level round-trip is the only check
    # that actually catches it.
    if new.replace(ins, "", 1) != text:
        return False
    with open(item["path"], "wb") as fh:
        fh.write(new.encode("utf-8"))
    return True


def main():
    write = "--write" in sys.argv
    explain = "--explain" in sys.argv or write
    include_archive = "--include-archive" in sys.argv
    only = load_filter()

    adds, skipped = plan(only, include_archive)

    print(f"pages to gain x-default        : {len(adds):,}")
    print(f"  skipped, already have it     : {skipped['already']:,}")
    print(f"  skipped, not en+vi           : {skipped['not-bilingual']:,}")
    print(f"  skipped, tnkb/ legacy        : {skipped['archive']:,}")
    if skipped["no-head"]:
        print(f"  skipped, no <head>           : {skipped['no-head']:,}")

    if explain:
        for a in adds:
            print(f"  + {a['rel']}  ->  {a['en_href']}")

    if not write:
        print("\nREPORT ONLY. Re-run with --write to apply.")
        return

    ok = 0
    bad = []
    for a in adds:
        if apply_one(a):
            ok += 1
        else:
            bad.append(a["rel"])
    print(f"\nwrote {ok} pages")
    if bad:
        print(f"REFUSED {len(bad)} (round-trip check failed):")
        for r in bad:
            print(f"  ! {r}")


if __name__ == "__main__":
    main()
