import os
import json
import re
import html
import shutil
from pathlib import Path

BASE = Path(r"D:\Github Repos\tennis-unified")

# Load master metadata
with open(BASE / "scripts" / "articles_200_data.json", "r", encoding="utf-8") as f:
    meta_200 = json.load(f)

# Load video map
with open(BASE / "scripts" / "article_video_map_1_144.json", "r", encoding="utf-8") as f:
    video_map = json.load(f)

# Load source mapping
with open(BASE / "scripts" / "article_source_mapping_144.json", "r", encoding="utf-8") as f:
    source_map = json.load(f)

# Extract reference templates
def get_templates(lang="vi"):
    if lang == "vi":
        ref_path = BASE / "vi" / "articles" / "VI-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors" / "index.html"
    else:
        ref_path = BASE / "en" / "articles" / "EN-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors" / "index.html"
    
    with open(ref_path, "r", encoding="utf-8") as f:
        content = f.read()

    marker_start = '<article class="md-content__inner md-typeset">'
    marker_end = '</article>'
    start_idx = content.find(marker_start)
    end_idx = content.find(marker_end, start_idx)

    head = content[:start_idx]
    foot = content[end_idx + len(marker_end):]
    return head, foot

head_vi_raw, foot_vi_raw = get_templates("vi")
head_en_raw, foot_en_raw = get_templates("en")

# Pillar slug mappings
pillar_urls_vi = {
    "biomechanics": ("co-sinh-hoc", "Cơ Sinh Học Ứng Dụng & Động Lực Học"),
    "neuro-athletics": ("than-kinh", "Thần Kinh Thể Thao & Nhận Thức"),
    "stroke-mechanics": ("cu-danh", "Cơ Học Cú Đánh & Kỹ Thuật"),
    "tactics": ("chien-thuat", "Chiến Thuật, Hình Học & Meta Trận Đấu"),
    "conditioning": ("the-luc", "Thể Lực, Phục Hồi & Trạng Thái Flow")
}

pillar_urls_en = {
    "biomechanics": ("biomechanics", "Applied Biomechanics & Kinetics"),
    "neuro-athletics": ("neuro-athletics", "Neuro-Athletics & Cognition"),
    "stroke-mechanics": ("stroke-mechanics", "Stroke Mechanics & Production"),
    "tactics": ("tactics", "Tactics, Geometry & Game Meta"),
    "conditioning": ("conditioning", "Conditioning, Recovery & Flow")
}

