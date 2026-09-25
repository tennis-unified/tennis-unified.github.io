# -*- coding: utf-8 -*-
"""Scan every VI HTML page for residual English catalogue titles (excluding video citations)."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")

from vi_title_overrides import EN_TITLE_IN_VI  # noqa: E402

BASE = r"D:\Github Repos\tennis-unified"
files = []
for root, dirs, names in os.walk(os.path.join(BASE, "vi")):
    if ".git" in root:
        continue
    for n in names:
        if n.endswith(".html"):
            files.append(os.path.join(root, n))

bad = []
for p in files:
    c = open(p, encoding="utf-8", errors="ignore").read()
    c = re.sub(r"<p><em>Video[^<]*</em></p>", "", c)
    c = re.sub(r'<iframe[^>]*title="[^"]*"[^>]*>.*?</iframe>', "", c, flags=re.S)
    for n, eng in EN_TITLE_IN_VI.items():
        if eng and eng in c:
            bad.append((os.path.relpath(p, BASE), n))

print(f"VI HTML files scanned: {len(files)}")
print(f"pages still showing an English catalogue title: {len(bad)}")
for b in bad[:12]:
    print("   ", b)

# spot-check the patched pages
for num, slug in ((34, "VI-tenniskb-kinetic-transfer-from-quad-drive-to-pelvic-acceleration"),
                  (131, "VI-tenniskb-target-zone-heatmaps-perrorxy-spatial-analytics")):
    p = os.path.join(BASE, "vi", "articles", slug, "index.html")
    c = open(p, encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", c).group(1)
    desc = re.search(r'<meta name="description" content="(.*?)"', c).group(1)
    h1 = re.search(r'<h1 id="content">(.*?)</h1>', c).group(1)
    print(f"\narticle {num}:\n  title: {title}\n  desc : {desc}\n  h1   : {h1}")
