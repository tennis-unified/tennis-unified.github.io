#!/usr/bin/env python3
"""
lang_audit.py — measure <html lang> against the page's actual body language.

`<html lang>` is the strongest single language signal a page emits, and nothing in
the existing stack checks it. `canonical_lang_audit.py` compares a canonical's
source/target lang; `hreflang_reciprocal.py` compares hreflang claims. Neither
asks "is this page's own lang attribute true?".

Method: strip <script>/<style> blocks, strip tags, then measure the share of
letters that are Vietnamese-specific characters (diacritics + đ). A page whose
declared lang disagrees with its body at a given threshold is a candidate.

The threshold matters and is deliberately reported at three levels: a large part
of the `vi/` tree is *partially* translated, so no single attribute describes it.
The threshold-insensitive core (same verdict at 8/15/20%) is the actionable set.

Read-only. Report by default.

Usage:
  python scripts/seo/lang_audit.py --root . [--threshold 8] [--bucket] [--paths]
"""
import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".github"}
# archive tree: retired 2026-10-29, redirect stubs only
SKIP_PREFIX = ("tnkb/",)

HTML_TAG = re.compile(r"<html\b[^>]*>", re.I)
LANG_ATTR = re.compile(r"""\blang\s*=\s*["']?([A-Za-z-]+)""", re.I)
SCRIPT = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.I | re.S)
TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")

# Vietnamese-specific letters: base letters that only exist in Vietnamese, plus
# every tone-marked vowel. ASCII a/e/i/o/u/y are NOT counted (they are shared with
# English), so the ratio is "how much of this text is unmistakably Vietnamese".
VI_CHARS = set(
    "ăâđêôơư"
    "ĂÂĐÊÔƠƯ"
    "àáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ"
    "ÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ"
)
LETTER = re.compile(r"[^\W\d_]", re.UNICODE)


def body_stats(text):
    t = SCRIPT.sub(" ", text)
    t = TAG.sub(" ", t)
    t = WS.sub(" ", t)
    letters = 0
    vi = 0
    for ch in t:
        if LETTER.match(ch):
            letters += 1
            if ch in VI_CHARS:
                vi += 1
    words = len(t.split())
    return letters, vi, words


def declared_lang(text):
    m = HTML_TAG.search(text)
    if not m:
        return None
    lm = LANG_ATTR.search(m.group(0))
    return lm.group(1).lower() if lm else None


def bucket_of(rel):
    parts = rel.split("/")
    if len(parts) == 1:
        return "(root)"
    if parts[0] == "vi" and len(parts) > 1:
        return "vi/" + (parts[1] if len(parts) > 2 else "(root)")
    return parts[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--threshold", type=float, default=8.0)
    ap.add_argument("--min-words", type=int, default=40)
    ap.add_argument("--bucket", action="store_true", help="group candidates by directory")
    ap.add_argument("--paths", action="store_true", help="print every candidate path")
    ap.add_argument("--core", action="store_true",
                    help="only rows whose verdict is identical at 8/15/20%%")
    args = ap.parse_args()
    root = Path(args.root)

    rows = []
    total = 0
    for p in root.rglob("*.html"):
        rel = p.relative_to(root).as_posix()
        if any(rel.startswith(s) for s in SKIP_PREFIX):
            continue
        if any(part in SKIP_DIRS for part in rel.split("/")[:-1]):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        lang = declared_lang(text)
        if lang is None:
            continue
        letters, vi, words = body_stats(text)
        if words < args.min_words or letters == 0:
            continue
        total += 1
        ratio = 100.0 * vi / letters
        rows.append((rel, lang, ratio, words))

    def verdict(ratio, t):
        # a page is "Vietnamese-bodied" above t, "English-bodied" below
        return "vi" if ratio >= t else "en"

    def mismatched(row, t):
        _, lang, ratio, _ = row
        v = verdict(ratio, t)
        if lang == "vi":
            return v == "en"
        if lang == "en":
            return v == "vi"
        return False

    print(f"pages measured: {total} (body >= {args.min_words} words, lang declared, tnkb/ excluded)")
    for t in (8.0, 15.0, 20.0):
        n_vi_en = sum(1 for r in rows if r[1] == "vi" and verdict(r[2], t) == "en")
        n_en_vi = sum(1 for r in rows if r[1] == "en" and verdict(r[2], t) == "vi")
        print(f"  threshold {t:>4.0f}% VI:  lang=vi+EN-body {n_vi_en:>5}   lang=en+VI-body {n_en_vi:>5}   total {n_vi_en + n_en_vi:>5}")

    t = args.threshold
    cands = [r for r in rows if mismatched(r, t)]
    if args.core:
        cands = [r for r in cands
                 if mismatched(r, 8.0) and mismatched(r, 15.0) and mismatched(r, 20.0)]
    print(f"\ncandidates at threshold {t:.0f}%: {len(cands)}"
          + (" (threshold-insensitive core)" if args.core else ""))

    if args.bucket:
        by = defaultdict(Counter)
        for rel, lang, ratio, words in cands:
            by[bucket_of(rel)][f"lang={lang}"] += 1
        print(f"\n{'bucket':<44} {'lang=vi':>8} {'lang=en':>8}")
        for b, c in sorted(by.items(), key=lambda kv: -sum(kv[1].values())):
            print(f"{b:<44} {c['lang=vi']:>8} {c['lang=en']:>8}")

    if args.paths:
        print()
        for rel, lang, ratio, words in sorted(cands, key=lambda r: r[0]):
            print(f"{ratio:6.2f}%  {words:>6}w  lang={lang:<2}  {rel}")


if __name__ == "__main__":
    main()
