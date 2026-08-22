#!/usr/bin/env python3
"""Detect chapter boundaries by scanning PDF text and extract per-chapter MD.

Strategy:
- For each page, extract page text.
- A page is a chapter start if its first non-empty line is a known chapter heading
  (case-insensitive, whitespace-tolerant match against a title list).
- Or: scan for big-font headings via pymupdf text blocks + size info.

Simpler & more reliable: pass an explicit (title, start_page) list, find the
right page by string-matching the title in the page text. This handles small
TOC offsets robustly.

Then assign end_page = next_start_page - 1, and last chapter ends at PDF end.
"""

import re
import fitz
from pathlib import Path

REPO = Path(r"C:\Users\Henry\Documents\GitHub\tennis-unified")
SRC_DIR = Path(r"C:\Users\Henry\Documents\New Tennis Knowledge\Tennis Books")

# Chapter titles in PDF order. Matching is substring + case-insensitive.
VOL2_TITLES = [
    "Introduction",
    "Features of Tennis:",
    "Basics of Tennis",
    "Tennis Instruction",
    "The Contact-Oriented",
    "Use of",
    "Skills Development:",
    "Developing and",
    "General Basics",
    "Training Coordination",
    "Training Techniques",
    "Training Tactics",
    "Training Conditioning",
    "Psychological Basics",
    "Planning for Training",
    "Competitive Coaching",
    "Sports-Medical",
    "The Pedagogical",
    "Index",
]

VOL1_TITLES = [
    "Introduction",
    "Basic Theory of",
    "Footwork in Tennis",
    "Stroke Techniques",
    "The Ball in Flight",
    "Tactics",
    "Toward a Terminology",
    "Ground Stroke",
    "Volley",
    "Serve",
    "Lob",
    "Smash",
    "Topspin",
    "Slice",
    "Drop Shot",
    "Half Volley",
    "Jump Smash",
    "Backhand Smash",
    "Service",
    "Individualized",
    "Index",
]


def find_chapter_pages(doc, titles):
    """For each title, return the page index where it first appears as a heading.

    Heuristic: title appears in the page text AND is followed by descriptive
    body text (so we don't match the TOC pages). Skip pages where text matches
    "Contents" pattern.
    """
    title_pages = []
    used_pages = set()
    for title in titles:
        title_low = title.lower()
        best_page = None
        for page_idx in range(doc.page_count):
            if page_idx in used_pages:
                continue
            text = doc[page_idx].get_text()
            # Skip pages that look like TOC (lots of page numbers in right margin)
            # Quick proxy: page with title appears alone on a page (no table-like layout)
            if title_low in text.lower():
                # Heuristic: real chapter page has title near top + lots of body
                lines = [l.strip() for l in text.splitlines() if l.strip()]
                # Find which line matches
                for i, line in enumerate(lines):
                    if title_low in line.lower():
                        # Is it the first heading-like line?
                        if i <= 5 and len(text) > 800:  # not TOC
                            best_page = page_idx
                            break
                if best_page is not None:
                    break
        if best_page is None:
            print(f"  [WARN] Could not locate '{title}'")
            title_pages.append((title, -1))
        else:
            title_pages.append((title, best_page))
            used_pages.add(best_page)
    return title_pages


def make_chapter_ranges(title_pages, total_pages):
    """Given (title, page_idx) list in order, return [(title, start, end)]."""
    ranges = []
    for i, (title, start) in enumerate(title_pages):
        if start == -1:
            continue
        if i + 1 < len(title_pages):
            next_start = title_pages[i + 1][1]
            end = next_start - 1 if next_start > 0 else total_pages - 1
        else:
            end = total_pages - 1
        ranges.append((title, start, end))
    return ranges


def extract_pages(doc, start_idx, end_idx):
    chunks = []
    for page_idx in range(start_idx, end_idx + 1):
        page = doc[page_idx]
        text = page.get_text()
        if text.strip():
            chunks.append(text.strip())
    return "\n\n<hr>\n\n".join(chunks)


def slugify(s):
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


def extract_volume(pdf_path, titles, out_dir, vol_label):
    doc = fitz.open(str(pdf_path))
    print(f"\n{'='*60}\n{vol_label}: {doc.page_count} pages\n{'='*60}")

    title_pages = find_chapter_pages(doc, titles)
    print(f"  Found {sum(1 for _, p in title_pages if p >= 0)}/{len(titles)} chapters")

    ranges = make_chapter_ranges(title_pages, doc.page_count)
    out_dir.mkdir(parents=True, exist_ok=True)

    extracted = []
    for ch_num, (title, start, end) in enumerate(ranges, 1):
        body = extract_pages(doc, start, end)
        if not body.strip():
            print(f"  [SKIP] {title}: empty range {start+1}-{end+1}")
            continue

        fname = f"{ch_num:02d}-{slugify(title)}.md"
        fpath = out_dir / fname

        md = (
            f"# Chapter {ch_num}: {title.strip()}\n\n"
            f"*Source: {vol_label}, PDF pages {start+1}–{end+1}.*\n\n"
            f"---\n\n"
            f"{body}\n"
        )
        fpath.write_text(md, encoding="utf-8")

        chars = len(body)
        words = len(body.split())
        extracted.append((ch_num, title.strip(), fname, words))
        print(f"  [OK] Ch{ch_num:>2}: {title[:55]:<55} p{start+1:>3}-{end+1:<3} ({words:>5,} words)")

    # Write index.md
    lines = [
        f"# {vol_label}",
        "",
        f"*Structured from PDF source: `{pdf_path.name}`. "
        f"{doc.page_count} pages total, {len(extracted)} chapters.*",
        "",
        "## Chapters",
        "",
    ]
    for ch_num, title, fname, words in extracted:
        lines.append(f"{ch_num}. [{title}]({fname}) — {words:,} words")
    lines.append("")
    (out_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"  [IDX] Wrote index.md")

    doc.close()
    return len(extracted)


def main():
    vol2_pdf = SRC_DIR / "Tennis_course_Vol2_Lessons and Training.pdf"
    vol1_pdf = SRC_DIR / "Tennis_course_Vol1_Techniques and Tactics.pdf"

    vol2_out = REPO / "docs" / "08-reference-library" / "tennis-books" / "tennis-course-vol2" / "en"
    vol1_out = REPO / "docs" / "08-reference-library" / "tennis-books" / "tennis-course-vol1" / "en"

    # Clear old extraction first
    for d in (vol2_out, vol1_out):
        if d.exists():
            for f in d.iterdir():
                f.unlink()

    extract_volume(vol2_pdf, VOL2_TITLES, vol2_out, "Tennis Course Vol 2 — Lessons and Training")
    extract_volume(vol1_pdf, VOL1_TITLES, vol1_out, "Tennis Course Vol 1 — Techniques and Tactics")


if __name__ == "__main__":
    main()