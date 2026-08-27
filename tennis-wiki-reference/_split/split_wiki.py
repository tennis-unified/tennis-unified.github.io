"""Split 4 long wiki topic pages into per-chapter subpages with
< Previous | Home | Next > nav, plus a master topic index.

Run:
    python split_wiki.py --apply
"""

import os, re, sys
from pathlib import Path

ROOT = Path(r"D:/Github Repos/tennis-unified/tennis-wiki-reference")

APP_SHELL_LINE = '<article class="md-content__inner md-typeset">'

# Each chapter: {slug, title, start_anchor, end_anchor}.
# start_anchor = h2/h3 id where the chapter body begins (inclusive).
# end_anchor   = h2/h3 id where the NEXT chapter begins (exclusive); or
#                None for the final chapter (runs to end of body).
#
# For pages where there's a long block of content with no headings, we set
# start_offset / end_offset directly (in body-coordinate offsets).
SPLIT_PLAN = {
    "tactical-tennis": [
        {"slug": "1-movement-the-universal-athletic-position",
         "title": "Movement — The Universal Athletic Position",
         "start_anchor": "article-1", "end_anchor": "article-2"},
        {"slug": "2-serving-mechanics-the-jump",
         "title": "Serving Mechanics — The Jump",
         "start_anchor": "article-2", "end_anchor": "article-3"},
        {"slug": "3-ball-toss-part-one",
         "title": "Serve Mechanics — Ball Toss (Part One)",
         "start_anchor": "article-3", "end_anchor": "article-4"},
        {"slug": "4-ball-toss-part-two",
         "title": "Serving Mechanics — Ball Toss (Part Two)",
         "start_anchor": "article-4", "end_anchor": None},
    ],
    "tennis-racket-sweet-spots": [
        {"slug": "1-what-part-of-the-racquet",
         "title": "What Part Of The Racquet Should Be Used To Strike The Ball?",
         "start_anchor": "article-1", "end_anchor": "article-2"},
        {"slug": "2-physics-of-tennis-racket-sweet-spots",
         "title": "The Physics of Tennis Racket Sweet Spots",
         "start_anchor": "article-2", "end_anchor": "article-3"},
        {"slug": "3-modern-tennis-rackets-balls-and-surfaces",
         "title": "Modern Tennis Rackets, Balls, and Surfaces",
         "start_anchor": "article-3", "end_anchor": None},
    ],
    "serve-and-volley": [
        {"slug": "1-the-classic-net-rushing-style",
         "title": "Serve and Volley — The Classic Net-Rushing Style",
         "start_anchor": "serve-and-volley-guide",
         "end_anchor": "serve-and-volley-is-it-worth-it"},
        {"slug": "2-is-it-worth-it",
         "title": "Serve-and-Volley — Is It Worth It?",
         "start_anchor": "serve-and-volley-is-it-worth-it",
         "end_anchor": "a-strategy-primer-on-how-to-serve-and-volley-effectively-in-tennis"},
        {"slug": "3-strategy-primer-effective-net-rushing",
         "title": "A Strategy Primer on How to Serve and Volley Effectively",
         "start_anchor": "a-strategy-primer-on-how-to-serve-and-volley-effectively-in-tennis",
         "end_anchor": None},
    ],
    "fault-tolerant-tennis": [
        {"slug": "1-what-is-fault-tolerance",
         "title": "What is Fault Tolerance?",
         "start_anchor": "what-is-fault-tolerance",
         "end_anchor": "engage-the-posterior-chain",  # end = full closing of h3
         "end_after": True},  # include the heading itself in Ch1, end at its close
        {"slug": "2-building-the-base",
         "title": "Building the Base — Between Fundamentals and Plateaus",
         "start_offset_body": None,  # filled in: end of engage-the-posterior-chain
         "end_offset_body": None},   # filled in: start of smashing-through-plateaus
        {"slug": "3-plateaus-and-bottlenecks",
         "title": "Plateaus and Bottlenecks",
         "start_anchor": "smashing-through-plateaus",
         "end_anchor": "triple-flexion-athleticism"},
        {"slug": "4-triple-flexion-athleticism",
         "title": "Triple-Flexion Athleticism",
         "start_anchor": "triple-flexion-athleticism",
         "end_anchor": None},
    ],
}

