#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reproduce the voice-pass metrics for a Vietnamese book, and test whether
they discriminate.

Why this exists
---------------
The handoff carries two editorial numbers that could not be re-measured from
this repository:

    Ch08 density 0.3079   ("pull back via loanwords if the band is a hard gate")
    "Forehand" vs "Thuận Tay" split, Ch04 50x vs Ch11 133x

The tool that produced the first one, `_voice_metrics.py`, lived only in the
voice-pass working clone (D:/Github Repos/tnkb-mirror-full), not here. A number
that cannot be reproduced from the repo is a number you have to take on trust,
which is the thing the handoff spends most of its words warning about. This
port makes it re-measurable, and adds the one thing the original did not do:
it reports the distribution, so you can see whether a threshold means anything.

What it measures
----------------
diacritic_density = VI-diacritic letters / total letters, over the body text
(after <style>/<script> removal and, when present, the content-wrap marker).
Higher means more of the prose is natively Vietnamese; ASCII/loanword-heavy
prose reads lower.

This is a blunt instrument. It is dominated by overall prose style, not by any
single term choice -- see the correlation report below.

Usage
-----
  python scripts/seo/voice_metrics.py
  python scripts/seo/voice_metrics.py --band 0.28,0.30
  python scripts/seo/voice_metrics.py --dir vi/cam-nang/Some_Book
"""

import os
import re
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DIR = "vi/cam-nang/Huong_Dan_Quan_Vot_Toan_Dien_Claude"

VI = set(
    "àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵ"
    "ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ"
)

# The two names this book uses for the same stroke.
TERM_EN = re.compile(r"\bforehand\b", re.I)
TERM_VI = re.compile(r"thu[ậa]n\s*tay", re.I)


def body_text(html):
    h = re.sub(r"<style.*?</style>", " ", html, flags=re.S | re.I)
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    i = h.find("content-wrap")
    if i != -1:
        h = h[i:]
    t = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"&[a-z]+;", " ", t)


def measure(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = body_text(fh.read())
    letters = [c for c in text if c.isalpha()]
    density = (sum(1 for c in letters if c in VI) / len(letters)) if letters else 0.0
    return density, len(TERM_EN.findall(text)), len(TERM_VI.findall(text)), len(letters)


def pearson(pairs):
    n = len(pairs)
    if n < 3:
        return float("nan")
    mx = sum(a for a, _ in pairs) / n
    my = sum(b for _, b in pairs) / n
    cov = sum((a - mx) * (b - my) for a, b in pairs)
    sx = sum((a - mx) ** 2 for a, _ in pairs) ** 0.5
    sy = sum((b - my) ** 2 for _, b in pairs) ** 0.5
    return cov / (sx * sy) if sx and sy else float("nan")


def main():
    book = DEFAULT_DIR
    if "--dir" in sys.argv:
        book = sys.argv[sys.argv.index("--dir") + 1]
    book = book if os.path.isabs(book) else os.path.join(ROOT, book)

    band = None
    if "--band" in sys.argv:
        lo, hi = sys.argv[sys.argv.index("--band") + 1].split(",")
        band = (float(lo), float(hi))

    rows = []
    for name in sorted(os.listdir(book)):
        if not name.lower().endswith((".html", ".htm")) or "Chuong" not in name:
            continue
        m = re.search(r"Chuong_(\d+)", name)
        if not m:
            continue
        d, en, vi, letters = measure(os.path.join(book, name))
        rows.append((m.group(1), d, en, vi, letters))

    if not rows:
        print(f"no chapter files found in {book}")
        return 1

    ds = sorted(r[1] for r in rows)
    q = statistics.quantiles(ds, n=4)
    print(f"chapters                     : {len(rows)}")
    print(f"diacritic density  min       : {ds[0]:.4f}")
    print(f"                   q1        : {q[0]:.4f}")
    print(f"                   median    : {statistics.median(ds):.4f}")
    print(f"                   q3        : {q[2]:.4f}")
    print(f"                   max       : {ds[-1]:.4f}")
    print(f"spread                       : {ds[-1] - ds[0]:.4f}")
    print(f"IQR                          : {q[2] - q[0]:.4f}")
    print(f"mean / pop sd                : {statistics.mean(ds):.4f} / {statistics.pstdev(ds):.4f}")

    print("\n-- rank, lowest density first (most ASCII/loanword heavy) --")
    for num, d, en, vi, _l in sorted(rows, key=lambda r: r[1]):
        print(f"  Ch{num}  {d:.4f}   forehand={en:>3}  thuận tay={vi:>3}")

    if band:
        lo, hi = band
        out = [r for r in rows if r[1] < lo or r[1] > hi]
        print(f"\n-- band [{lo:.2f}, {hi:.2f}] --")
        print(f"  chapters outside the band   : {len(out)} of {len(rows)}")
        for num, d, _e, _v, _l in sorted(out, key=lambda r: r[1]):
            print(f"    Ch{num}  {d:.4f}")
        print(
            "  If this count is large, the band is narrower than the book's own\n"
            "  natural variation and will flag chapters that are not outliers."
        )

    both = [r for r in rows if r[2] and r[3]]
    print(f"\n-- terminology --")
    print(f"  chapters using 'forehand'    : {sum(1 for r in rows if r[2])}")
    print(f"  chapters using 'thuận tay'   : {sum(1 for r in rows if r[3])}")
    print(f"  chapters using BOTH          : {len(both)}  {[r[0] for r in both]}")
    print(f"  total forehand / thuận tay   : {sum(r[2] for r in rows)} / {sum(r[3] for r in rows)}")

    pairs = [
        (r[1], r[2] / (r[2] + r[3])) for r in rows if r[2] + r[3]
    ]
    print(
        f"\n  Pearson r (density vs English-term share) = {pearson(pairs):+.3f}\n"
        "  A weak |r| means the two editorial questions are largely independent:\n"
        "  the density metric is not a proxy for terminology consistency."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
