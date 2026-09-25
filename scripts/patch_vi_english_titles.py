# -*- coding: utf-8 -*-
"""Replace the 20 remaining English catalogue titles (articles 34-43, 51, 53, 57, 60,
69, 70, 96, 119, 131, 134) with Vietnamese titles across every VI HTML page that
displays them: their own article pages, the article index, and the pillar indexes.

Usage:
    python patch_vi_english_titles.py            # dry run, report only
    python patch_vi_english_titles.py --apply    # write changes
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from vi_title_overrides import EN_TITLE_IN_VI, VI_TITLE_OVERRIDE  # noqa: E402

BASE = r"D:\Github Repos\tennis-unified"
APPLY = "--apply" in sys.argv

TARGETS = [34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 51, 53, 57, 60, 69, 70, 96, 119, 131, 134]

# every VI html page under vi/ (bounded: index + article pages + pillar pages)
files = []
for root, dirs, names in os.walk(os.path.join(BASE, "vi")):
    if ".git" in root:
        continue
    for n in names:
        if n.endswith(".html"):
            files.append(os.path.join(root, n))

total = 0
touched = []
residual = []
for path in files:
    with open(path, "rb") as f:
        raw = f.read()
    crlf = raw.count(b"\r\n") > 0
    c = raw.decode("utf-8", errors="ignore")
    original = c
    per_file = 0

    for num in TARGETS:
        eng = EN_TITLE_IN_VI[num]
        vie = VI_TITLE_OVERRIDE[num]
        if not eng:
            continue
        for variant in {eng, eng.replace("&", "&amp;")}:
            # 1. fix the wrong hard-coded "Bài viết 001:" prefix together with the title
            fixed_prefix = f"Bài viết 001: {variant}"
            if fixed_prefix in c:
                c = c.replace(fixed_prefix, f"Bài viết {num}: {vie}")
                per_file += 1
            # 2. remaining occurrences (H1, breadcrumb, cross-reference bullets)
            if variant in c:
                per_file += c.count(variant)
                c = c.replace(variant, vie)

    if c != original:
        touched.append((os.path.relpath(path, BASE), per_file))
        total += per_file
        if APPLY:
            # preserve the original line ending style so the diff stays minimal
            out = c.replace("\r\n", "\n")
            if crlf:
                out = out.replace("\n", "\r\n")
            with open(path, "wb") as f:
                f.write(out.encode("utf-8"))

print(f"{'APPLIED' if APPLY else 'DRY RUN'}: {len(touched)} file(s), {total} replacement(s)")
for p, n in sorted(touched):
    print(f"  {n:3d}  {p}")

# confirm nothing is left
for path in files:
    with open(path, encoding="utf-8", errors="ignore") as f:
        c = f.read()
    for num in TARGETS:
        eng = EN_TITLE_IN_VI[num]
        if eng and eng in c:
            residual.append((os.path.relpath(path, BASE), num))
if residual:
    print(f"residual English titles: {len(residual)}")
    for r in residual[:10]:
        print("  ", r)
else:
    print("residual English titles: none")
