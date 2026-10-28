#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give each chapter of a dumped book its own <title>, and a description.

The problem
-----------
The 47 chapters of vi/cam-nang/Huong_Dan_Quan_Vot_Toan_Dien_Claude/ all carry
the same <title>:

    <title>Advanced Tennis Training Manual</title>

One English string, in a Vietnamese book, repeated 47 times. It is the browser
tab, the bookmark, the search result and the share card -- all identical. And
none of the 47 pages has a meta description at all.

The source of truth is the book's own index, which already carries a correct
Vietnamese title and a one-sentence summary for every chapter, written by the
author:

    <div class="ch-title">Chương 01: Sức Mạnh Đến Từ Mặt Đất</div>
    <div class="ch-desc">Chuỗi động học, lực phản hồi mặt đất và ...</div>

So nothing is invented and nothing is translated. This tool copies the author's
own words from the index into the chapter's <head>, and stops there.

Why "guarded"
-------------
The handoff records that term-map passes mangled <title>/brand/nav twice
(Ch09, Ch11) by rewriting text nodes they should not have touched. This tool
never rewrites text: it replaces one exact <title> element and inserts one
<meta> immediately before it. Every write is validated by reversing the two
substitutions and requiring the result to be byte-identical to the original.
A page that fails that check is skipped and reported, not written.

Usage
-----
  python scripts/seo/chapter_titles.py            # report
  python scripts/seo/chapter_titles.py --write
  python scripts/seo/chapter_titles.py --write --dir vi/cam-nang/Some_Book
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DIR = "vi/cam-nang/Huong_Dan_Quan_Vot_Toan_Dien_Claude"
BOOK = "Hướng Dẫn Quần Vợt Toàn Diện"
# Separator between the chapter name and the book name. NOT an em dash: 27 of
# the 47 chapter names already contain one ("Backhand — Từ Điểm Yếu Đến Vũ Khí"),
# and a dash separator turns those into three parallel clauses that read as one
# sentence. A middle dot cannot be confused with the author's own punctuation.
SEP = " · "
OLD_TITLE = "<title>Advanced Tennis Training Manual</title>"

ANCHOR_RE = re.compile(r'<a[^>]*href="[^"]*Chuong_(\d+)\.html"[^>]*>(.*?)</a>', re.S | re.I)
TITLE_RE = re.compile(r'<div[^>]*class="[^"]*ch-title[^"]*"[^>]*>(.*?)</div>', re.S | re.I)
DESC_RE = re.compile(r'<div[^>]*class="[^"]*ch-desc[^"]*"[^>]*>(.*?)</div>', re.S | re.I)
TITLE_TAG_RE = re.compile(r"<title>.*?</title>", re.S | re.I)
META_DESC_RE = re.compile(r'<meta[^>]+name="description"', re.I)


def plain(html):
    """Visible text of a fragment, whitespace collapsed."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def esc_attr(s):
    """Escape for a double-quoted attribute value.

    Only '"' and '&' can break out. '&' is absent from every summary in this
    book (measured), and '&amp;' must not be double-escaped, so bare '&' is
    escaped only when it does not already start an entity.
    """
    s = re.sub(r"&(?!#?\w+;)", "&amp;", s)
    return s.replace('"', "&quot;")


def load_index(book_dir):
    """chapter number -> (title, description), from the book's own index."""
    path = os.path.join(book_dir, "index.html")
    with open(path, encoding="utf-8") as fh:
        idx = fh.read()
    out = {}
    for m in ANCHOR_RE.finditer(idx):
        num, inner = m.group(1), m.group(2)
        if num in out:
            continue
        t = TITLE_RE.search(inner)
        d = DESC_RE.search(inner)
        if not t:
            continue
        out[num] = (plain(t.group(1)), plain(d.group(1)) if d else "")
    return out


def main():
    write = "--write" in sys.argv
    book_dir = DEFAULT_DIR
    if "--dir" in sys.argv:
        book_dir = sys.argv[sys.argv.index("--dir") + 1]
    book_dir = book_dir if os.path.isabs(book_dir) else os.path.join(ROOT, book_dir)

    meta = load_index(book_dir)
    print(f"chapters described by the index : {len(meta)}")

    plan, skipped, titles = [], [], []
    for name in sorted(os.listdir(book_dir)):
        if not name.lower().endswith((".html", ".htm")) or "Chuong" not in name:
            continue
        m = re.search(r"Chuong_(\d+)\.html$", name)
        if not m:
            continue
        num = m.group(1)
        if num not in meta:
            skipped.append((name, "no index entry"))
            continue
        full = os.path.join(book_dir, name)
        with open(full, "rb") as fh:
            text = fh.read().decode("utf-8")

        title, desc = meta[num]
        new_title = f"<title>{esc_attr(title)}{SEP}{BOOK}</title>"
        existing = TITLE_TAG_RE.findall(text)
        if len(existing) != 1:
            skipped.append((name, f"expected exactly one <title>, found {len(existing)}"))
            continue
        old_title_tag = existing[0]

        # Insert the description only when the page has none; replace the title
        # whenever it differs from the canonical form. That makes the tool
        # convergent: re-running it drives every page to the same state instead
        # of skipping pages that were already touched once.
        desc_tag = ""
        if not META_DESC_RE.search(text) and desc:
            desc_tag = f'<meta name="description" content="{esc_attr(desc)}"/>'
        if old_title_tag == new_title and not desc_tag:
            continue

        new = text.replace(old_title_tag, desc_tag + new_title, 1)

        # Reversal proof: undo both substitutions; anything but the original bytes
        # means the edit reached wider than the head.
        back = new.replace(desc_tag, "", 1) if desc_tag else new
        back = back.replace(new_title, old_title_tag, 1)
        if back != text:
            skipped.append((name, "change wider than the head edit"))
            continue
        if len(TITLE_TAG_RE.findall(new)) != 1:
            skipped.append((name, "not exactly one <title> afterwards"))
            continue

        plan.append((name, full, title, desc, new))
        titles.append(title)

    dupes = {t for t in titles if titles.count(t) > 1}
    print(f"pages to rewrite                : {len(plan)}")
    print(f"distinct titles after the pass  : {len(set(titles))}")
    print(f"duplicate titles                : {len(dupes)}")
    print(f"skipped                         : {len(skipped)}")
    for n, why in skipped:
        print(f"    {n}: {why}")
    for name, _f, t, d, _n in plan[:3]:
        print(f"  e.g. {name}\n       {t}\n       {d[:90]}{'...' if len(d) > 90 else ''}")

    if dupes:
        print("\nREFUSING TO WRITE: the derived titles are not unique.")
        return 1
    if not write:
        print("\nREPORT ONLY. Re-run with --write to apply.")
        return 0
    for _name, full, _t, _d, new in plan:
        with open(full, "wb") as fh:
            fh.write(new.encode("utf-8"))
    print(f"\nwrote {len(plan)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
