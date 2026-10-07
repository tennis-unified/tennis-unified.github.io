#!/usr/bin/env python3
"""
build_vi_md_only.py — Build index.html for Vietnamese articles that have an
index.md source but no built index.html (live 404).

Generalises scripts/generate_vi_html.py (which was hard-coded to 10 slugs) into
a frontmatter-driven builder:

  * reads title / article_number / pillar / pillar_title / description
    / prev_article / next_article from each md's YAML frontmatter;
  * renders the body with the same markdown_to_html() converter and the same
    reference head/foot template, so output is visually identical to the
    118 already-built Vietnamese articles;
  * rewrites prev/next nav to fall back to the pillar index when the target
    slug is not present in the tree (5 refs in the source data are dangling);
  * writes a self-referential absolute canonical and *no* hreflang (these 57
    articles have no EN twin — verified), matching the SEO policy enforced by
    scripts/seo/seo_fix.py verify.

Usage:
    python build_vi_md_only.py --root <repo> [--dry-run]
"""

import argparse
import os
import re
import sys
from pathlib import Path

REF_SLUG = "VI-tenniskb-ground-reaction-forces-grf-vertical-vs-horizontal-vectors"
CANON = "https://tennis-unified.github.io"


# --------------------------------------------------------------------------- #
# frontmatter
# --------------------------------------------------------------------------- #
def read_frontmatter(path):
    txt = Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", txt, re.S)
    if not m:
        return {}, txt
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.split("\n"):
        mm = re.match(r'^([A-Za-z_]+):\s*"?(.*?)"?\s*$', line)
        if mm:
            fm[mm.group(1)] = mm.group(2)
    return fm, body


