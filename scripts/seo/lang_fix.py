#!/usr/bin/env python3
"""
lang_fix.py — correct <html lang> to match the page's actual body language.

G3a (independent, safe): sources/tennis-wiki/docs/vi/** and book/TUC/chuong-*
are Vietnamese (verified: titles "Tài Liệu Kỹ Thuật" / "Chương 1…", 9-17% VI
diacritic chars) but declare lang="en". Set lang="vi".

Only the <html> opening tag's lang attribute is touched (quoted or unquoted);
nothing else in the file changes. Idempotent: pages already lang="vi" are skipped.

Usage: python lang_fix.py --root <repo> [--write]
"""
import argparse
import re
import sys
from pathlib import Path

HTML_TAG = re.compile(r"<html\b[^>]*>", re.I)
LANG_ATTR = re.compile(r"""(lang\s*=\s*["']?)en(["\']?)""", re.I)


def fix_text(text):
    m = HTML_TAG.search(text)
    if not m:
        return text, False
    tag = m.group(0)
    new_tag = LANG_ATTR.sub(r"\1vi\2", tag, count=1)
    if new_tag == tag:
        return text, False
    return text[:m.start()] + new_tag + text[m.end():], True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)

    targets = []
    sd = root / "sources" / "tennis-wiki" / "docs" / "vi"
    if sd.is_dir():
        targets += sorted(sd.rglob("index.html"))
    bt = root / "book" / "TUC"
    if bt.is_dir():
        targets += sorted(bt.glob("chuong-*/index.html"))

    changed = 0
    already = 0
    notag = 0
    for p in targets:
        text = p.read_text(encoding="utf-8", errors="ignore")
        new, did = fix_text(text)
        if not did:
            # distinguish "already vi" from "no <html> tag"
            if HTML_TAG.search(text) and re.search(r'lang\s*=\s*["\']?vi', HTML_TAG.search(text).group(0), re.I):
                already += 1
            else:
                notag += 1
            continue
        changed += 1
        if args.write:
            p.write_text(new, encoding="utf-8", newline="")

    print(f"targets={len(targets)} changed={changed} already_vi={already} no_change={notag} write={args.write}")
    if not args.write:
        print("  (dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
