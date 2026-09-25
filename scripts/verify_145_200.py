# -*- coding: utf-8 -*-
"""Comprehensive verification for articles 145-200 (VI, EN, root mirror)."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
BASE = r"D:\Github Repos\tennis-unified"
SCRIPTS = os.path.join(BASE, "scripts")

with open(os.path.join(SCRIPTS, "articles_200_data.json"), encoding="utf-8") as f:
    CAT = json.load(f)

VN = set("àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
         "ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ")

EN_HEAD_PATTERNS = ["executive summary", "biomechanical", "step-by-step", "errors, causes",
                    "self-assessment", "printable practice card", "pocket drill card",
                    "performance metrics", "diagnostic diagram", "video demonstration",
                    "cross-domain"]
VN_HEAD_PATTERNS = ["tóm tắt điều hành", "nền tảng cơ sinh học", "trình tự thực thi",
                    "chỉ số hiệu suất", "lỗi thường gặp", "sơ đồ chẩn đoán", "video minh họa",
                    "ứng dụng liên ngành", "bảng tự đánh giá", "thẻ thực hành"]

missing, small, placeholders, fm_leaks = [], [], [], []
en_head_in_vi, vn_text_in_en, vn_text_in_mirror, bad_sections = [], [], [], []
stats = []

for num in range(145, 201):
    s_en = CAT["en"][num - 1]["slug"]
    s_vi = CAT["vi"][num - 1]["slug"]
    paths = [("VI", os.path.join(BASE, "vi", "articles", s_vi, "index.html")),
             ("EN", os.path.join(BASE, "en", "articles", s_en, "index.html")),
             ("Mirror", os.path.join(BASE, "articles", s_en, "index.html"))]
    sizes = {}
    for label, p in paths:
        if not os.path.exists(p):
            missing.append((num, label, p))
            continue
        sz = os.path.getsize(p)
        sizes[label] = sz
        if sz < 15000:
            small.append((num, label, sz))
        content = open(p, encoding="utf-8", errors="ignore").read()
        if "VIDEO_ID_PLACEHOLDER" in content:
            placeholders.append((num, label))
        if "<p>title: " in content or "<p>description: " in content or "<p>author: " in content:
            fm_leaks.append((num, label))
        body = content.split('<article class="md-content__inner md-typeset">')[-1].split("</article>")[0]
        body_no_bc = re.sub(r"<!-- TP-BREADCRUMB-START -->[\s\S]*?<!-- TP-NAV-END -->", "", body)
        text = re.sub(r"<[^>]+>", " ", body_no_bc)
        if label in ("EN", "Mirror"):
            if sum(1 for c in text if c in VN) > 20:
                (vn_text_in_en if label == "EN" else vn_text_in_mirror).append(num)
        else:
            heads = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", content)
            for h in heads:
                hl = re.sub(r"<[^>]+>", "", h).strip().lower()
                if any(p in hl for p in EN_HEAD_PATTERNS):
                    en_head_in_vi.append((num, h.strip()))
            for p in VN_HEAD_PATTERNS:
                if f"<h2>{p}" not in content.lower() and p not in content.lower():
                    bad_sections.append((num, p))
            if sum(1 for c in text if c in VN) < 200:
                bad_sections.append((num, "low-diacritic-density"))
    stats.append((num, sizes.get("VI", 0), sizes.get("EN", 0), sizes.get("Mirror", 0)))

print("================ VERIFICATION 145-200 ================")
print(f"articles checked: {len(stats)}")
print(f"missing files: {len(missing)} {missing[:3]}")
print(f"files under 15KB: {len(small)} {small[:5]}")
print(f"VIDEO_ID_PLACEHOLDER: {len(placeholders)} {placeholders[:5]}")
print(f"frontmatter leaks: {len(fm_leaks)} {fm_leaks[:5]}")
print(f"English headings leaking into VI: {len(en_head_in_vi)} {en_head_in_vi[:5]}")
print(f"VI section/diacritic problems: {len(bad_sections)} {bad_sections[:5]}")
print(f"Vietnamese text in EN: {len(vn_text_in_en)} {vn_text_in_en[:5]}")
print(f"Vietnamese text in Mirror: {len(vn_text_in_mirror)} {vn_text_in_mirror[:5]}")
if stats:
    vi_avg = sum(s[1] for s in stats) / len(stats)
    en_avg = sum(s[2] for s in stats) / len(stats)
    mirror_avg = sum(s[3] for s in stats) / len(stats)
    print(f"average sizes: VI {vi_avg:,.0f} B | EN {en_avg:,.0f} B | Mirror {mirror_avg:,.0f} B")
    print(f"smallest: VI {min(s[1] for s in stats):,} B | EN {min(s[2] for s in stats):,} B")
print("=====================================================")
