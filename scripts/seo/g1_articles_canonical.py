#!/usr/bin/env python3
"""
g1_articles_canonical.py — G1 of the canonical proposals (2026-10-29).

/articles/<slug>/ is a word-for-word (Jaccard 1.0) duplicate of
/en/articles/<slug>/ (the nav-linked canonical section). Consolidate:
  - set canonical on /articles/<slug>/ -> /en/articles/<slug>/
  - remove its three <link rel="alternate"> tags (a canonicalised duplicate
    must not emit hreflang)
  - remove the /articles/<slug>/ <url> blocks from sitemap.xml
  - regenerate sitemap.xml.gz

Idempotent. DRY RUN unless --write.

Usage: python g1_articles_canonical.py --root <repo> [--write]
"""
import argparse
import gzip
import re
from pathlib import Path

CANON = re.compile(r'<link rel="canonical" href="[^"]*">')
ALT = re.compile(r'[ \t]*<link rel="alternate" href="[^"]*" hreflang="[^"]*">\s*\n')
SITEMAP_URL = re.compile(
    r"[ \t]*<url>\s*<loc>https://tenniskb\.github\.io/articles/[^<]*</loc>[\s\S]*?</url>\s*\n?"
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)

    art = root / "articles"
    pages = sorted(art.glob("*/index.html")) if art.is_dir() else []
    changed = 0
    for p in pages:
        slug = p.parent.name
        text = p.read_text(encoding="utf-8", errors="ignore")
        new = CANON.sub(lambda m: f'<link rel="canonical" href="/en/articles/{slug}/">', text, count=1)
        new = ALT.sub("", new)
        if new != text:
            changed += 1
            if args.write:
                p.write_text(new, encoding="utf-8", newline="")

    # sitemap: drop /articles/ blocks
    sm = root / "sitemap.xml"
    stext = sm.read_text(encoding="utf-8", errors="ignore")
    before = len(re.findall(r"<loc>https://tenniskb\.github\.io/articles/", stext))
    snew = SITEMAP_URL.sub("", stext)
    after = len(re.findall(r"<loc>https://tenniskb\.github\.io/articles/", snew))

    print(f"pages={len(pages)} changed={changed} write={args.write}")
    print(f"sitemap /articles/ locs: {before} -> {after}")

    if args.write:
        sm.write_text(snew, encoding="utf-8", newline="")
        gz = root / "sitemap.xml.gz"
        gz.write_bytes(gzip.compress(snew.encode("utf-8"), mtime=0))
        print(f"  wrote sitemap.xml + sitemap.xml.gz")
    else:
        print("  (dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
