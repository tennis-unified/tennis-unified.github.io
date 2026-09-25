import os
import json
import re
import html
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Import core modules
exec(open(r"C:\Users\Phamd\.gemini\antigravity\brain\3e583d85-01a7-476e-8d52-34e7c4491c9c\scratch\deploy_engine.py", encoding="utf-8").read())

vi_dir = BASE / "vi" / "articles"
en_dir = BASE / "en" / "articles"
root_articles_dir = BASE / "articles"
en_md_dir = BASE / "en" / "articles_md"

root_articles_dir.mkdir(parents=True, exist_ok=True)

print(f"Beginning deployment of articles 1 to 144 across:")
print(f"  1. {vi_dir}")
print(f"  2. {en_dir}")
print(f"  3. {root_articles_dir} (Mirror)")

success_vi = 0
success_en = 0
success_mirror = 0

for i in range(1, 145):
    m_en = meta_200["en"][i-1]
    m_vi = meta_200["vi"][i-1]
    s_en = m_en["slug"]
    s_vi = m_vi["slug"]
    pillar = m_en.get("pillar_slug", "biomechanics")
    
    # Calculate prev and next
    prev_vi = meta_200["vi"][i-2]["slug"] if i > 1 else ""
    next_vi = meta_200["vi"][i]["slug"] if i < 200 else ""
    prev_en = meta_200["en"][i-2]["slug"] if i > 1 else ""
    next_en = meta_200["en"][i]["slug"] if i < 200 else ""

    vid_info = video_map.get(str(i), {
        "video_id": "LIKPQn_KgwA",
        "title": "Tennis Kinetic Fundamentals",
        "channel": "Tennis Unified"
    })
    
    p_url_vi, p_title_vi = pillar_urls_vi.get(pillar, ("co-sinh-hoc", "Cơ Sinh Học"))
    p_url_en, p_title_en = pillar_urls_en.get(pillar, ("biomechanics", "Applied Biomechanics"))

    # ----------------------------------------------------
    # 1. BUILD VIETNAMESE ARTICLE
    # ----------------------------------------------------
    target_vi_dir = vi_dir / s_vi
    target_vi_dir.mkdir(parents=True, exist_ok=True)
    target_vi_file = target_vi_dir / "index.html"

    sm = source_map[str(i)]
    vi_content_html = ""

    # If markdown source exists:
    if sm["vi_md_path"] and os.path.exists(sm["vi_md_path"]):
        raw_md = open(sm["vi_md_path"], "r", encoding="utf-8", errors="ignore").read()
        cleaned_md = clean_vietnamese_markdown(raw_md, i, vid_info)
        vi_content_html = md_to_html(cleaned_md)
    elif sm["vi_html_size"] > 20000 and target_vi_file.exists():
        existing_html = open(target_vi_file, "r", encoding="utf-8", errors="ignore").read()
        marker_start = '<article class="md-content__inner md-typeset">'
        marker_end = '</article>'
        if marker_start in existing_html:
            inner_body = existing_html.split(marker_start)[-1].split(marker_end)[0]
            # Replace placeholder video if present
            if "VIDEO_ID_PLACEHOLDER" in inner_body:
                vid_id = vid_info["video_id"]
                vid_title = vid_info["title"]
                vid_channel = vid_info["channel"]
                video_html = f'''<div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 8px; margin: 1.5rem 0;">
  <iframe src="https://www.youtube-nocookie.com/embed/{vid_id}" title="{html.escape(vid_title)}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>
<p><em>Video: {html.escape(vid_title)} ({html.escape(vid_channel)}).</em></p>'''
                inner_body = re.sub(r'<div class="video-container"[\s\S]*?</div>\s*(?:<p><em>[^<]*</em></p>)?', video_html, inner_body)
                inner_body = inner_body.replace("VIDEO_ID_PLACEHOLDER", vid_id)
            vi_content_html = inner_body

    breadcrumb_vi = f'''<!-- TP-BREADCRUMB-START -->
<p><a href="/">🏠 Home</a> &nbsp;›&nbsp; <a href="/vi/articles/">Tennis Fundamentals</a> &nbsp;›&nbsp; <a href="/vi/articles/{p_url_vi}/">{p_title_vi}</a> &nbsp;›&nbsp; {m_vi["title"]}</p>
<hr />
<!-- TP-NAV-END -->'''

    prev_link_vi = f'<a href="/vi/articles/{prev_vi}/">← Trước</a>' if prev_vi else '<span style="opacity:0.5">← Trước</span>'
    next_link_vi = f'<a href="/vi/articles/{next_vi}/">Sau →</a>' if next_vi else '<span style="opacity:0.5">Sau →</span>'
    nav_vi = f'''<!-- TP-NAV-START -->
<p class="article-nav" style="margin-top:2rem;font-size:0.95rem">{prev_link_vi} &nbsp;|&nbsp; <a href="/vi/articles/">🏠 Trang chủ</a> &nbsp;|&nbsp; {next_link_vi}</p>
<!-- TP-NAV-END -->'''

    custom_head_vi = head_vi_raw.replace(
        'Lực Phản Hồi Từ Mặt Sân (GRF) — Vector Dọc So Với Vector Ngang', m_vi["title"]
    ).replace(
        'VI-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors', s_vi
    ).replace(
        'EN-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors', s_en
    )

    full_page_vi = (
        custom_head_vi
        + '<article class="md-content__inner md-typeset">\n\n'
        + breadcrumb_vi + '\n\n'
        + f'<h1 id="content">{m_vi["title"]}</h1>\n\n'
        + vi_content_html + '\n\n'
        + nav_vi + '\n\n'
        + '</article>\n'
        + foot_vi_raw
    )

    with open(target_vi_file, "w", encoding="utf-8") as f:
        f.write(full_page_vi)
    success_vi += 1

    # ----------------------------------------------------
    # 2. BUILD ENGLISH ARTICLE
    # ----------------------------------------------------
    target_en_dir = en_dir / s_en
    target_en_dir.mkdir(parents=True, exist_ok=True)
    target_en_file = target_en_dir / "index.html"

    en_content_html = ""
    en_md_file = en_md_dir / f"ART-{i:03d}.md"

    # Priority 1: Check if translated English markdown file exists
    if en_md_file.exists():
        raw_en_md = open(en_md_file, "r", encoding="utf-8", errors="ignore").read()
        cleaned_en_md = strip_frontmatter(raw_en_md)
        
        # Inject video into EN markdown if not already present
        vid_id = vid_info["video_id"]
        vid_title = vid_info["title"]
        vid_channel = vid_info["channel"]
        video_html = f'''<div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 8px; margin: 1.5rem 0;">
  <iframe src="https://www.youtube-nocookie.com/embed/{vid_id}" title="{html.escape(vid_title)}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>
<p><em>Video: {html.escape(vid_title)} ({html.escape(vid_channel)}).</em></p>'''

        if "VIDEO_ID_PLACEHOLDER" in cleaned_en_md:
            cleaned_en_md = re.sub(r'<div class="video-container"[\s\S]*?</div>\s*(?:<p><em>[^<]*</em></p>)?', video_html, cleaned_en_md)
            cleaned_en_md = cleaned_en_md.replace("VIDEO_ID_PLACEHOLDER", vid_id)
        elif '<div class="video-container"' not in cleaned_en_md:
            cue_match = re.search(r'(>[\s\S]*?\n\n)', cleaned_en_md)
            if cue_match:
                end_pos = cue_match.end()
                cleaned_en_md = cleaned_en_md[:end_pos] + video_html + "\n\n" + cleaned_en_md[end_pos:]
            else:
                cleaned_en_md = video_html + "\n\n" + cleaned_en_md

        en_content_html = md_to_html(cleaned_en_md)

    # Priority 2: Check if existing full English html exists and is clean (>15000 bytes)
    elif sm["en_html_size"] > 15000 and target_en_file.exists():
        existing_en = open(target_en_file, "r", encoding="utf-8", errors="ignore").read()
        marker_start = '<article class="md-content__inner md-typeset">'
        marker_end = '</article>'
        if marker_start in existing_en:
            inner_en = existing_en.split(marker_start)[-1].split(marker_end)[0]
            # Strip any leaked breadcrumb or duplicate h1
            inner_en = re.sub(r'<!-- TP-BREADCRUMB-START -->[\s\S]*?<!-- TP-NAV-END -->\s*', '', inner_en)
            inner_en = re.sub(r'<h1 id="content">[^<]+</h1>\s*', '', inner_en)
            inner_en = re.sub(r'<!-- TP-NAV-START -->[\s\S]*?<!-- TP-NAV-END -->\s*', '', inner_en)
            
            # Replace placeholder video if present
            vid_id = vid_info["video_id"]
            vid_title = vid_info["title"]
            vid_channel = vid_info["channel"]
            video_html = f'''<div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 8px; margin: 1.5rem 0;">
  <iframe src="https://www.youtube-nocookie.com/embed/{vid_id}" title="{html.escape(vid_title)}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>
<p><em>Video: {html.escape(vid_title)} ({html.escape(vid_channel)}).</em></p>'''
            if "VIDEO_ID_PLACEHOLDER" in inner_en:
                inner_en = re.sub(r'<div class="video-container"[\s\S]*?</div>\s*(?:<p><em>[^<]*</em></p>)?', video_html, inner_en)
                inner_en = inner_en.replace("VIDEO_ID_PLACEHOLDER", vid_id)
            en_content_html = inner_en
    else:
        # Fallback if md not translated yet
        en_content_html = vi_content_html

    breadcrumb_en = f'''<!-- TP-BREADCRUMB-START -->
<p><a href="/">🏠 Home</a> &nbsp;›&nbsp; <a href="/en/articles/">Tennis Fundamentals</a> &nbsp;›&nbsp; <a href="/en/articles/{p_url_en}/">{p_title_en}</a> &nbsp;›&nbsp; {m_en["title"]}</p>
<hr />
<!-- TP-NAV-END -->'''

    prev_link_en = f'<a href="/en/articles/{prev_en}/">← Previous</a>' if prev_en else '<span style="opacity:0.5">← Previous</span>'
    next_link_en = f'<a href="/en/articles/{next_en}/">Next →</a>' if next_en else '<span style="opacity:0.5">Next →</span>'
    nav_en = f'''<!-- TP-NAV-START -->
<p class="article-nav" style="margin-top:2rem;font-size:0.95rem">{prev_link_en} &nbsp;|&nbsp; <a href="/en/articles/">🏠 Home</a> &nbsp;|&nbsp; {next_link_en}</p>
<!-- TP-NAV-END -->'''

    custom_head_en = head_en_raw.replace(
        'Ground Reaction Forces (GRF): Vertical vs. Horizontal Vectors', m_en["title"]
    ).replace(
        'EN-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors', s_en
    ).replace(
        'VI-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors', s_vi
    )

    full_page_en = (
        custom_head_en
        + '<article class="md-content__inner md-typeset">\n\n'
        + breadcrumb_en + '\n\n'
        + f'<h1 id="content">{m_en["title"]}</h1>\n\n'
        + en_content_html + '\n\n'
        + nav_en + '\n\n'
        + '</article>\n'
        + foot_en_raw
    )

    with open(target_en_file, "w", encoding="utf-8") as f:
        f.write(full_page_en)
    success_en += 1

    # ----------------------------------------------------
    # 3. BUILD MIRROR ARTICLE IN ROOT /articles/
    # ----------------------------------------------------
    target_mirror_dir = root_articles_dir / s_en
    target_mirror_dir.mkdir(parents=True, exist_ok=True)
    target_mirror_file = target_mirror_dir / "index.html"

    # Add canonical pointing to /en/articles/{s_en}/
    mirror_page = full_page_en.replace(
        f'<link rel="alternate" href="/en/articles/{s_en}/" hreflang="en">',
        f'<link rel="canonical" href="https://tennis-unified.github.io/en/articles/{s_en}/">\n    <link rel="alternate" href="/en/articles/{s_en}/" hreflang="en">'
    )

    with open(target_mirror_file, "w", encoding="utf-8") as f:
        f.write(mirror_page)
    success_mirror += 1

    if i % 20 == 0 or i == 144:
        print(f"Progress: Deployed through article {i:03d}/144...")

print(f"\nDeployment Complete!")
print(f"  Vietnamese articles deployed: {success_vi}/144")
print(f"  English articles deployed: {success_en}/144")
print(f"  Root mirror articles deployed: {success_mirror}/144")
