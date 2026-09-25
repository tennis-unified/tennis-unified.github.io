# -*- coding: utf-8 -*-
"""Compile and deploy articles 145-200 (EN + VI + root mirror).

Reuses the verified templates and markdown->HTML converter from deploy_engine.py.
"""
import html
import json
import re
import sys
from pathlib import Path

SCRIPTS = Path(r"D:\Github Repos\tennis-unified\scripts")
BASE = Path(r"D:\Github Repos\tennis-unified")
sys.path.insert(0, str(SCRIPTS))
sys.stdout.reconfigure(encoding="utf-8")

import deploy_engine as E  # noqa: E402  (loads templates, md_to_html, strip_frontmatter)

with open(SCRIPTS / "articles_145_200_meta.json", encoding="utf-8") as f:
    META = json.load(f)
with open(SCRIPTS / "article_video_map_145_200.json", encoding="utf-8") as f:
    VIDEO = json.load(f)
with open(SCRIPTS / "articles_200_data.json", encoding="utf-8") as f:
    CAT = json.load(f)

TITLE_VI_REF = "Lực Phản Hồi Từ Mặt Sân (GRF) — Vector Dọc So Với Vector Ngang"
TITLE_EN_REF = "Ground Reaction Forces (GRF): Vertical vs. Horizontal Vectors"
SLUG_REF_EN = "EN-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors"
SLUG_REF_VI = "VI-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors"

VI_DIR = BASE / "vi" / "articles"
EN_DIR = BASE / "en" / "articles"
MIRROR_DIR = BASE / "articles"
EN_MD_DIR = BASE / "en" / "articles_md"


def video_block(vid_id, title, caption_prefix="Video"):
    div = (
        '<div class="video-container" style="position: relative; padding-bottom: 56.25%; '
        'height: 0; overflow: hidden; max-width: 100%; border-radius: 8px; margin: 1.5rem 0;">\n'
        f'  <iframe src="https://www.youtube-nocookie.com/embed/{vid_id}" title="{html.escape(title)}" '
        'frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; '
        'picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; '
        'height: 100%;"></iframe>\n'
        '</div>'
    )
    caption = f'*{caption_prefix}: {v["title"]} ({v["channel"]}).*'
    return div + "\n\n" + caption


def inject_video(md, v, caption_prefix="Video"):
    block = video_block(v["video_id"], v["title"], caption_prefix)
    if "VIDEO_ID_PLACEHOLDER" in md or '<div class="video-container"' in md:
        pattern = (r'<div class="video-container"[\s\S]*?</div>'
                   r'(?:\s*(?:<p><em>[^<]*</em></p>|\*[^\n*]*\*))?')
        md = re.sub(pattern, lambda _m: block, md, count=1)
        return md.replace("VIDEO_ID_PLACEHOLDER", v["video_id"])
    m = re.search(r'(>[\s\S]*?\n\n)', md)
    if m:
        return md[:m.end()] + block + "\n\n" + md[m.end():]
    return block + "\n\n" + md