# Diacritics and heading cleaning dictionaries
VN_SECTION_TITLES = {
    r"(?i)(?:^#+\s*|\b)1\.?\s*(?:Tóm\s*Tắt\s*Điều\s*Hành|Executive\s*Summary).*": "1. Tóm Tắt Điều Hành & Ý Đồ Thể Thao",
    r"(?i)(?:^#+\s*|\b)2\.?\s*(?:Nền\s*Tảng\s*Sinh\s*Học\s*Cơ|Nền\s*Tảng\s*Cơ\s*Sinh\s*Học|Biomechanical\s*Foundation).*": "2. Nền Tảng Cơ Sinh Học & Thần Kinh Học",
    r"(?i)(?:^#+\s*|\b)3\.?\s*(?:Thực\s*Hành\s*Kỹ\s*Thuật\s*Từng\s*Bước|Trình\s*Tự\s*Thực\s*Thi|Step-by-Step\s*Technical\s*Execution).*": "3. Trình Tự Thực Thi Kỹ Thuật (Checkpoints)",
    r"(?i)(?:^#+\s*|\b)4\.?\s*(?:Chỉ\s*Số\s*Hiệu\s*Suất|Liều\s*Lượng|Performance\s*Metrics).*": "4. Chỉ Số Hiệu Suất & Liều Lượng Huấn Luyện",
    r"(?i)(?:^#+\s*|\b)5\.?\s*(?:Lỗi,?\s*Nguyên\s*Nhân|Lỗi\s*Thường\s*Gặp|Errors,?\s*Causes).*": "5. Lỗi Thường Gặp, Nguyên Nhân & Giao Thức Khắc Phục",
    r"(?i)(?:^#+\s*|\b)6\.?\s*(?:Sơ\s*Đồ\s*Chẩn\s*Đoán|Hiệp\s*Đồng\s*Liên\s*Miền|Diagnostic\s*Diagram|Cross-Domain\s*Synergy).*": "6. Sơ Đồ Chẩn Đoán & Ra Quyết Định",
    r"(?i)(?:^#+\s*|\b)7\.?\s*(?:Video\s*Minh\s*Họa|Video\s*Demonstration).*": "7. Video Minh Họa & Phân Tích Kỹ Thuật",
    r"(?i)(?:^#+\s*|\b)8\.?\s*(?:Ứng\s*Dụng\s*Liên\s*Ngành|Ma\s*Trận\s*Tự\s*Đánh\s*Giá|Self-Assessment\s*Matrix).*": "8. Ứng Dụng Liên Ngành & Phối Hợp Đa Trụ Cột",
    r"(?i)(?:^#+\s*|\b)9\.?\s*(?:Bảng\s*Tự\s*Đánh\s*Giá|Thẻ\s*Tập\s*Luyện|Printable\s*Practice\s*Card).*": "9. Bảng Tự Đánh Giá (Rubric Đa Cấp Độ)",
    r"(?i)(?:^#+\s*|\b)10\.?\s*(?:Thẻ\s*Thực\s*Hành\s*In\s*Sổ\s*Tay|Thẻ\s*Tập\s*Luyện|Pocket\s*Card).*": "10. Thẻ Thực Hành In Sổ Tay (Pocket Drill Card)"
}

DIACRITICS_FIXES = [
    ("Phan Tich Du Lieu Tennis", "Phân Tích Dữ Liệu Tennis"),
    ("Thong Ke Tran Dau", "Thống Kê Trận Đấu"),
    ("Chi So Hieu Suat", "Chỉ Số Hiệu Suất"),
    ("Xoay Than Nguyen Khoi", "Xoay Thân Nguyên Khối"),
    ("Hinh Hoc Diem Tiep Xuc", "Hình Học Điểm Tiếp Xúc"),
    ("Co Hoc Cu Danh", "Cơ Học Cú Đánh"),
    ("Ky Thuat Danh Bong", "Kỹ Thuật Đánh Bóng"),
    ("Nen Tang Sinh Hoc Co", "Nền Tảng Cơ Sinh Học"),
    ("Loi Quan Sat Duoc", "Lỗi Quan Sát Được"),
    ("Nguyen Nhan Goc", "Nguyên Nhân Gốc Rễ"),
    ("Giao Thuc Khac Phuc", "Giao Thức Khắc Phục"),
    ("Chi So", "Chỉ Số"),
    ("Muc Tieu", "Mục Tiêu"),
    ("Dang Phat Trien", "Đang Phát Triển"),
    ("Dat Chuan", "Đạt Chuẩn"),
    ("Nang Cao", "Nâng Cao"),
    ("Dang Cap", "Đẳng Cấp (ATP/WTA)"),
    ("Lieulieu Luong", "Liều Lượng"),
    ("Tuan", "Tuần"),
    ("Khoi", "Khối"),
    ("Tan Suat", "Tần Suất"),
    ("Cong", "Cổng Đánh Giá"),
    ("Ma Tran Tu Danh Gia", "Ma Trận Tự Đánh Giá"),
    ("Ma Tran", "Ma Trận"),
    ("Tu Danh Gia", "Tự Đánh Giá"),
    ("Thuc Hanh Ky Thuat Tung Buoc", "Thực Hành Kỹ Thuật Từng Bước"),
    ("Thuc Hanh", "Thực Hành"),
    ("Tung Buoc", "Từng Bước"),
    ("Giai Doan", "Giai Đoạn"),
    ("Trinh Bay", "Trình Bày"),
    ("The Tap Luyen", "Thẻ Tập Luyện"),
    ("In So Tay", "In Sổ Tay"),
    ("Tom Tat", "Tóm Tắt"),
    ("Dieu Hanh", "Điều Hành"),
    ("Y Dinh", "Ý Định"),
    ("The Thao", "Thể Thao"),
    ("Nen Tang", "Nền Tảng"),
    ("Than Kinh Hoc", "Thần Kinh Học"),
    ("Loi Thuong Gap", "Lỗi Thường Gặp"),
    ("So Do Chan Doan", "Sơ Đồ Chẩn Đoán"),
    ("Quyet Dinh", "Quyết Định"),
    ("Explicit Decision Tree (Cây Quyết Định Tường Minh)", "Cây Quyết Định Tường Minh (Explicit Decision Tree)"),
    ("Visual Performance Metrics Dưới Biến Thể Ánh Sáng", "Chỉ Số Hiệu Suất Thị Giác Dưới Biến Thể Ánh Sáng"),
    ("Footwork Pattern Decision Tree", "Cây Quyết Định Mẫu Bộ Pháp (Footwork Pattern Decision Tree)"),
    ("Tactical Adjustment Decision Tree (Cây Quyết Định Điều Chỉnh Chiến Thuật)", "Cây Quyết Định Điều Chỉnh Chiến Thuật (Tactical Adjustment Decision Tree)")
]