NAV_HTML = """
<nav class="chapter-nav" aria-label="Chapter navigation" style="margin:3rem 0 1rem;padding:1.25rem;border-top:1px solid var(--md-default-fg-color--lightest,#ddd);display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;font-size:.95rem;">
  <div style="flex:1;text-align:left;">__PREV__</div>
  <div style="flex:1;text-align:center;"><a href="../" style="text-decoration:none;">Home</a></div>
  <div style="flex:1;text-align:right;">__NEXT__</div>
</nav>
"""


def enumerate_headings(html_text, body_start, body_end):
    body = html_text[body_start:body_end]
    pat = re.compile(
        r'<(h[1-4])[^>]*\bid="([^"]+)"[^>]*>(.*?)</\1>', re.S)
    out = []
    for m in pat.finditer(body):
        anchor = m.group(2)
        out.append({
            "anchor": anchor,
            "span_open": m.span()[0],
            "span_close": m.span()[1],
        })
    out.sort(key=lambda h: h["span_open"])
    return out


def find_anchor_span(headings, anchor_id):
    for h in headings:
        if h["anchor"] == anchor_id:
            return h
    return None


def compose_chapter_page(head_text, tail_text, chapter_html,
                         chapter_title, prev_link, next_link, breadcrumb_label):
    breadcrumb = (
        f'\n<p style="margin:0 0 1.25rem;font-size:.85rem;color:var(--md-default-fg-color--light,#666);">'
        f'{breadcrumb_label} &rsaquo; <strong>{chapter_title}</strong></p>\n'
    )
    h1 = (f'\n<h1 id="chapter-top">{chapter_title}</h1>\n'
          f'<p style="margin:0 0 1.5rem;"><a href="../">&larr; Back to all chapters in {breadcrumb_label}</a></p>\n')
    nav = NAV_HTML
    nav = nav.replace("__PREV__", prev_link or '<span>&nbsp;</span>')
    nav = nav.replace("__NEXT__", next_link or '<span>&nbsp;</span>')
    new_body = APP_SHELL_LINE + breadcrumb + h1 + chapter_html + "\n" + nav + "\n</article>"
    return head_text + new_body + tail_text


def safe_link(slug, title):
    return f'<a href="../{slug}/" rel="next">{title}</a>'


def build_master_index(head_text, tail_text, topic_title, chapters):
    parts = [APP_SHELL_LINE]
    parts.append(f'\n<h1 id="{topic_title}">{topic_title}</h1>\n')
    parts.append(
        f'\n<p>This long topic has been split into {len(chapters)} chapters. '
        f'Pick one to read it on its own page, or open any chapter\'s '
        f'&quot;&larr; Back to all chapters&quot; link to return here.</p>\n'
    )
    parts.append('<ol style="line-height:1.9;">')
    for ch in chapters:
        parts.append(f'  <li><a href="./{ch["slug"]}/">{ch["title"]}</a></li>')
    parts.append('</ol>')
    parts.append('\n</article>')
    return head_text + "".join(parts) + tail_text


