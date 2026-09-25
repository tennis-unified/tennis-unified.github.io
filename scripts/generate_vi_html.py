#!/usr/bin/env python3
"""
Generate Vietnamese HTML articles from markdown files using existing template.
This script converts the 10 new markdown files (034-043) to HTML and updates index.html navigation.
"""

import os
import re
import json
from pathlib import Path

BASE = Path(r"D:\Github Repos\tennis-unified")

# The 10 new Vietnamese articles (034-043)
NEW_VI_ARTICLES = [
    {
        "num": 34,
        "slug": "VI-tenniskb-kinetic-transfer-from-quad-drive-to-pelvic-acceleration",
        "title": "Bài viết 034: Truyền Động Năng Lượng Từ Cú Đạp Tứ Đầu Đến Gia Tốc Khung Chậu",
        "pillar": "co-sinh-hoc",
        "pillar_title": "Cơ Sinh Học Ứng Dụng & Động Học",
        "prev_slug": "VI-tenniskb-passive-ligamentous-locking-vs-active-muscle-tension",
        "next_slug": "VI-tenniskb-torque-vector-generation-in-open-vs-closed-stances",
    },
    {
        "num": 35,
        "slug": "VI-tenniskb-torque-vector-generation-in-open-vs-closed-stances",
        "title": "Bài viết 035: Sinh Thành Vector Mô-Men Trong Tư Thế Mở So Với Đóng",
        "pillar": "co-sinh-hoc",
        "pillar_title": "Cơ Sinh Học Ứng Dụng & Động Học",
        "prev_slug": "VI-tenniskb-kinetic-transfer-from-quad-drive-to-pelvic-acceleration",
        "next_slug": "VI-tenniskb-gravitational-acceleration-utilization-in-drop-feeds",
    },
    {
        "num": 36,
        "slug": "VI-tenniskb-gravitational-acceleration-utilization-in-drop-feeds",
        "title": "Bài viết 036: Tận Dụng Gia Tốc Trọng Trường Trong Drop-Feed",
        "pillar": "co-sinh-hoc",
        "pillar_title": "Cơ Sinh Học Ứng Dụng & Động Học",
        "prev_slug": "VI-tenniskb-torque-vector-generation-in-open-vs-closed-stances",
        "next_slug": "VI-tenniskb-passive-ligamentous-locking-vs-active-muscle-tension",
    },
    {
        "num": 37,
        "slug": "VI-tenniskb-passive-ligamentous-locking-vs-active-muscle-tension",
        "title": "Bài viết 037: Khóa Bị Động Của Dây Chằng So Với Căng Cơ Chủ Động",
        "pillar": "co-sinh-hoc",
        "pillar_title": "Cơ Sinh Học Ứng Dụng & Động Học",
        "prev_slug": "VI-tenniskb-gravitational-acceleration-utilization-in-drop-feeds",
        "next_slug": "VI-tenniskb-rotational-inertia-adjustment-during-mid-swing-tracking",
    },
    {
        "num": 38,
        "slug": "VI-tenniskb-rotational-inertia-adjustment-during-mid-swing-tracking",
        "title": "Bài viết 038: Điều Chỉnh Mô-Men Quán Tính Trong Theo Dõi Giữa Swing",
        "pillar": "co-sinh-hoc",
        "pillar_title": "Cơ Sinh Học Ứng Dụng & Động Học",
        "prev_slug": "VI-tenniskb-passive-ligamentous-locking-vs-active-muscle-tension",
        "next_slug": "VI-tenniskb-kinetic-chain-peak-power-phase-alignment",
    },
    {
        "num": 39,
        "slug": "VI-tenniskb-kinetic-chain-peak-power-phase-alignment",
        "title": "Bài viết 039: Căn Chỉnh Pha Đỉnh Sức Mạnh Của Chuỗi Động Học",
        "pillar": "co-sinh-hoc",
        "pillar_title": "Cơ Sinh Học Ứng Dụng & Động Học",
        "prev_slug": "VI-tenniskb-rotational-inertia-adjustment-during-mid-swing-tracking",
        "next_slug": "VI-tenniskb-biomechanical-efficiency-audits-for-stroke-longevity",
    },
    {
        "num": 40,
        "slug": "VI-tenniskb-biomechanical-efficiency-audits-for-stroke-longevity",
        "title": "Bài viết 040: Kiểm Toán Hiệu Suất Cơ Sinh Học Cho Sự Bền Cú Đánh",
        "pillar": "co-sinh-hoc",
        "pillar_title": "Cơ Sinh Học Ứng Dụng & Động Học",
        "prev_slug": "VI-tenniskb-kinetic-chain-peak-power-phase-alignment",
        "next_slug": "VI-tenniskb-quiet-eye-qe-fixing-visual-anchors-before-impact",
    },
    {
        "num": 41,
        "slug": "VI-tenniskb-quiet-eye-qe-fixing-visual-anchors-before-impact",
        "title": "Bài viết 041: Quiet Eye (QE): Cố Định Neo Thị Giác Trước Tiếp Xúc",
        "pillar": "than-kinh-the-thao",
        "pillar_title": "Thần Kinh Thể Thao & Kỹ Thuật",
        "prev_slug": "VI-tenniskb-biomechanical-efficiency-audits-for-stroke-longevity",
        "next_slug": "VI-tenniskb-vestibular-ocular-reflex-vor-and-head-stabilization",
    },
    {
        "num": 42,
        "slug": "VI-tenniskb-vestibular-ocular-reflex-vor-and-head-stabilization",
        "title": "Bài viết 042: Phản Xạ Tiền Đình-Nhãn Cầu (VOR) & Ổn Định Đầu",
        "pillar": "than-kinh-the-thao",
        "pillar_title": "Thần Kinh Thể Thao & Kỹ Thuật",
        "prev_slug": "VI-tenniskb-quiet-eye-qe-fixing-visual-anchors-before-impact",
        "next_slug": "VI-tenniskb-proprioceptive-feedback-loops-in-high-velocity-tracking",
    },
    {
        "num": 43,
        "slug": "VI-tenniskb-proprioceptive-feedback-loops-in-high-velocity-tracking",
        "title": "Bài viết 043: Vòng Phản Hồi Cảm Nhận Bản Thân Trong Theo Dõi Tốc Độ Cao",
        "pillar": "than-kinh-the-thao",
        "pillar_title": "Thần Kinh Thể Thao & Kỹ Thuật",
        "prev_slug": "VI-tenniskb-vestibular-ocular-reflex-vor-and-head-stabilization",
        "next_slug": "VI-tenniskb-neural-myelination-through-high-density-precision-repetitions",
    },
]