def strip_frontmatter(text):
    """Cleanly strip YAML frontmatter even with BOM, spaces, or diverse newlines."""
    text = text.lstrip("\ufeff \t\r\n")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\r\n")
    return text

def md_to_html(md_text):
    """Convert Markdown to HTML with tables, code, blockquotes, lists, and LaTeX preservation."""
    lines = md_text.split('\n')
    output = []
    in_table = False
    table_rows = []
    in_list = False
    in_code = False
    code_block = []

    def flush_table():
        nonlocal in_table, table_rows
        if not table_rows:
            in_table = False
            return
        html_tbl = ['<table>', '<thead><tr>']
        headers = [c.strip() for c in table_rows[0].split('|') if c.strip()]
        for h in headers:
            html_tbl.append(f'<th style="text-align: left;">{h}</th>')
        html_tbl.append('</tr></thead><tbody>')
        for r in table_rows[2:]:
            cells = [c.strip() for c in r.split('|') if c.strip()]
            if cells:
                html_tbl.append('<tr>')
                for c in cells:
                    html_tbl.append(f'<td style="text-align: left;">{c}</td>')
                html_tbl.append('</tr>')
        html_tbl.append('</tbody></table>')
        output.append('\n'.join(html_tbl))
        table_rows = []
        in_table = False

    def flush_list():
        nonlocal in_list
        if in_list:
            output.append('</ul>')
            in_list = False

    def flush_code():
        nonlocal in_code, code_block
        if in_code:
            output.append('<pre><code>' + html.escape('\n'.join(code_block)) + '</code></pre>')
            code_block = []
            in_code = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('```'):
            if in_code:
                flush_code()
            else:
                flush_table()
                flush_list()
                in_code = True
            continue

        if in_code:
            code_block.append(line)
            continue

        if stripped.startswith('|') and stripped.endswith('|'):
            flush_list()
            in_table = True
            table_rows.append(stripped)
            continue
        elif in_table:
            flush_table()

        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                output.append('<ul>')
                in_list = True
            item_text = stripped[2:]
            output.append(f'<li>{item_text}</li>')
            continue
        elif in_list:
            flush_list()

        if stripped.startswith('#### '):
            output.append(f'<h4>{stripped[5:]}</h4>')
            continue
        if stripped.startswith('### '):
            output.append(f'<h3>{stripped[4:]}</h3>')
            continue
        if stripped.startswith('## '):
            output.append(f'<h2>{stripped[3:]}</h2>')
            continue
        if stripped.startswith('# '):
            continue

        if stripped.startswith('> '):
            quote_text = stripped[2:]
            output.append(f'<blockquote>\n<p>{quote_text}</p>\n</blockquote>')
            continue

        if stripped in ('---', '***', '___'):
            output.append('<hr />')
            continue

        if stripped.startswith('<div class="video-container"') or stripped.startswith('<iframe') or stripped.startswith('</div>'):
            output.append(line)
            continue

        if stripped:
            output.append(f'<p>{line}</p>')
        else:
            output.append('')

    if in_table:
        flush_table()
    if in_list:
        flush_list()
    if in_code:
        flush_code()

    res = '\n'.join(output)
    res = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', res)
    res = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', res)
    return res