def process_topic(topic, chapters_plan):
    topic_dir = ROOT / topic
    src = topic_dir / "index.html"
    if not src.exists():
        print(f"  [skip] {topic}: no index.html")
        return
    text = src.read_text(encoding="utf-8")

    article_open_pos = text.find(APP_SHELL_LINE)
    article_close_pos = text.find("</article>", article_open_pos)
    if article_open_pos < 0 or article_close_pos < 0:
        print(f"  [skip] {topic}: can't locate article body")
        return

    body_start = article_open_pos + len(APP_SHELL_LINE)
    body_end = article_close_pos
    body = text[body_start:body_end]
    headings = enumerate_headings(text, body_start, body_end)

    # Resolve any start_offset_body / end_offset_body references for
    # fault-tolerant-tennis Ch 2 (the long text-only block).
    for ch in chapters_plan:
        if ch.get("start_anchor") == "what-is-fault-tolerance" and ch.get("end_after"):
            # Mark where Ch 1 ends (close of 'engage-the-posterior-chain')
            h_close = find_anchor_span(headings, ch["end_anchor"])
            if h_close:
                ch["_resolved_end"] = h_close["span_close"]
        if ch.get("slug") == "2-building-the-base" and topic == "fault-tolerant-tennis":
            ch["_resolved_start"] = find_anchor_span(headings, "engage-the-posterior-chain")["span_close"]
            ch["_resolved_end"] = find_anchor_span(headings, "smashing-through-plateaus")["span_open"]

    chapter_ranges = []
    for ch in chapters_plan:
        if "_resolved_start" in ch:
            chapter_ranges.append((ch, ch["_resolved_start"], ch["_resolved_end"]))
            continue
        start_h = find_anchor_span(headings, ch["start_anchor"])
        if start_h is None:
            print(f"    [warn] {topic}/{ch['slug']}: start anchor '{ch['start_anchor']}' not found")
            continue
        if ch.get("end_anchor"):
            end_h = find_anchor_span(headings, ch["end_anchor"])
            if end_h is None:
                print(f"    [warn] {topic}/{ch['slug']}: end anchor '{ch['end_anchor']}' not found")
                continue
            end = end_h["span_open"]
        else:
            end = len(body)
        chapter_ranges.append((ch, start_h["span_open"], end))

    head_text = text[:article_open_pos + len(APP_SHELL_LINE)]
    tail_text = text[article_close_pos + len("</article>"):]

    breadcrumb_label = topic.replace("-", " ").title()
    written = 0
    for i, (ch, c_start, c_end) in enumerate(chapter_ranges):
        prev_ch = chapters_plan[i - 1] if i > 0 else None
        next_ch = chapters_plan[i + 1] if i + 1 < len(chapter_ranges) else None
        prev_link = safe_link(prev_ch["slug"], "&laquo; " + prev_ch["title"]) if prev_ch else ""
        next_link = safe_link(next_ch["slug"], next_ch["title"] + " &raquo;") if next_ch else ""
        chapter_html = body[c_start:c_end].rstrip()
        # Rewrite image/script paths from ../../assets -> /assets
        # (absolute-from-site-root works regardless of folder depth on
        # GitHub Pages, so this is more robust than counting ../ segments).
        chapter_html = re.sub(r'(\.{2}/){2}assets/', r'/assets/', chapter_html)
        chapter_html = re.sub(r'(\.{2}/){2}assets/', r'/assets/', chapter_html)  # double-pass: ../../assets/ -> /assets/
        page_html = compose_chapter_page(
            head_text, tail_text, chapter_html, ch["title"],
            prev_link, next_link, breadcrumb_label,
        )
        chap_dir = topic_dir / ch["slug"]
        chap_dir.mkdir(exist_ok=True)
        (chap_dir / "index.html").write_text(page_html, encoding="utf-8")
        written += 1
        print(f"    wrote {topic}/{ch['slug']}/index.html  body={c_end - c_start} chars")

    # Build master topic index (replaces topic/index.html)
    topic_title = topic.replace("-", " ").title()
    master_html = build_master_index(head_text, tail_text, topic_title, chapters_plan)
    (topic_dir / "index.html").write_text(master_html, encoding="utf-8")
    print(f"  [{topic}] wrote {written} chapters + master")


def main():
    apply = "--apply" in sys.argv
    if not apply:
        print("DRY RUN. Use --apply to write.")
        for topic, plan in SPLIT_PLAN.items():
            print(f"\n{topic}: {len(plan)} chapters")
        return
    for topic, plan in SPLIT_PLAN.items():
        process_topic(topic, plan)


if __name__ == "__main__":
    main()