# --------------------------------------------------------------------------- #
# markdown -> html (ported verbatim from generate_vi_html.py so output matches
# the 118 already-built articles)
# --------------------------------------------------------------------------- #
def markdown_to_html(md_text):
    html = md_text

    lines = html.split("\n")
    new_lines = []
    skipped_first_h1 = False
    for line in lines:
        if not skipped_first_h1 and re.match(r"^# ", line.strip()):
            skipped_first_h1 = True
            continue
        new_lines.append(line)
    html = "\n".join(new_lines)

    def convert_table(match):
        table_text = match.group(0)
        rows = table_text.strip().split("\n")
        if len(rows) < 2:
            return table_text
        header_cells = [c.strip() for c in rows[0].split("|") if c.strip()]
        data_rows = rows[2:] if len(rows) > 2 else []
        out = ["<table>", "<thead><tr>"]
        for cell in header_cells:
            out.append(f'<th style="text-align: left;">{cell}</th>')
        out.append("</tr></thead>")
        if data_rows:
            out.append("<tbody>")
            for row in data_rows:
                cells = [c.strip() for c in row.split("|") if c.strip()]
                if cells:
                    out.append("<tr>")
                    for cell in cells:
                        out.append(f'<td style="text-align: left;">{cell}</td>')
                    out.append("</tr>")
            out.append("</tbody>")
        out.append("</table>")
        return "\n".join(out)

    html = re.sub(
        r"^\|.*\|$\n^\|[-:\s|]+\|$\n(?:\|.*\|$\n?)*", convert_table, html, flags=re.MULTILINE
    )
    html = re.sub(r"^### (.*?)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.*?)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.*?)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)

    bold_placeholders = {}

    def save_bold(match):
        ph = f"__BOLD_{len(bold_placeholders)}__"
        bold_placeholders[ph] = match.group(0)
        return ph

    html = re.sub(r"\*\*(.+?)\*\*", save_bold, html)

    # Italic.
    #
    # Guard: a leading "* " is a LIST BULLET, not an italic opener. Left in the
    # text it mis-pairs with the asterisks of a following **bold**, producing
    # stray "<em>" / "</em>". Stash bullet markers first, then run italic on
    # what is left, so the two cannot cross.
    bullets = {}

    def save_bullet(m):
        ph = f"__BULLET_{len(bullets)}__"
        bullets[ph] = "* "
        return ph

    html = re.sub(r"(?m)^([ \t]*)\*[ \t]+", lambda m: m.group(1) + save_bullet(m), html)
    html = re.sub(r"\*([^*\n]+?)\*", r"<em>\1</em>", html)
    for ph, b in bullets.items():
        html = html.replace(ph, "* ")
    for ph, b in bold_placeholders.items():
        html = html.replace(ph, b)

    # Blockquotes.
    #
    # The upstream generate_vi_html.py used a single regex with DOTALL that
    # over-matched across blank lines and emitted a malformed trailing
    # "<p></blockquote></p>". Do this line-by-line instead: consume runs of
    # consecutive "> " lines and wrap the lot in one <blockquote>.
    def _bq(lines):
        out, i = [], 0
        while i < len(lines):
            if lines[i].lstrip().startswith(">"):
                buf = []
                while i < len(lines) and lines[i].lstrip().startswith(">"):
                    buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                    i += 1
                inner = "\n".join(buf).strip()
                # drop a trailing stray paragraph-close artefact if present
                inner = re.sub(r"</p>\s*</blockquote>\s*</p>", "</p>", inner)
                inner = re.sub(r"</blockquote>\s*</p>\s*$", "</blockquote>", inner)
                out.append(
                    f"<blockquote>\n<p>{inner}</p>\n</blockquote>"
                    if "<p>" not in inner
                    else f"<blockquote>\n{inner}\n</blockquote>"
                )
            else:
                out.append(lines[i])
                i += 1
        return out

    html = "\n".join(_bq(html.split("\n")))

    def replace_code_block(match):
        return f'<pre><code class="language-html">{match.group(1)}</code></pre>'

    html = re.sub(r"```html\n(.*?)\n```", replace_code_block, html, flags=re.DOTALL)

    # Escape stray "<" that is prose, not a tag. The source articles contain
    # literal angle-bracket text ("<Zone 2", "(<Service line)") which the
    # browser would otherwise parse as an unknown element. A "<" is treated as
    # markup only when it is followed by a known element name / closing slash.
    KNOWN = (
        "p|strong|em|b|i|u|h[1-6]|ul|ol|li|table|thead|tbody|tr|th|td|"
        "blockquote|pre|code|div|span|a|img|br|hr|meta|link|title|"
        "article|nav|button|style|figure|figcaption|sup|sub|small|"
        "iframe|video|source|script|section|header|footer|main|input|label|svg|path"
    )
    html = re.sub(rf"<(?!/?(?:{KNOWN})\b)", "&lt;", html)

    lines = html.split("\n")
    result = []
    in_table = False
    in_list = False
    list_type = None

    for line in lines:
        stripped = line.strip()
        if re.match(r"^</?(h[1-6]|p|blockquote|pre|table|thead|tbody|tr|th|td|ul|ol|li|hr|div)\b", stripped):
            if stripped.startswith("<table"):
                in_table = True
            if stripped.startswith("</table"):
                in_table = False
            if in_list:
                result.append(f"</{list_type}>")
                in_list = False
                list_type = None
            result.append(line)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                result.append("<ul>")
                in_list = True
                list_type = "ul"
            result.append(f"<li>{stripped[2:]}</li>")
        elif re.match(r"^\d+\. ", stripped):
            if not in_list:
                result.append("<ol>")
                in_list = True
                list_type = "ol"
            result.append(f"<li>{re.sub(r'^[0-9]+\\. ', '', stripped)}</li>")
        elif stripped == "":
            if in_list:
                result.append(f"</{list_type}>")
                in_list = False
                list_type = None
            result.append("")
        elif in_table:
            result.append(line)
        else:
            if in_list:
                result.append(f"</{list_type}>")
                in_list = False
                list_type = None
            if stripped:
                result.append(f"<p>{line}</p>")
            else:
                result.append("")

    if in_list:
        result.append(f"</{list_type}>")
    return "\n".join(result)


# --------------------------------------------------------------------------- #
# template
# --------------------------------------------------------------------------- #
def load_templates(root):
    ref = Path(root) / "vi" / "articles" / REF_SLUG / "index.html"
    content = ref.read_text(encoding="utf-8")
    start = content.find('<article class="md-content__inner md-typeset">')
    end = content.find("</article>", start)
    if start < 0 or end < 0:
        raise RuntimeError(f"reference template markers not found in {ref}")
    return content[:start], content[end + len("</article>"):]


# --------------------------------------------------------------------------- #
# build one page
# --------------------------------------------------------------------------- #
def build_page(root, slug, fm, md_body, head_tpl, foot_tpl, all_slugs):
    title = fm.get("title", slug)
    pillar = fm.get("pillar", "")
    pillar_title = fm.get("pillar_title", pillar)
    num = fm.get("article_number", "0")
    num = int(num) if str(num).isdigit() else 0

    def nav_target(s, fallback_pillar):
        if s and s in all_slugs:
            return f"/vi/articles/{s}/"
        return f"/vi/articles/{fallback_pillar}/"

    prev_href = nav_target(fm.get("prev_article"), pillar)
    next_href = nav_target(fm.get("next_article"), pillar)

    content_html = markdown_to_html(md_body)
    short = title.split(": ", 1)[1] if ": " in title else title
    h1 = title

    breadcrumb = (
        f'<p><a href="/">🏠 Home</a> &nbsp;›&nbsp; '
        f'<a href="/vi/articles/">Tennis Fundamentals</a> &nbsp;›&nbsp; '
        f'<a href="/vi/articles/{pillar}/">{pillar_title}</a> &nbsp;›&nbsp; {h1}</p>\n<hr />'
    )
    nav = (
        '<p class="article-nav" style="margin-top:2rem;font-size:0.95rem">\n'
        f'  <a href="{prev_href}">← Trước</a> &nbsp;|&nbsp;\n'
        '  <a href="/vi/articles/">🏠 Trang chủ</a> &nbsp;|&nbsp;\n'
        f'  <a href="{next_href}">Sau →</a>\n</p>'
    )
    body = f'{breadcrumb}\n\n<h1 id="content">{h1}</h1>\n\n{content_html}\n\n{nav}'

    # NOTE: the reference template's <title> already ends with the site suffix
    # " - Tennis Unified Library", and its <meta description> already ends with
    # "| Tennis Future Lab". ref_* must therefore be the *full* strings exactly
    # as they appear, and new_* must carry the same suffix, or the suffix is
    # left behind and duplicated.
    ref_title = (
        "Bài viết 001: Lực Phản Hồi Từ Mặt Sân (GRF) — Vector Dọc So Với Vector Ngang"
        " - Tennis Unified Library"
    )
    ref_desc = (
        "TennisKB — Bài viết 001: Lực Phản Hồi Từ Mặt Sân (GRF) — Vector Dọc So Với Vector Ngang"
        " | Tennis Future Lab"
    )
    new_title = f"Bài viết {num:03d}: {short} - Tennis Unified Library"
    new_desc = f"TennisKB — Bài viết {num:03d}: {short} | Tennis Future Lab"

    head = head_tpl.replace(ref_title, new_title).replace(ref_desc, new_desc)
    head = head.replace(REF_SLUG, slug).replace(REF_SLUG.replace("VI-", "EN-"), slug.replace("VI-", "EN-"))

    # --- SEO conformance: absolute self canonical, strip any stale hreflang ---
    head = re.sub(r'\n?\s*<link rel="alternate"[^>]*hreflang="[^"]*"[^>]*>', "", head)
    canon_url = f"{CANON}/vi/articles/{slug}/"
    if 'rel="canonical"' in head:
        head = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{canon_url}">', head)
    else:
        head = head.replace(
            '<link rel="icon"', f'<link rel="canonical" href="{canon_url}">\n    <link rel="icon"', 1
        )

    page = head + '<article class="md-content__inner md-typeset">\n\n' + body + "\n\n</article>\n" + foot_tpl
    return page


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    vdir = root / "vi" / "articles"
    all_slugs = {d.name for d in vdir.iterdir() if d.is_dir()}

    targets = []
    for d in sorted(vdir.iterdir()):
        if not d.is_dir():
            continue
        md, html = d / "index.md", d / "index.html"
        if md.is_file() and not html.is_file():
            targets.append(d)

    print(f"md-only Vietnamese articles to build: {len(targets)}")
    head_tpl, foot_tpl = load_templates(root)

    built = 0
    for d in targets:
        fm, body = read_frontmatter(d / "index.md")
        if not fm.get("title"):
            print(f"  SKIP (no frontmatter): {d.name}")
            continue
        page = build_page(root, d.name, fm, body, head_tpl, foot_tpl, all_slugs)
        if args.dry_run:
            print(f"  WOULD WRITE {d.name}  ({len(page)} bytes)")
        else:
            (d / "index.html").write_text(page, encoding="utf-8", newline="")
            print(f"  wrote {d.name}  ({len(page)} bytes)")
        built += 1

    print(f"\n{'would build' if args.dry_run else 'built'}: {built}")


if __name__ == "__main__":
    main()