ok_en = ok_vi = ok_mirror = 0
for num in range(145, 201):
    key = str(num)
    meta = META[key]
    v = VIDEO[key]
    i = num  # catalogue index is 1-based

    m_en = CAT["en"][num - 1]
    m_vi = CAT["vi"][num - 1]
    s_en, s_vi = meta["slug_en"], meta["slug_vi"]
    pillar = m_en.get("pillar_slug", "biomechanics")

    prev_en = CAT["en"][num - 2]["slug"] if num > 1 else ""
    next_en = CAT["en"][num]["slug"] if num < 200 else ""
    prev_vi = meta.get("prev_vi") or (CAT["vi"][num - 2]["slug"] if num > 1 else "")
    next_vi = meta.get("next_vi") or (CAT["vi"][num]["slug"] if num < 200 else "")

    p_url_vi, p_title_vi = E.pillar_urls_vi.get(pillar, ("co-sinh-hoc", "Cơ Sinh Học"))
    p_url_en, p_title_en = E.pillar_urls_en.get(pillar, ("biomechanics", "Applied Biomechanics"))

    # ---------------- Vietnamese page
    vi_md_path = VI_DIR / s_vi / "index.md"
    if not vi_md_path.exists():
        print(f"[skip] missing VI md: {vi_md_path}")
        continue
    vi_md = inject_video(E.strip_frontmatter(vi_md_path.read_text(encoding="utf-8")), v,
                         caption_prefix="Video minh họa")
    vi_body = E.md_to_html(vi_md)

    breadcrumb_vi = (
        '<!-- TP-BREADCRUMB-START -->\n'
        f'<p><a href="/">🏠 Home</a> &nbsp;›&nbsp; <a href="/vi/articles/">Tennis Fundamentals</a> '
        f'&nbsp;›&nbsp; <a href="/vi/articles/{p_url_vi}/">{p_title_vi}</a> &nbsp;›&nbsp; {m_vi["title"]}</p>\n'
        '<hr />\n<!-- TP-NAV-END -->'
    )
    prev_link_vi = f'<a href="/vi/articles/{prev_vi}/">← Trước</a>' if prev_vi else '<span style="opacity:0.5">← Trước</span>'
    next_link_vi = f'<a href="/vi/articles/{next_vi}/">Sau →</a>' if next_vi else '<span style="opacity:0.5">Sau →</span>'
    nav_vi = (
        '<!-- TP-NAV-START -->\n'
        f'<p class="article-nav" style="margin-top:2rem;font-size:0.95rem">{prev_link_vi} &nbsp;|&nbsp; '
        f'<a href="/vi/articles/">🏠 Trang chủ</a> &nbsp;|&nbsp; {next_link_vi}</p>\n'
        '<!-- TP-NAV-END -->'
    )
    head_vi = (E.head_vi_raw.replace(TITLE_VI_REF, m_vi["title"])
               .replace(SLUG_REF_VI, s_vi).replace(SLUG_REF_EN, s_en))
    page_vi = (head_vi + '<article class="md-content__inner md-typeset">\n\n' + breadcrumb_vi + '\n\n'
               + f'<h1 id="content">{m_vi["title"]}</h1>\n\n' + vi_body + '\n\n' + nav_vi + '\n\n'
               + '</article>\n' + E.foot_vi_raw)
    (VI_DIR / s_vi).mkdir(parents=True, exist_ok=True)
    (VI_DIR / s_vi / "index.html").write_text(page_vi, encoding="utf-8", newline="\n")
    ok_vi += 1

    # ---------------- English page
    en_md_path = EN_MD_DIR / f"ART-{num:03d}.md"
    if not en_md_path.exists():
        print(f"[skip] missing EN md: {en_md_path}")
        continue
    en_md = inject_video(E.strip_frontmatter(en_md_path.read_text(encoding="utf-8")), v)
    en_body = E.md_to_html(en_md)

    breadcrumb_en = (
        '<!-- TP-BREADCRUMB-START -->\n'
        f'<p><a href="/">🏠 Home</a> &nbsp;›&nbsp; <a href="/en/articles/">Tennis Fundamentals</a> '
        f'&nbsp;›&nbsp; <a href="/en/articles/{p_url_en}/">{p_title_en}</a> &nbsp;›&nbsp; {m_en["title"]}</p>\n'
        '<hr />\n<!-- TP-NAV-END -->'
    )
    prev_link_en = f'<a href="/en/articles/{prev_en}/">← Previous</a>' if prev_en else '<span style="opacity:0.5">← Previous</span>'
    next_link_en = f'<a href="/en/articles/{next_en}/">Next →</a>' if next_en else '<span style="opacity:0.5">Next →</span>'
    nav_en = (
        '<!-- TP-NAV-START -->\n'
        f'<p class="article-nav" style="margin-top:2rem;font-size:0.95rem">{prev_link_en} &nbsp;|&nbsp; '
        f'<a href="/en/articles/">🏠 Home</a> &nbsp;|&nbsp; {next_link_en}</p>\n'
        '<!-- TP-NAV-END -->'
    )
    head_en = (E.head_en_raw.replace(TITLE_EN_REF, m_en["title"])
               .replace(SLUG_REF_EN, s_en).replace(SLUG_REF_VI, s_vi))
    page_en = (head_en + '<article class="md-content__inner md-typeset">\n\n' + breadcrumb_en + '\n\n'
               + f'<h1 id="content">{m_en["title"]}</h1>\n\n' + en_body + '\n\n' + nav_en + '\n\n'
               + '</article>\n' + E.foot_en_raw)
    (EN_DIR / s_en).mkdir(parents=True, exist_ok=True)
    (EN_DIR / s_en / "index.html").write_text(page_en, encoding="utf-8", newline="\n")
    ok_en += 1

    # ---------------- Root mirror (canonical -> /en/)
    mirror = page_en.replace(
        f'<link rel="alternate" href="/en/articles/{s_en}/" hreflang="en">',
        f'<link rel="canonical" href="https://tennis-unified.github.io/en/articles/{s_en}/">\n'
        f'    <link rel="alternate" href="/en/articles/{s_en}/" hreflang="en">'
    )
    (MIRROR_DIR / s_en).mkdir(parents=True, exist_ok=True)
    (MIRROR_DIR / s_en / "index.html").write_text(mirror, encoding="utf-8", newline="\n")
    ok_mirror += 1

    if num % 14 == 0 or num == 200:
        print(f"  deployed through {num:03d}")

print(f"\nDeployed 145-200 -> VI {ok_vi}, EN {ok_en}, mirror {ok_mirror}")
