#!/usr/bin/env python3
"""
pillar_index_repoint.py — point the four Pillars catalogs at the static article
pages instead of at the client-side reader.

Background (session report §38):
  §34 generated a static, server-rendered page per Pillars article (2,558 files),
  gave each a self-canonical and en/vi/x-default alternates, and listed them in
  both sitemaps. But the catalogs were never updated: all four `index.html` files
  still link `article.html?p=<name>.md&lang=<lang>`, and `article.html` is a
  63-character "Loading article..." shell that canonicalises to itself and is in
  neither sitemap.

  Consequence, measured 2026-10-29: 1,279 Pillars pages are in the sitemap with
  zero inbound internal links, while every internal link points at a URL the
  sitemap does not contain and that cannot be indexed.

  The static page is a superset of the reader: same shell/CSS/MathJax, the article
  body is inline instead of fetched, and (after pillar_nav_populate.py) it has the
  same prev/next and the same language switcher. So repointing loses nothing.

TARGET RESOLUTION
  `article.html?p=ART-002-<slug>.md` -> `ART-002-<slug>.html` in the same
  directory. A link is rewritten only when that file exists; anything else is
  reported and left alone rather than pointed at a 404.

  One link is a typo, not a missing page: `vi/Tenniskb-5 Pillars/index.html`
  references `ART-001_GRF_TriPlanar_VI.md`. Measured: `*_VI.md` and `*_VI.html`
  exist nowhere in the tree while `*_VN.*` number 1,279, so `_VI` is a
  transcription slip for `_VN`. It is repaired explicitly and counted separately —
  it is not silently folded into the rewrite.

Idempotent: a catalog with no `article.html?p=` links is skipped.
Safe by default: DRY RUN unless --write.

Usage:
  python scripts/seo/pillar_index_repoint.py --root .            # dry-run
  python scripts/seo/pillar_index_repoint.py --root . --write
"""
import argparse
import re
from pathlib import Path

DIRS = ("Tenniskb-10 Pillars", "Tenniskb-5 Pillars",
        "vi/Tenniskb-10 Pillars", "vi/Tenniskb-5 Pillars")

# href="article.html?p=NAME.md&lang=xx"  (lang may be absent; & may be &amp;)
RE_LINK = re.compile(
    r'href="article\.html\?p=([^"&]+?)(?:&(?:amp;)?lang=[a-z]{2})?"'
)

# The one measured typo, declared rather than pattern-matched.
TYPO = {"ART-001_GRF_TriPlanar_VI.md": "ART-001_GRF_TriPlanar_VN.md"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    tot_rew = tot_typo = tot_unres = 0

    for d in DIRS:
        dd = root / d
        idx = dd / "index.html"
        if not idx.is_file():
            print(f"  WARN missing {idx}")
            continue
        html = idx.read_text(encoding="utf-8")
        rew = typo = unres = 0
        missing = []

        def rep(m):
            nonlocal rew, typo, unres
            name = m.group(1)
            fixed = TYPO.get(name, name)
            stem = Path(fixed).stem
            if not (dd / (stem + ".html")).is_file():
                unres += 1
                missing.append(name)
                return m.group(0)
            if fixed != name:
                typo += 1
            rew += 1
            return f'href="{stem}.html"'

        new = RE_LINK.sub(rep, html)
        changed = new != html
        print(f"  {d:26s} links_rewritten={rew:5d} (typo_repaired={typo}) "
              f"unresolved={unres:3d} bytes {len(html)}->{len(new)}")
        for n in missing[:5]:
            print(f"      UNRESOLVED {n}")
        if changed and args.write:
            idx.write_text(new, encoding="utf-8", newline="")
        tot_rew += rew
        tot_typo += typo
        tot_unres += unres

    print(f"\nSUMMARY: write={args.write} rewritten={tot_rew} "
          f"typo_repaired={tot_typo} unresolved={tot_unres}")
    if not args.write:
        print("  (dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