def clean_vietnamese_markdown(md_text, article_num, vid_info):
    """Clean English leaks and diacritics in Vietnamese markdown."""
    text = strip_frontmatter(md_text)

    # Fix known unaccented phrases
    for wrong, right in DIACRITICS_FIXES:
        text = text.replace(wrong, right)

    # Fix section headers
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        stripped = line.strip()
        matched = False
        if stripped.startswith("## ") or stripped.startswith("### "):
            header_content = re.sub(r"^#+\s*", "", stripped)
            for pattern, canonical_title in VN_SECTION_TITLES.items():
                if re.match(pattern, header_content):
                    cleaned_lines.append(f"## {canonical_title}")
                    matched = True
                    break
        if not matched:
            cleaned_lines.append(line)
    text = "\n".join(cleaned_lines)

    # Fix table headers that are in English
    table_replacements = [
        (r"\|\s*Observable Error\s*\|\s*Root Cause\s*\|\s*Correction Protocol\s*\|",
         "| Lỗi Quan Sát Được | Nguyên Nhân Gốc Rễ | Giao Thức Khắc Phục |"),
        (r"\|\s*Metric\s*\|\s*Club Target\s*\|\s*Collegiate Target\s*\|\s*Pro Target\s*\|",
         "| Chỉ Số | Mục Tiêu CLB | Mục Tiêu Đại Học | Mục Tiêu Đẳng Cấp ATP/WTA |"),
        (r"\|\s*Phase\s*\|\s*Technical Name\s*\|\s*Primary Biomechanics\s*\|\s*Timing\s*\|\s*KPI\s*\|",
         "| Pha | Tên Kỹ Thuật | Cơ Sinh Học Chính | Thời Gian | KPI Đạt Chuẩn |"),
        (r"\|\s*Checkpoint\s*\|\s*Pass\s*\|\s*Leak\s*\|",
         "| Điểm Kiểm Tra | Đạt Chuẩn | Rò Rỉ Động Lực |"),
        (r"\|\s*Level 1\s*\|\s*Level 2\s*\|\s*Level 3\s*\|\s*Level 4\s*\|",
         "| Mức 1 (Cơ Bản) | Mức 2 (Chuyển Tiếp) | Mức 3 (Chức Năng Hiện Đại) | Mức 4 (Đẳng Cấp ATP) |")
    ]
    for pattern, repl in table_replacements:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)

    # Video container
    vid_id = vid_info["video_id"]
    vid_title = vid_info["title"]
    vid_channel = vid_info["channel"]
    
    video_html = f'''<div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 8px; margin: 1.5rem 0;">
  <iframe src="https://www.youtube-nocookie.com/embed/{vid_id}" title="{html.escape(vid_title)}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>
<p><em>Video: {html.escape(vid_title)} ({html.escape(vid_channel)}).</em></p>'''

    if "VIDEO_ID_PLACEHOLDER" in text:
        text = re.sub(r'<div class="video-container"[\s\S]*?</div>\s*(?:<p><em>[^<]*</em></p>)?', video_html, text)
        text = text.replace("VIDEO_ID_PLACEHOLDER", vid_id)
    elif "<div class=\"video-container\"" not in text:
        # inject after Pro Cue
        cue_match = re.search(r'(>[\s\S]*?\n\n)', text)
        if cue_match:
            end_pos = cue_match.end()
            text = text[:end_pos] + video_html + "\n\n" + text[end_pos:]
        else:
            text = video_html + "\n\n" + text

    # Ensure Pro Cue is properly styled
    text = re.sub(r'>\s*\*\*PRO CUE:\*\*', '> **CUE CHUYÊN GIA:**', text)
    return text

print("Deployment engine ready to execute.")
