# -*- coding: utf-8 -*-
"""Append sitemap entries for articles 145-200 (VI, EN, root mirror) idempotently."""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = r"D:\Github Repos\tennis-unified"
with open(os.path.join(BASE, "scripts", "articles_200_data.json"), encoding="utf-8") as f:
    CAT = json.load(f)

path = os.path.join(BASE, "sitemap.xml")
with open(path, encoding="utf-8") as f:
    xml = f.read()

blocks = []
for num in range(145, 201):
    s_en = CAT["en"][num - 1]["slug"]
    s_vi = CAT["vi"][num - 1]["slug"]
    for url, prio in ((f"https://tennis-unified.github.io/vi/articles/{s_vi}/", "0.8"),
                      (f"https://tennis-unified.github.io/en/articles/{s_en}/", "0.8"),
                      (f"https://tennis-unified.github.io/articles/{s_en}/", "0.6")):
        if f"<loc>{url}</loc>" in xml:
            continue
        blocks.append("  <url>\n"
                      f"    <loc>{url}</loc>\n"
                      "    <changefreq>monthly</changefreq>\n"
                      f"    <priority>{prio}</priority>\n"
                      "  </url>\n")

if blocks:
    xml = xml.replace("</urlset>", "".join(blocks) + "</urlset>")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    print(f"added {len(blocks)} sitemap entries")
else:
    print("sitemap already up to date")

count = xml.count("<url>")
print(f"total sitemap url entries: {count}")
