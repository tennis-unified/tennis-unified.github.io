"""Sub-splitter: take a chapter page that has no natural sub-section breaks
and split it into N roughly-equal sub-chapters using image boundaries.

For pages WITHOUT a sub-heading structure (e.g. fault-tolerant-tennis/2-building-the-base
which is one long essay), use the image positions as natural break points
and split into ~40-60K char sub-chapters each.

For pages WITH a heading structure (rare), use heading-based splitting.

Run:
    python sub_split.py [--apply]
"""

import os, re, sys, json
from pathlib import Path

ROOT = Path(r"D:/Github Repos/tennis-unified/tennis-wiki-reference")

NAV_HTML = """
<nav class="chapter-nav" aria-label="Chapter navigation" style="margin:3rem 0 1rem;padding:1.25rem;border-top:1px solid var(--md-default-fg-color--lightest,#ddd);display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;font-size:.95rem;">
  <div style="flex:1;text-align:left;">__PREV__</div>
  <div style="flex:1;text-align:center;"><a href="../" style="text-decoration:none;">Home</a></div>
  <div style="flex:1;text-align:right;">__NEXT__</div>
</nav>
"""

APP_SHELL_LINE = '<article class="md-content__inner md-typeset">'


def find_body_range(text):
    """Find the (head_with_article_open, body_text, tail_with_close_article)."""
    article_open = text.find(APP_SHELL_LINE)
    article_close = text.find("</article>", article_open)
    if article_open < 0 or article_close < 0:
        return None
    head = text[:article_open + len(APP_SHELL_LINE)]
    body = text[article_open + len(APP_SHELL_LINE): article_close]
    tail = text[article_close + len("</article>"):]
    return head, body, tail


def enumerate_headings(body):
    pat = re.compile(r'<(h[1-4])[^>]*\bid="([^"]+)"[^>]*>(.*?)</\1>', re.S)
    out = []
    for m in pat.finditer(body):
        anchor = m.group(2)
        out.append({
            "anchor": anchor,
            "level": int(m.group(1)[1]),
            "span": m.span(),
        })
    return out


def find_image_breaks(body, target_chunk_size=50000):
    """Find a list of body-offsets where each chunk ends — at image boundaries,
    each ~target_chunk_size chars after the previous break."""
    img_positions = [m.start() for m in re.finditer(r'<img\b', body)]
    if not img_positions:
        return [len(body)]
    breaks = [0]
    cur = 0
    for p in img_positions:
        if p - breaks[-1] >= target_chunk_size:
            breaks.append(p)
            cur = p
    if breaks[-1] < len(body):
        breaks.append(len(body))
    return breaks


def _decode_entities(s):
    """Decode HTML entities AND collapse whitespace for use in slugs/titles."""
    s = (s.replace("&rsaquo;", " ")
          .replace("&para;", "")
          .replace("&laquo;", "")
          .replace("&raquo;", "")
          .replace("&mdash;", "-")
          .replace("&middot;", "·")
          .replace("&amp;", "&"))
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def first_sentence(body_slice):
    """Return the first text sentence of a chunk for use as a sub-chapter title."""
    text = re.sub(r'<[^>]+>', '', body_slice)
    text = re.sub(r'\s+', ' ', text).strip()
    m = re.search(r'^[^.!?]+[.!?]', text)
    sentence = m.group(0).strip() if m else text[:80].strip()
    return _decode_entities(sentence[:90])


def find_image_breaks(body, target_chunk_size=50000):
    """Find a list of body-offsets where each chunk ends — at image boundaries,
    each ~target_chunk_size chars after the previous break. Always returns
    at least 2 entries (start and end of body)."""
    img_positions = [m.start() for m in re.finditer(r'<img\b', body)]
    if not img_positions:
        return [0, len(body)]
    breaks = [0]
    for p in img_positions:
        if p - breaks[-1] >= target_chunk_size:
            breaks.append(p)
    if breaks[-1] < len(body) - 200:  # if last chunk is tiny, fold it back
        breaks[-1] = len(body)
    elif breaks[-1] < len(body):
        breaks.append(len(body))
    return breaks


def safe_link(slug, title):
    return f'<a href="../{slug}/" rel="next">{title}</a>'


def write_subchapter_page(head_text, tail_text, body_chunk, sub_title,
                         prev_link, next_link, breadcrumb_label):
    breadcrumb = (
        f'\n<p style="margin:0 0 1.25rem;font-size:.85rem;color:var(--md-default-fg-color--light,#666);">'
        f'{breadcrumb_label} &rsaquo; <strong>{sub_title}</strong></p>\n'
    )
    h1 = (f'\n<h1 id="chapter-top">{sub_title}</h1>\n'
          f'<p style="margin:0 0 1.5rem;"><a href="../../">&larr; Back to all chapters in {breadcrumb_label}</a></p>\n')
    nav = NAV_HTML
    nav = nav.replace("__PREV__", prev_link or '<span>&nbsp;</span>')
    nav = nav.replace("__NEXT__", next_link or '<span>&nbsp;</span>')
    new_body = APP_SHELL_LINE + breadcrumb + h1 + body_chunk.rstrip() + "\n" + nav + "\n</article>"
    return head_text + new_body + tail_text