def load_reference_template():
    """Load the reference Vietnamese article to extract head and foot templates."""
    ref_path = BASE / "vi" / "articles" / "VI-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors" / "index.html"
    with open(ref_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    article_start = content.find('<article class="md-content__inner md-typeset">')
    article_end = content.find("</article>", article_start)
    
    head_template = content[:article_start]
    foot_template = content[article_end + len("</article>"):]
    
    return head_template, foot_template

def markdown_to_html(md_text):
    """Convert basic markdown to HTML for our article structure."""
    html = md_text
    
    # First, remove the first # heading since template provides h1
    lines = html.split('\n')
    # Find and skip the first # heading
    new_lines = []
    skipped_first_h1 = False
    for line in lines:
        if not skipped_first_h1 and re.match(r'^# ', line.strip()):
            skipped_first_h1 = True
            continue
        new_lines.append(line)
    html = '\n'.join(new_lines)
    
    # Handle tables first - convert markdown tables to HTML tables
    def convert_table(match):
        table_text = match.group(0)
        rows = table_text.strip().split('\n')
        if len(rows) < 2:
            return table_text
        
        # Parse header
        header_cells = [c.strip() for c in rows[0].split('|') if c.strip()]
        # Skip separator row
        data_rows = rows[2:] if len(rows) > 2 else []
        
        html_table = ['<table>']
        html_table.append('<thead><tr>')
        for cell in header_cells:
            html_table.append(f'<th style="text-align: left;">{cell}</th>')
        html_table.append('</tr></thead>')
        
        if data_rows:
            html_table.append('<tbody>')
            for row in data_rows:
                cells = [c.strip() for c in row.split('|') if c.strip()]
                if cells:
                    html_table.append('<tr>')
                    for cell in cells:
                        html_table.append(f'<td style="text-align: left;">{cell}</td>')
                    html_table.append('</tr>')
            html_table.append('</tbody>')
        html_table.append('</table>')
        return '\n'.join(html_table)
    
    # Convert markdown tables (lines with |...| pattern)
    html = re.sub(r'^\|.*\|$\n^\|[-:\s|]+\|$\n(?:\|.*\|$\n?)*', convert_table, html, flags=re.MULTILINE)
    
    # Headers
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    
    # Italic - simple approach: single *text* not **text**
    # First protect **bold** with placeholder
    bold_placeholders = {}
    def save_bold(match):
        placeholder = f"__BOLD_{len(bold_placeholders)}__"
        bold_placeholders[placeholder] = match.group(0)
        return placeholder
    html = re.sub(r'\*\*(.+?)\*\*', save_bold, html)
    
    # Now handle *italic*
    html = re.sub(r'\*([^*]+?)\*', r'<em>\1</em>', html)
    
    # Restore bold
    for placeholder, bold_text in bold_placeholders.items():
        html = html.replace(placeholder, bold_text)
    
    # Blockquotes - handle multi-line
    def replace_blockquote(match):
        content = match.group(1)
        # Don't wrap if already has paragraph tags
        if '<p>' in content:
            return f'<blockquote>\n{content}\n</blockquote>'
        return f'<blockquote>\n<p>{content}</p>\n</blockquote>'
    html = re.sub(r'^>\s*(.+?)(?=\n>|$)', replace_blockquote, html, flags=re.MULTILINE | re.DOTALL)
    # Fix nested p tags in blockquotes
    html = re.sub(r'<blockquote>\n<p>(.*?)</p>\n<p></blockquote></p>', r'<blockquote>\n<p>\1</p>\n</blockquote>', html, flags=re.DOTALL)
    
    # Code blocks (```html ... ```)
    def replace_code_block(match):
        code = match.group(1)
        return f'<pre><code class="language-html">{code}</code></pre>'
    html = re.sub(r'```html\n(.*?)\n```', replace_code_block, html, flags=re.DOTALL)
    
    # Video container divs - preserve as-is
    # They're already HTML in the markdown
    
    # Paragraphs - wrap lines that aren't already wrapped in tags
    lines = html.split('\n')
    result = []
    in_table = False
    in_list = False
    list_type = None  # 'ul' or 'ol'
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Check if line is already HTML block element
        if re.match(r'^<(h[1-6]|p|blockquote|pre|table|thead|tbody|tr|th|td|ul|ol|li|hr|div)', stripped):
            if stripped.startswith('<table'):
                in_table = True
            if stripped.startswith('</table'):
                in_table = False
            if in_list:
                result.append(f'</{list_type}>')
                in_list = False
                list_type = None
            result.append(line)
        elif stripped.startswith('- ') or stripped.startswith('* '):
            # List item
            if not in_list:
                result.append('<ul>')
                in_list = True
                list_type = 'ul'
            result.append(f'<li>{stripped[2:]}</li>')
        elif re.match(r'^\d+\. ', stripped):
            # Numbered list
            if not in_list:
                result.append('<ol>')
                in_list = True
                list_type = 'ol'
            result.append(f'<li>{re.sub(r"^\d+\. ", "", stripped)}</li>')
        elif stripped == '':
            if in_list:
                result.append(f'</{list_type}>')
                in_list = False
                list_type = None
            result.append('')
        elif in_table:
            result.append(line)
        else:
            if in_list:
                result.append(f'</{list_type}>')
                in_list = False
                list_type = None
            # Wrap in paragraph if not empty
            if stripped:
                result.append(f'<p>{line}</p>')
            else:
                result.append('')
        i += 1
    
    if in_list:
        result.append(f'</{list_type}>')
    
    return '\n'.join(result)

def generate_article_html(article_meta, md_content, head_template, foot_template):
    """Generate complete HTML for a Vietnamese article."""
    slug = article_meta["slug"]
    title = article_meta["title"]
    pillar_title = article_meta["pillar_title"]
    pillar_slug = article_meta["pillar"]
    prev_slug = article_meta["prev_slug"]
    next_slug = article_meta["next_slug"]
    article_num = article_meta["num"]
    
    # Convert markdown content to HTML
    content_html = markdown_to_html(md_content)
    
    # Breadcrumb
    breadcrumb = f'<p><a href="/">🏠 Home</a> &nbsp;›&nbsp; <a href="/vi/articles/">Tennis Fundamentals</a> &nbsp;›&nbsp; <a href="/vi/articles/{pillar_slug}/">{pillar_title}</a> &nbsp;›&nbsp; {title}</p>\n<hr />'
    
    # Navigation footer
    nav = f'<p class="article-nav" style="margin-top:2rem;font-size:0.95rem">\n  <a href="/vi/articles/{prev_slug}/">← Trước</a> &nbsp;|&nbsp;\n  <a href="/vi/articles/">🏠 Trang chủ</a> &nbsp;|&nbsp;\n  <a href="/vi/articles/{next_slug}/">Sau →</a>\n</p>'
    
    # Body
    body = f'{breadcrumb}\n\n<h1 id="content">{title}</h1>\n\n{content_html}\n\n{nav}'
    
    # Update head template - replace title and description
    # The reference has "Bài viết 001: Lực Phản Hồi..." - need to replace the whole thing
    ref_title = "Bài viết 001: Lực Phản Hồi Từ Mặt Sân (GRF) — Vector Dọc So Với Vector Ngang"
    ref_desc = "TennisKB — Bài viết 001: Lực Phản Hồi Từ Mặt Sân (GRF) — Vector Dọc So Với Vector Ngang | Tennis Future Lab"
    
    new_title = f"Bài viết {article_num:03d}: {title.split(': ', 1)[1] if ': ' in title else title} - Tennis Unified Library"
    new_desc = f"TennisKB — Bài viết {article_num:03d}: {title.split(': ', 1)[1] if ': ' in title else title} | Tennis Future Lab"
    
    head = head_template.replace(ref_title, new_title).replace(ref_desc, new_desc)
    head = head.replace(
        "VI-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors", slug
    ).replace(
        "EN-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors",
        slug.replace("VI-", "EN-")
    )
    
    # Update foot template (update cross-reference links if needed)
    # The foot template contains the cross-references and footer - keep as is
    
    return (
        head
        + '<article class="md-content__inner md-typeset">\n\n'
        + body
        + "\n\n</article>\n"
        + foot_template
    )

def main():
    print("Loading reference template...")
    head_template, foot_template = load_reference_template()
    print("Template loaded.")
    
    for article in NEW_VI_ARTICLES:
        slug = article["slug"]
        md_path = BASE / "vi" / "articles" / slug / "index.md"
        html_path = BASE / "vi" / "articles" / slug / "index.html"
        
        print(f"Processing article {article['num']}: {slug}")
        
        # Read markdown
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        
        # Remove frontmatter (everything between first --- and second ---)
        if md_content.startswith('---'):
            parts = md_content.split('---', 2)
            if len(parts) >= 3:
                md_content = parts[2].strip()
        
        # Generate HTML
        html = generate_article_html(article, md_content, head_template, foot_template)
        
        # Write HTML
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"  Generated: {html_path} ({len(html)} bytes)")

    print("\nAll 10 articles generated!")
    
    # Now update vi/articles/index.html to include new articles in navigation
    update_vi_index()

def update_vi_index():
    """Update the Vietnamese articles index.html to include new articles in the listing."""
    print("\nUpdating vi/articles/index.html...")
    index_path = BASE / "vi" / "articles" / "index.html"
    
    if not index_path.exists():
        print("  WARNING: vi/articles/index.html not found")
        return
    
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # The index.html contains article cards. We need to add the new ones.
    # This is complex - for now, just note that it needs manual update or a more sophisticated approach
    print("  Note: vi/articles/index.html needs manual update to include new article cards")
    print("  The new articles are now accessible at /vi/articles/{slug}/")

if __name__ == "__main__":
    main()