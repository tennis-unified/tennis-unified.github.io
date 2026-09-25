# -*- coding: utf-8 -*-
"""Replace English catalogue titles with the Vietnamese overrides on VI landing pages
for the articles in the 145-200 batch that were affected."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from vi_title_overrides import EN_TITLE_IN_VI, VI_TITLE_OVERRIDE  # noqa: E402

BASE = r"D:\Github Repos\tennis-unified"
TARGETS = [os.path.join(BASE, "vi", "articles", "index.html"),
           os.path.join(BASE, "vi", "articles", "the-luc", "index.html")]

# only the articles completed in this batch
SCOPE = [163, 171, 179, 180, 181]

for path in TARGETS:
    if not os.path.exists(path):
        print(f"absent: {path}")
        continue
    with open(path, encoding="utf-8") as f:
        c = f.read()
    changes = 0
    for num in SCOPE:
        eng = EN_TITLE_IN_VI[num]
        vie = VI_TITLE_OVERRIDE[num]
        for variant in {eng, eng.replace("&", "&amp;")}:
            n = c.count(variant)
            if n:
                c = c.replace(variant, vie)
                changes += n
    if changes:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(c)
    print(f"{os.path.relpath(path, BASE)}: replaced {changes} title occurrence(s)")

# report residual English catalogue titles from the 1-144 catalogue (out of batch scope)
for path in TARGETS:
    c = open(path, encoding="utf-8").read()
    residual = [n for n, eng in EN_TITLE_IN_VI.items()
                if n not in SCOPE and eng and eng in c]
    print(f"{os.path.relpath(path, BASE)}: residual pre-existing English titles from articles 1-144 -> {residual}")
