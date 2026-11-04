#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_vi_pdfs.py — generate the A4 Vietnamese PDF for vi/books readers that
lack one (21 measured 2026-11-03; utility pages glossary.html and
court_diagrams.html are intentionally excluded).

Replicates the existing *_Vietnamese_Final.pdf house style (fingerprinted from
Zen_Tennis_Vietnamese_Final.pdf): A4 portrait, Arial TTF, reportlab PDF 1.3,
cover header "TENNIS FUTURE LAB · CHUYÊN KHẢO", MỤC LỤC page, justified body,
footer page numbers, metadata author 'Phạm Đức Hải' / creator 'Tennis Future Lab'.

Body extraction is structure-based: h1 title, h2/h3 headings, <p> paragraphs,
<img> (cover-art preferred; body images resolved relative to vi/books/).
Bold/italic inline markup is flattened to text (house PDFs are plain-text).

Usage:
  python scripts/books/build_vi_pdfs.py 1_the_art_of_modern_tennis_vi [...slug...]
  python scripts/books/build_vi_pdfs.py --all-missing
"""
import os
import re
import sys
import html as htmllib

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Image, PageBreak)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOOKS = os.path.join(ROOT, "vi", "books")

FONT_DIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("ArialVI", os.path.join(FONT_DIR, "arial.ttf")))
pdfmetrics.registerFont(TTFont("ArialVI-B", os.path.join(FONT_DIR, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("ArialVI-I", os.path.join(FONT_DIR, "ariali.ttf")))

BRAND = "TENNIS FUTURE LAB · CHUYÊN KHẢO"
S = {
    "h1": ParagraphStyle("h1", fontName="ArialVI-B", fontSize=22, leading=28,
                         spaceAfter=6, alignment=TA_CENTER),
    "cover-sub": ParagraphStyle("cover-sub", fontName="ArialVI", fontSize=12,
                                leading=16, alignment=TA_CENTER, textColor="#555555"),
    "brand": ParagraphStyle("brand", fontName="ArialVI", fontSize=9, leading=12,
                            alignment=TA_CENTER, textColor="#8a7433"),
    "h2": ParagraphStyle("h2", fontName="ArialVI-B", fontSize=15, leading=20,
                         spaceBefore=14, spaceAfter=6),
    "h3": ParagraphStyle("h3", fontName="ArialVI-B", fontSize=12, leading=16,
                         spaceBefore=10, spaceAfter=4),
    "p": ParagraphStyle("p", fontName="ArialVI", fontSize=10.5, leading=15.5,
                        alignment=TA_JUSTIFY, spaceAfter=7),
    "toc-h2": ParagraphStyle("toc-h2", fontName="ArialVI-B", fontSize=12, leading=17),
    "toc-h3": ParagraphStyle("toc-h3", fontName="ArialVI", fontSize=10, leading=14,
                             leftIndent=14),
    "toc-title": ParagraphStyle("toc-title", fontName="ArialVI-B", fontSize=18,
                                leading=24, spaceAfter=10),
}


def flat(fragment):
    """Inline markup -> plain text with entities resolved."""
    t = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", htmllib.unescape(t)).strip()


def parse_reader(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    low = t.lower()
    body = t[low.find("<body"):]
    title_m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S) or \
        re.search(r"<title>([^<]*)", t)
    title = flat(title_m.group(1)) if title_m else os.path.basename(path)
    # cover image lives in the pre-main header
    cover_art = None
    cm = re.search(r'<img[^>]*class="[^"]*cover-art[^"]*"[^>]*src="([^"]+)"', body) or \
        re.search(r'<img[^>]*src="([^"]+)"[^>]*class="[^"]*cover-art[^"]*"', body)
    if cm:
        cover_art = htmllib.unescape(cm.group(1))
    # content container: <main> … </main> when present, else whole body
    m = re.search(r"<main\b([\s\S]*?)</main>", body, re.I) or \
        re.search(r"<article\b([\s\S]*?)</article>", body, re.I)
    content = m.group(1) if m else body
    blocks = []
    for mm in re.finditer(r"<(h1|h2|h3|p)\b[^>]*>([\s\S]*?)</\1>|(<img\b[^>]*>)", content, re.I):
        if mm.group(3):  # self-closing img
            src = re.search(r'src="([^"]+)"', mm.group(3))
            if src:
                blocks.append(("img", htmllib.unescape(src.group(1))))
            continue
        tag, inner = mm.group(1).lower(), mm.group(2)
        txt = flat(inner)
        if not txt:
            continue
        blocks.append((tag, txt) if len(txt) > 1 or tag != "p" else ("p", txt))
    return title, blocks, cover_art


def img_flowable(src, maxh_mm=200):
    if src.startswith("/"):
        p = os.path.join(ROOT, src.lstrip("/"))
    else:
        p = os.path.join(BOOKS, src)
    if not os.path.exists(p):
        return None
    try:
        im = Image(p)
        w, h = im.imageWidth, im.imageHeight
        maxw, maxh = 160 * mm, maxh_mm * mm
        scale = min(maxw / w, maxh / h, 1.0)
        im.drawWidth, im.drawHeight = w * scale, h * scale
        return im
    except Exception:
        return None


def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("ArialVI", 8)
        canvas.setFillColor("#8a7433")
        canvas.drawCentredString(A4[0] / 2, 12 * mm, str(doc.page))
    canvas.restoreState()


def build(slug):
    src = os.path.join(BOOKS, slug + ".html")
    out = os.path.join(BOOKS, slug + "_Vietnamese_Final.pdf")
    title, blocks, cover_art = parse_reader(src)
    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=18 * mm, bottomMargin=20 * mm,
                          title=title, author="Phạm Đức Hải",
                          subject=title, creator="Tennis Future Lab")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])

    story = [Paragraph(BRAND, S["brand"]), Spacer(1, 60 * mm),
             Paragraph(title, S["h1"])]
    if cover_art:
        im = img_flowable(cover_art, maxh_mm=130)
        if im:
            story += [Spacer(1, 8 * mm), im]
    story += [PageBreak()]

    # MỤC LỤC from headings (skip the title itself and a leading Mục lục block)
    story.append(Paragraph("MỤC LỤC", S["toc-title"]))
    in_toc_h2 = False
    toc_items = [(lv, txt) for lv, txt in blocks
                 if lv in ("h2", "h3") and txt.lower() != "mục lục"]
    for lv, txt in toc_items:
        story.append(Paragraph(txt, S["toc-h2" if lv == "h2" else "toc-h3"]))
    story.append(PageBreak())

    for lv, val in blocks:
        if lv == "img":
            im = img_flowable(val)
            if im:
                story += [im, Spacer(1, 4 * mm)]
        elif lv == "p":
            story.append(Paragraph(val, S["p"]))
        else:
            story.append(Paragraph(val, S["h2" if lv == "h2" else "h3"]))
    doc.build(story)
    return out, len(blocks)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    if args[0] == "--all-missing":
        from slugs import MISSING  # noqa
    for slug in args:
        out, nblocks = build(slug)
        size = os.path.getsize(out) // 1024
        print("built %s (%d KB, %d content blocks)" % (os.path.basename(out), size, nblocks))


if __name__ == "__main__":
    main()
