# -*- coding: utf-8 -*-
"""Audit VI pages of 145-200 for English leakage (titles, headings, cross-references)."""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from vi_title_overrides import EN_TITLE_IN_VI  # noqa: E402

BASE = r"D:\Github Repos\tennis-unified"
with open(os.path.join(BASE, "scripts", "articles_200_data.json"), encoding="utf-8") as f:
    CAT = json.load(f)

VN = set("àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
         "ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ")

problems = []
for num in range(145, 201):
    s_vi = CAT["vi"][num - 1]["slug"]
    path = os.path.join(BASE, "vi", "articles", s_vi, "index.html")
    c = open(path, encoding="utf-8").read()

    title = re.search(r"<title>(.*?)</title>", c).group(1)
    h1 = re.search(r'<h1 id="content">(.*?)</h1>', c).group(1)

    # 1. no leftover "Bài viết 001:" prefix, no double prefix
    if "Bài viết 001" in title or title.count("Bài viết") > 1:
        problems.append((num, "title prefix artifact", title))
    # 2. title and h1 carry Vietnamese diacritics
    if not any(ch in VN for ch in title):
        problems.append((num, "title lacks diacritics", title))
    if not any(ch in VN for ch in h1):
        problems.append((num, "h1 lacks diacritics", h1))
    # 3. no catalogue English title anywhere in the VI body
    # External video citations are proper titles of third-party works; exclude the
    # caption line from the prose-leakage test (site-wide convention on 1-144).
    body = re.sub(r"<p><em>Video minh họa:.*?</em></p>", "", c, flags=re.S)
    body = re.sub(r'<iframe[^>]*title="[^"]*"[^>]*>.*?</iframe>', "", body, flags=re.S)
    for n, eng in EN_TITLE_IN_VI.items():
        if eng and eng in body:
            problems.append((num, f"English catalogue title leaked (article {n})", eng))

if problems:
    print(f"VI leakage problems: {len(problems)}")
    for p in problems[:20]:
        print("  ", p)
else:
    print("VI leakage audit: clean (no prefix artifacts, no English catalogue titles, H1/title accented)")

# spot-print a corrected title and H1
for num in (145, 163, 171, 179, 180, 181):
    s_vi = CAT["vi"][num - 1]["slug"]
    c = open(os.path.join(BASE, "vi", "articles", s_vi, "index.html"), encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", c).group(1)
    h = re.search(r'<h1 id="content">(.*?)</h1>', c).group(1)
    print(f"  {num}: {t}\n       H1: {h}")