def process_chapter(chapter_dir, target_chunk_size=50000):
    """Split a chapter page into sub-chapters. Returns (parent_slug, list_of_subslug_titles)."""
    src = chapter_dir / "index.html"
    if not src.exists():
        return None
    text = src.read_text(encoding="utf-8")
    rng = find_body_range(text)
    if rng is None:
        print(f"  skip {chapter_dir}: no article body")
        return None
    head, body, tail = rng
    # Find any h3/h4 inside this chapter (post-split).
    headings = enumerate_headings(body)
    # Use a unique chapter title derived from existing breadcrumb / h1
    # In our existing structure, the parent topic is at chapter_dir.parent
    parent = chapter_dir.parent
    # breadcrumb label = topic name
    breadcrumb_label = parent.name.replace("-", " ").title()
    parent_h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', text)
    parent_h1 = parent_h1_match.group(1) if parent_h1_match else chapter_dir.name.replace("-", " ").title()

    # If there ARE sub-headings, use them; otherwise fall back to image breaks.
    if len(headings) >= 2 and False:  # disable h-based path; not used in current targets
        spans = [h["span"][0] for h in headings if h["level"] in (2, 3)]
        spans.append(len(body))
        spans = [s for s in spans if s > 200]
        chunks = []
        for i in range(len(spans) - 1):
            chunk_body = body[spans[i]:spans[i+1]]
            chunks.append((spans[i], spans[i+1], first_sentence(chunk_body), first_sentence(chunk_body)))
    else:
        spans = find_image_breaks(body, target_chunk_size=target_chunk_size)
        chunks = []
        for i in range(len(spans) - 1):
            slice_text = body[spans[i]:spans[i+1]]
            first = first_sentence(slice_text)
            chunks.append((spans[i], spans[i+1], first, first))

    # Build slug for each chunk
    sub_slugs = []
    for i, (c_start, c_end, sentence, sub_title) in enumerate(chunks):
        slug = f"{i+1:02d}-part-{i+1:02d}"
        # Try to slugify from first sentence
        if sentence:
            clean = _decode_entities(sentence)
            slug_words = re.findall(r'[A-Za-z]+', clean)[:5]
            if slug_words:
                slug = f"{i+1:02d}-" + "-".join(w.lower() for w in slug_words)
        sub_slugs.append((slug, _decode_entities(sub_title) or f"Part {i+1}"))

    # Write each sub-chapter
    written = []
    for i, (slug, sub_title) in enumerate(sub_slugs):
        prev_entry = sub_slugs[i - 1] if i > 0 else None
        next_entry = sub_slugs[i + 1] if i + 1 < len(sub_slugs) else None
        prev_link = safe_link(prev_entry[0], "&laquo; " + prev_entry[1]) if prev_entry else ""
        next_link = safe_link(next_entry[0], next_entry[1] + " &raquo;") if next_entry else ""
        body_chunk = body[chunks[i][0]:chunks[i][1]]
        # If the parent chapter's page didn't already use absolute paths,
        # the slice inherits them. Ensure body_chunk still has /assets/ paths.
        # (No rewrite needed — split_wiki.py already rewrote ../../assets -> /assets.)
        page_html = write_subchapter_page(
            head, tail, body_chunk, sub_title,
            prev_link, next_link, breadcrumb_label,
        )
        sub_dir = chapter_dir / slug
        sub_dir.mkdir(exist_ok=True)
        (sub_dir / "index.html").write_text(page_html, encoding="utf-8")
        written.append((slug, sub_title, chunks[i][1] - chunks[i][0]))

    # Replace original chapter's index.html with a master sub-chapter index
    parts = [APP_SHELL_LINE]
    parts.append(f'\n<h1 id="{parent_h1}">{parent_h1}</h1>\n')
    parts.append(f'\n<p>This long chapter has been split into {len(sub_slugs)} sub-chapters.</p>\n')
    parts.append('<ol style="line-height:1.9;">')
    for slug, sub_title, _ in written:
        parts.append(f'  <li><a href="./{slug}/">{sub_title}</a></li>')
    parts.append('</ol>\n')
    parts.append('\n<hr />\n')
    parts.append(
        f'<p><em>The original long page is preserved at '
        f'<a href="./original/">index.html &mdash; original long page</a>.</em></p>\n'
    )
    parts.append('\n</article>')
    master_html = head + "".join(parts) + tail

    # Save the original long page
    orig_dir = chapter_dir / "original"
    orig_dir.mkdir(exist_ok=True)
    (orig_dir / "index.html").write_text(text, encoding="utf-8")

    # Replace the chapter's index.html with the master
    (chapter_dir / "index.html").write_text(master_html, encoding="utf-8")
    return written


# Chapter pages that need sub-splitting (skipping angular-momentum clones).
# Each entry: (chapter_dir_rel_path, target_chunk_size).
# Only include pages where target_chunk_size yields >= 2 sub-chapters.
TARGETS = [
    ("fault-tolerant-tennis/2-building-the-base", 50000),   # 581K -> 9 sub-chapters
    ("serve-and-volley/3-strategy-primer-effective-net-rushing", 25000),  # 68K -> 2
    ("tennis-racket-sweet-spots/3-modern-tennis-rackets-balls-and-surfaces", 25000),  # 47K -> 1
]


def main():
    apply = "--apply" in sys.argv
    for rel, target in TARGETS:
        chapter_dir = ROOT / rel
        if not chapter_dir.exists():
            print(f"  skip {rel}: not found")
            continue
        if apply:
            written = process_chapter(chapter_dir, target_chunk_size=target)
            if written:
                print(f"  {rel}: split into {len(written)} sub-chapters")
                for s, t, sz in written:
                    print(f"    - {s:50s} ({sz:>6} chars)  {t[:60]!r}")
        else:
            print(f"  [dry] would split {rel} (target {target}/chunk)")


if __name__ == "__main__":
    main()