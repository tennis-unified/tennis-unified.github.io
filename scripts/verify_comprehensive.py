import os
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = r"D:\Github Repos\tennis-unified"
with open(os.path.join(base, "scripts", "articles_200_data.json"), encoding="utf-8") as f:
    meta_200 = json.load(f)

vi_dir = os.path.join(base, "vi", "articles")
en_dir = os.path.join(base, "en", "articles")
mirror_dir = os.path.join(base, "articles")

vn_diacritics = set("àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
                    "ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ")

en_heading_patterns = [
    'executive summary', 'biomechanical foundation', 'step-by-step technical', 'errors, causes',
    'self-assessment matrix', 'self-assessment rubric', 'printable practice card', 'pocket drill card'
]

missing_files = []
small_files = []
placeholder_count = 0
frontmatter_leaks = []
en_heading_leaks_in_vi = []
vn_leaks_in_en = []
vn_leaks_in_mirror = []

for i in range(1, 145):
    m_en = meta_200["en"][i-1]
    m_vi = meta_200["vi"][i-1]
    s_en = m_en["slug"]
    s_vi = m_vi["slug"]

    p_vi = os.path.join(vi_dir, s_vi, "index.html")
    p_en = os.path.join(en_dir, s_en, "index.html")
    p_mirror = os.path.join(mirror_dir, s_en, "index.html")

    for p, label in [(p_vi, "VI"), (p_en, "EN"), (p_mirror, "Mirror")]:
        if not os.path.exists(p):
            missing_files.append((i, label, p))
            continue
        sz = os.path.getsize(p)
        if sz < 15000:
            small_files.append((i, label, sz))

        content = open(p, "r", encoding="utf-8", errors="ignore").read()

        if "VIDEO_ID_PLACEHOLDER" in content:
            placeholder_count += 1

        if "<p>title: " in content or "<p>description: " in content or "<p>author: " in content:
            frontmatter_leaks.append((i, label))

        # Check for VN leaks in EN / Mirror
        if label in ["EN", "Mirror"]:
            marker = '<article class="md-content__inner md-typeset">'
            body = content.split(marker)[-1].split('</article>')[0] if marker in content else content
            # Remove breadcrumbs
            body = re.sub(r'<!-- TP-BREADCRUMB-START -->[\s\S]*?<!-- TP-NAV-END -->', '', body)
            clean_body = re.sub(r'<[^>]+>', ' ', body)
            vn_chars = sum(1 for c in clean_body if c in vn_diacritics)
            if vn_chars > 20:
                if label == "EN":
                    vn_leaks_in_en.append((i, vn_chars))
                else:
                    vn_leaks_in_mirror.append((i, vn_chars))

    # Check for EN leaks in VI
    if os.path.exists(p_vi):
        vi_c = open(p_vi, "r", encoding="utf-8", errors="ignore").read()
        h2s = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', vi_c)
        for h in h2s:
            clean_h = re.sub(r'<[^>]+>', '', h).strip().lower()
            for pat in en_heading_patterns:
                if pat in clean_h:
                    en_heading_leaks_in_vi.append((i, h))

print("================ FINAL COMPREHENSIVE AUDIT ================")
print(f"Total articles audited: 144 across VI, EN, Mirror (432 files)")
print(f"Missing HTML files: {len(missing_files)}")
print(f"Files under 15KB: {len(small_files)}")
if small_files:
    print(f"Small files sample: {small_files[:5]}")
print(f"VIDEO_ID_PLACEHOLDER occurrences: {placeholder_count}")
print(f"Frontmatter leak occurrences: {len(frontmatter_leaks)}")
if frontmatter_leaks:
    print(f"Frontmatter leaks sample: {frontmatter_leaks[:5]}")
print(f"English heading leaks in VI: {len(en_heading_leaks_in_vi)}")
if en_heading_leaks_in_vi:
    print(f"EN heading leaks in VI sample: {en_heading_leaks_in_vi[:5]}")
print(f"Vietnamese text leaks in EN: {len(vn_leaks_in_en)}")
if vn_leaks_in_en:
    print(f"VN leaks in EN sample: {vn_leaks_in_en[:5]}")
print(f"Vietnamese text leaks in Mirror: {len(vn_leaks_in_mirror)}")
if vn_leaks_in_mirror:
    print(f"VN leaks in Mirror sample: {vn_leaks_in_mirror[:5]}")
print("===========================================================")
