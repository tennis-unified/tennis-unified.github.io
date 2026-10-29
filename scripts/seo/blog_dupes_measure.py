#!/usr/bin/env python3
"""
blog_dupes_measure.py — READ-ONLY classification for G2 (duplicate canonical)
and G3b (lang fix) of the canonical proposals.

For each /blog/<slug>/ that declares lang="vi":
  A) TRUE DUPLICATE (G2): /vi/blog/<slug>/ exists, both lang="vi", and word-level
     sequence similarity >= 0.84 (difflib, autojunk=False). Canonical should move
     to /vi/blog/.
  B) ENGLISH-BODIED (G3b): VI-diacritic fraction < 2% -> the body is English but
     lang says vi. Should be lang="en".
  C) OTHER: genuinely Vietnamese, no twin, or a slug collision (low similarity).

Prints counts + the A and B slug lists (for the apply step). No writes.
"""
import re
import sys
import difflib
from pathlib import Path

VI_CHARS = r"[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]"


def body_text(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    t = re.sub(r"<script[\s\S]*?</script>", " ", t, flags=re.I)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return t


def vi_frac(p):
    b = body_text(p)
    vi = len(re.findall(VI_CHARS, b, re.I))
    letters = len(re.findall(r"[A-Za-zÀ-ỹ]", b))
    return vi / max(letters, 1)


def words(p):
    return re.findall(r"[a-z0-9]+", body_text(p).lower())


def lang_of(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'<html[^>]*\blang="([^"]*)"', t)
    return m.group(1) if m else None


def main():
    root = Path(sys.argv[1])
    A, B, C = [], [], []
    for bp in sorted((root / "blog").glob("*/index.html")):
        slug = bp.parent.name
        if lang_of(bp) != "vi":
            continue
        vp = root / "vi" / "blog" / slug / "index.html"
        vf = vi_frac(bp)
        rec = {"slug": slug, "vi_frac": round(vf, 4), "has_vi": vp.is_file()}
        if vp.is_file() and lang_of(vp) == "vi":
            wa, wb = words(bp), words(vp)
            sim = difflib.SequenceMatcher(None, wa, wb, autojunk=False).ratio()
            rec["sim"] = round(sim, 3)
            if sim >= 0.84:
                A.append(rec)
            elif vf < 0.02:
                B.append(rec)
            else:
                C.append(rec)
        else:
            if vf < 0.02:
                B.append(rec)
            else:
                C.append(rec)

    print(f"G2 TRUE DUPLICATES (both vi, sim>=0.84): {len(A)}")
    for r in A:
        print(f"  {r['slug']}  sim={r['sim']} vi_frac={r['vi_frac']}")
    print(f"\nG3b ENGLISH-BODIED (lang=vi, vi_frac<2%): {len(B)}")
    for r in B[:20]:
        print(f"  {r['slug']}  vi_frac={r['vi_frac']} has_vi={r['has_vi']}")
    if len(B) > 20:
        print(f"  ... and {len(B)-20} more")
    print(f"\nC OTHER (genuinely vi / collision / no twin): {len(C)}")
    for r in C[:8]:
        print(f"  {r['slug']}  vi_frac={r['vi_frac']} has_vi={r['has_vi']} sim={r.get('sim')}")


if __name__ == "__main__":
    main()
