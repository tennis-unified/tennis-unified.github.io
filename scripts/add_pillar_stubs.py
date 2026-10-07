#!/usr/bin/env python3
"""
add_pillar_stubs.py — Create hyphenated alias URLs for the spaced "Pillars"
directories, without renaming the directories themselves.

Why not rename: 8,579 of 8,595 internal references to these trees are ABSOLUTE
("/Tenniskb-5 Pillars/..."), so a directory rename would break every one of them
(~25k files touch these paths). The spaced URLs already serve HTTP 200 on GitHub
Pages, and the Pillars trees are deliberately absent from the sitemap, so a
rename buys nothing but risk.

What this does instead: writes a redirect stub at each hyphenated path
(/tenniskb-5-pillars/, /tenniskb-10-pillars/, /vi/tenniskb-5-pillars/,
/vi/tenniskb-10-pillars/) pointing at the existing spaced directory. Clean URLs
work; nothing existing breaks.

Usage: python add_pillar_stubs.py --root <repo> [--dry-run]
"""

import argparse
import os
from pathlib import Path

CANON = "https://tennis-unified.github.io"

STUBS = [
    # (hyphenated alias path,      target path with spaces)
    ("tenniskb-5-pillars", "Tenniskb-5 Pillars"),
    ("tenniskb-10-pillars", "Tenniskb-10 Pillars"),
    ("vi/tenniskb-5-pillars", "vi/Tenniskb-5 Pillars"),
    ("vi/tenniskb-10-pillars", "vi/Tenniskb-10 Pillars"),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <title>Redirecting...</title>
  <meta http-equiv="refresh" content="0; url=/{target}/">
  <link rel="canonical" href="{canon}/{target}/">
</head>
<body>
  <p>{label} <a href="/{target}/">/{target}/</a>...</p>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    for alias, target in STUBS:
        tdir = root / target
        if not (tdir / "index.html").is_file():
            print(f"  SKIP {alias}: target {target}/index.html not found")
            continue
        # URL-encode the space for the redirect target
        target_url = target.replace(" ", "%20")
        lang = "vi" if alias.startswith("vi/") else "en"
        label = "Chuyển hướng đến" if lang == "vi" else "Redirecting to"
        page = TEMPLATE.format(lang=lang, target=target_url, canon=CANON, label=label)
        out = root / alias / "index.html"
        if args.dry_run:
            print(f"  WOULD WRITE {alias}/index.html -> /{target}/")
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page, encoding="utf-8", newline="")
            print(f"  wrote {alias}/index.html ({len(page)} bytes) -> /{target}/")


if __name__ == "__main__":
    main()
