# -*- coding: utf-8 -*-
"""
Complete an hreflang annotation set that the page's own tags already determine.

Two defects, one repair
-----------------------
1. MISSING SELF-REFERENCE. A page carrying only

       <link rel="alternate" href="/blog/x/" hreflang="en">

   on `/vi/blog/x/` names its twin but never names itself. Google's rule is that
   the annotation set is identical on every page of the cluster and each version
   lists itself. So the VI page must also carry `vi -> itself`.

2. MISSING X-DEFAULT. A page carrying `en` and `vi` but no `x-default` leaves the
   cluster without a fallback. `xdefault_complete.py` already fixed this class
   elsewhere; these are the pages it could not see.

Why neither is a judgement call
-------------------------------
Both values are read off the tree, not chosen:

  * the self tag's href is the page's own URL -- there is nothing else it can be;
  * `x-default` is copied from the page's own `en` alternate href. Measured across
    all 7,150 pages that carry an x-default tag, `x-default == en href` holds
    **7,150 / 7,150** with zero exceptions, and `xdefault_complete.py` documents
    the same rule ("copied from the page's own `en` alternate rather than
    recomputed, so a cluster whose EN twin lives at a non-mirrored path stays
    correct").

Where the twin already speaks, it is cross-checked
--------------------------------------------------
If the counterpart page (the other-language alternate) exists and declares the
value being written, the two must agree. Disagreement is reported and the page is
refused -- that would be a cluster with a genuine conflict, which is a decision,
not a repair.

Refusals (never guessed)
------------------------
  * `<html lang>` contradicts the path prefix;
  * no `en` alternate, so x-default has no source;
  * an own-language tag already exists but resolves elsewhere (wrong-self);
  * the last alternate tag does not sit on a line of its own;
  * the counterpart disagrees with the value that would be written.

Style
-----
New tags are produced by rewriting an existing tag on the same page, so attribute
order, quoting, indentation and `>` vs `/>` all match the file. Nothing existing is
rewritten or reordered.

Usage
-----
    python scripts/seo/hreflang_selfref_fix.py            # dry run
    python scripts/seo/hreflang_selfref_fix.py --write
"""
import argparse
import os
import re
import sys
import urllib.parse
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github"}

LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
HTML_LANG = re.compile(r"<html\b[^>]*>", re.I)
ATTR = re.compile(
    r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))"""
)
HREFLANG_VAL = re.compile(r"""(\shreflang\s*=\s*)(["'])([^"']*)(\2)""", re.I)
HREF_VAL = re.compile(r"""(\shref\s*=\s*)(["'])([^"']*)(\2)""", re.I)


def attrs(tag):
    out = {}
    for m in ATTR.finditer(tag):
        key = m.group(1).lower()
        val = m.group(2)
        if val is None:
            val = m.group(3) if m.group(3) is not None else m.group(4)
        out[key] = val or ""
    return out


def page_url(rel):
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def norm(href, base):
    if not href:
        return ""
    p = urllib.parse.urlsplit(urllib.parse.urljoin(base, href)).path
    p = urllib.parse.unquote(p)
    if not p.startswith("/"):
        p = "/" + p
    if p.endswith("/index.html"):
        p = p[: -len("index.html")]
    return p


def walk():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            if fn.lower().endswith(".html"):
                yield os.path.join(dirpath, fn)


def read_alts(html):
    """[(lang, href, tag_text)] in document order, plus canonical href."""
    alts, canon = [], None
    for m in LINK_TAG.finditer(html):
        tag = m.group(0)
        a = attrs(tag)
        rel = (a.get("rel") or "").lower().split()
        if "alternate" in rel and "hreflang" in a:
            alts.append((a["hreflang"].strip().lower(), a.get("href", ""), tag))
        elif "canonical" in rel:
            canon = a.get("href", "")
    return alts, canon


def own_lang(rel, html):
    path_lang = "vi" if rel.startswith("vi/") else "en"
    m = HTML_LANG.search(html)
    if not m:
        return path_lang, None
    declared = (attrs(m.group(0)).get("lang") or "").strip().lower().split("-")[0]
    if declared in ("en", "vi") and declared != path_lang:
        return path_lang, declared
    return path_lang, None


def retarget(template, lang, href):
    """Rewrite an existing alternate tag to a new lang/href, keeping its style."""
    out = HREFLANG_VAL.sub(lambda m: m.group(1) + m.group(2) + lang + m.group(4), template, count=1)
    out = HREF_VAL.sub(lambda m: m.group(1) + m.group(2) + href + m.group(4), out, count=1)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="apply (default: dry run)")
    ap.add_argument("--only", metavar="PREFIX", help="restrict to paths with this prefix")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    plan = []          # (rel, [(lang, href, new_tag)], indent, template)
    refused = []
    single_lang = []
    already = 0
    seen = 0

    for full in walk():
        rel = os.path.relpath(full, ROOT).replace(os.sep, "/")
        if args.only and not rel.startswith(args.only):
            continue
        try:
            html = open(full, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        alts, canon = read_alts(html)
        if not alts:
            continue
        seen += 1

        base = page_url(rel)
        lang, declared = own_lang(rel, html)

        by_lang = {}
        for l, h, t in alts:
            by_lang.setdefault(l, []).append((h, t))

        to_add = []

        # ---- 1. self-reference ----
        if lang not in by_lang:
            to_add.append((lang, base))
        else:
            if not any(norm(h, base) == norm(base, base) for h, _ in by_lang[lang]):
                refused.append(
                    (rel, "own tag %s resolves to %s, not self" % (lang, by_lang[lang][0][0]))
                )
                continue

        # ---- 2. x-default ----
        if "x-default" not in by_lang:
            if "en" not in by_lang:
                if to_add:
                    refused.append((rel, "no en alternate, x-default has no source"))
                    continue
                # nothing derivable: a single-language page naming only itself
                single_lang.append(rel)
                continue
            to_add.append(("x-default", by_lang["en"][0][0]))

        # Nothing to write -> complete, and a lang mismatch is then not this
        # tool's business (the three such pages already carry all three tags).
        if not to_add:
            already += 1
            continue

        # A contradiction here only matters because it decides what to write.
        if declared:
            refused.append((rel, "html lang=%s contradicts path (%s)" % (declared, lang)))
            continue

        # ---- cross-check against the counterpart ----
        other = [l for l in by_lang if l not in (lang, "x-default")]
        conflict = None
        if other:
            twin_href = by_lang[other[0]][0][0]
            twin_rel = norm(twin_href, base).lstrip("/")
            twin_file = twin_rel + "index.html" if twin_rel.endswith("/") else twin_rel
            twin_path = os.path.join(ROOT, twin_file)
            if os.path.isfile(twin_path):
                twin_html = open(twin_path, encoding="utf-8", errors="replace").read()
                twin_alts, _ = read_alts(twin_html)
                twin_by = {}
                for l, h, t in twin_alts:
                    twin_by.setdefault(l, []).append(h)
                twin_base = page_url(twin_file)
                for l, href in to_add:
                    if l in twin_by:
                        mine = norm(href, base)
                        theirs = norm(twin_by[l][0], twin_base)
                        if mine != theirs:
                            conflict = "%s: page would write %s but twin declares %s" % (
                                l, mine, theirs,
                            )
                            break

        if conflict:
            refused.append((rel, conflict))
            continue

        # ---- locate the insertion point ----
        lines = html.split("\n")
        last_idx, indent, template = None, None, None
        for i, line in enumerate(lines):
            for m in LINK_TAG.finditer(line):
                a = attrs(m.group(0))
                if "alternate" in (a.get("rel") or "").lower().split() and "hreflang" in a:
                    last_idx, template = i, m.group(0)
        if last_idx is None:
            refused.append((rel, "no alternate tag on its own line"))
            continue
        stripped = LINK_TAG.sub("", lines[last_idx]).strip()
        if stripped:
            refused.append((rel, "last alternate line has other content"))
            continue
        indent = re.match(r"[ \t]*", lines[last_idx]).group(0)

        new_tags = [(l, h, retarget(template, l, h)) for l, h in to_add]
        plan.append((rel, new_tags, indent, lines, last_idx))

    # ---- report ----
    print("pages with >=1 alternate scanned : %d" % seen)
    print("  already complete               : %d" % already)
    print("  to change                      : %d" % len(plan))
    print("  refused                        : %d" % len(refused))
    print("  single-language (no en twin)   : %d" % len(single_lang))
    print()

    if single_lang:
        print("--- single-language, nothing derivable ---")
        for rel in single_lang:
            print("   %s" % rel)
        print()

    if refused:
        print("--- refused (not guessed) ---")
        for rel, why in refused:
            print("   %-70s %s" % (rel, why))
        print()

    kind = Counter()
    for rel, new_tags, _, _, _ in plan:
        for l, _, _ in new_tags:
            kind[l] += 1
    print("tags to add: %s" % dict(kind))
    print("total insertions: %d" % sum(kind.values()))
    print()

    if args.verbose or not args.write:
        for rel, new_tags, indent, _, _ in plan[:80]:
            print("   %s" % rel)
            for l, h, tag in new_tags:
                print("       + %s" % tag.strip())
        if len(plan) > 80:
            print("   ... %d more" % (len(plan) - 80))
        print()

    if not args.write:
        print("DRY RUN. Re-run with --write to apply.")
        return 0

    written = 0
    for rel, new_tags, indent, lines, last_idx in plan:
        ins = ["%s%s" % (indent, tag.strip()) for _, _, tag in new_tags]
        lines[last_idx + 1:last_idx + 1] = ins
        full = os.path.join(ROOT, rel)
        with open(full, "w", encoding="utf-8", newline="") as fh:
            fh.write("\n".join(lines))
        written += 1
    print("wrote %d files" % written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
