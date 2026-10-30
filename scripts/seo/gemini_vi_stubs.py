#!/usr/bin/env python3
"""
gemini_vi_stubs.py — create the VI redirect stubs the EN tree already has.

The gemini-notebooks articles live once, under
`tennis-technical-reference/gemini-notebooks/<slug>/`. The root-level
`gemini-notebooks/<slug>/` paths are legacy public URLs, kept alive as
meta-refresh + canonical stubs: 448 of them, exactly matching the 448 canonical
articles, 0 orphans, 0 missing.

The VI tree has the same 448 canonical articles and the same sidebar links
pointing at `/vi/gemini-notebooks/<slug>/` — but **no stubs at all**:
`vi/gemini-notebooks/` contains only index.html. That is 892 dead links inside
the VI gemini pages, all pointing at a path shape the EN side already solved.

This generates the missing VI stubs, one per canonical article, mirroring the
EN stub's structure (meta refresh + canonical + body link) with VI text and the
VI target. Absolute URLs, as the EN siblings use.

Guards: the target must exist before a stub is written; an existing file is
never overwritten; rerun reports 0.

Usage:
  python scripts/seo/gemini_vi_stubs.py --root . [--write]
"""
import argparse
import os
from pathlib import Path

CANON = "vi/tennis-technical-reference/gemini-notebooks"
STUBS = "vi/gemini-notebooks"

TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <title>Đang chuyển hướng...</title>
  <meta http-equiv="refresh" content="0; url=/{target}">
  <link rel="canonical" href="/{target}">
</head>
<body>
  <p>Đang chuyển hướng đến <a href="/{target}">/{target}</a>...</p>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    os.chdir(args.root)

    canon = Path(CANON)
    if not canon.is_dir():
        raise SystemExit(f"canonical tree missing: {CANON}")

    slugs = sorted(d.name for d in canon.iterdir() if d.is_dir())
    print(f"canonical articles: {len(slugs)}")

    created = skipped = 0
    missing_target = []
    for slug in slugs:
        target_dir = canon / slug
        if not (target_dir / "index.html").is_file():
            missing_target.append(slug)
            continue
        stub = Path(STUBS) / slug / "index.html"
        if stub.exists():
            skipped += 1
            continue
        target = f"{CANON}/{slug}/"
        body = TEMPLATE.format(target=target)
        if args.write:
            stub.parent.mkdir(parents=True, exist_ok=True)
            stub.write_text(body, encoding="utf-8", newline="")
        created += 1

    print(f"stubs created: {created}   already present: {skipped}   "
          f"targets missing: {len(missing_target)}")
    for s in missing_target[:5]:
        print(f"  !! no index.html in {CANON}/{s}/")
    if not args.write:
        print("(dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
