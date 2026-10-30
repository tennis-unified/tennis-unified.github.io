#!/usr/bin/env python3
"""
pillar_nav_fix.py — drop the three Pillars nav tabs that point at nothing.

The 18-tab `md-tabs` nav in the Pillars article shell carries three links that
resolve to 404 and have no counterpart anywhere in the tree or in git history:

    ../tennis-wiki-reference/   "Wiki"
    ../building-champions/      "Champions"
    ../new-issue/               "New Issue"

Measured 2026-10-29: 404 live on all three; `git log --all -- <path>` returns
nothing for any of them, so they were never built here — they are not a rename,
they are a template written against a different site plan. Every generated
Pillars article inherits them: 2,560 pages x 3 dead tabs = 7,680 dead nav edges.

Removal is the information-preserving fix: the same nav already carries
"Reference" -> ../reference-library/ (200 live), so repointing "Wiki" at the
technical reference would duplicate an existing tab, and "Champions" / "New Issue"
have no candidate at all.

Scope is the four Pillars directories, including the two `article.html` shells —
the shells matter because `pillar_static_gen.py` reads them as the template, so a
regeneration would otherwise reintroduce the dead tabs.

Idempotent: a page with no dead tab is skipped, so rerun reports 0.

Usage:
  python scripts/seo/pillar_nav_fix.py --root . [--write]
"""
import argparse
import re
import sys
from pathlib import Path

DIRS = ("Tenniskb-5 Pillars", "Tenniskb-10 Pillars",
        "vi/Tenniskb-5 Pillars", "vi/Tenniskb-10 Pillars")

DEAD = ("tennis-wiki-reference", "building-champions", "new-issue")

# <li class="md-tabs__item"><a href="../tennis-wiki-reference/" class="md-tabs__link">Wiki</a></li>
ITEM = re.compile(
    r"[ \t]*<li class=\"md-tabs__item\">\s*<a\s[^>]*href=\"[^\"]*(?:"
    + "|".join(re.escape(d) for d in DEAD)
    + r")/\"[^>]*>[^<]*</a>\s*</li>\n?",
    re.I,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)

    files = []
    for d in DIRS:
        p = root / d
        if p.is_dir():
            files += sorted(p.glob("*.html"))

    changed = removed = 0
    tabs_before = tabs_after = 0
    for p in files:
        text = p.read_text(encoding="utf-8", errors="ignore")
        hits = ITEM.findall(text)
        if not hits:
            continue
        new, n = ITEM.subn("", text)
        if n != len(hits):  # substitution and count disagree -> do not touch
            print(f"  !! {p}: findall={len(hits)} subn={n}, skipped")
            continue
        tb = text.count('class="md-tabs__item"')
        ta = new.count('class="md-tabs__item"')
        if tb - ta != n:
            print(f"  !! {p}: tab delta {tb - ta} != removed {n}, skipped")
            continue
        if new.count("<li") - new.count("</li>") != 0 and text.count("<li") == text.count("</li>"):
            print(f"  !! {p}: li balance changed, skipped")
            continue
        changed += 1
        removed += n
        tabs_before += tb
        tabs_after += ta
        if args.write:
            p.write_text(new, encoding="utf-8", newline="")

    print(f"pillar pages: {len(files)}   files needing repair: {changed}   "
          f"dead tabs removed: {removed}   tabs {tabs_before} -> {tabs_after}")
    if not args.write:
        print("(dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
