#!/usr/bin/env python3
"""
g2g3b_blog.py — apply G2 (duplicate canonical) + G3b (lang) of the proposals.

G2: /blog/<slug>/ that is a true duplicate of /vi/blog/<slug>/ (both lang=vi,
    word-level difflib similarity >= 0.84) -> canonical moves to /vi/blog/<slug>/,
    alternates removed, root sitemap drops /blog/<slug>/ and vi sitemap gains
    /vi/blog/<slug>/.
G3b: /blog/<slug>/ with lang="vi" but an English body (VI-diacritic fraction
    < 2%) and NOT a G2 duplicate -> set lang="en".

The two sets are disjoint by construction (G2 checked first). Idempotent.
DRY RUN unless --write.

Usage: python g2g3b_blog.py --root <repo> [--write]
"""
import argparse
import difflib
import gzip
import re
from pathlib import Path

VI_CHARS = r"[ăâđêôơưàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ]"
CANON = re.compile(r'<link rel="canonical" href="[^"]*">')
ALT = re.compile(r'[ \t]*<link rel="alternate"[^>]*>\s*\n')
HTML_TAG = re.compile(r"<html\b[^>]*>", re.I)


def body(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    t = re.sub(r"<script[\s\S]*?</script>", " ", t, flags=re.I)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t, flags=re.I)
    return re.sub(r"<[^>]+>", " ", t)


def vi_frac(p):
    b = body(p)
    vi = len(re.findall(VI_CHARS, b, re.I))
    return vi / max(len(re.findall(r"[A-Za-zÀ-ỹ]", b)), 1)


def words(p):
    return re.findall(r"[a-z0-9]+", body(p).lower())


def lang_of(p):
    m = re.search(r'<html[^>]*\blang="([^"]*)"', p.read_text(encoding="utf-8", errors="ignore"))
    return m.group(1) if m else None


def classify(root):
    A, B = [], []
    for bp in sorted((root / "blog").glob("*/index.html")):
        slug = bp.parent.name
        if lang_of(bp) != "vi":
            continue
        vp = root / "vi" / "blog" / slug / "index.html"
        sim = None
        if vp.is_file() and lang_of(vp) == "vi":
            sim = difflib.SequenceMatcher(None, words(bp), words(vp), autojunk=False).ratio()
        if sim is not None and sim >= 0.84:
            A.append((slug, bp))
        elif vi_frac(bp) < 0.02:
            B.append((slug, bp))
    return A, B


def drop_sitemap_blog(sm_text, slugs):
    n = 0
    for s in slugs:
        pat = re.compile(rf"[ \t]*<url>\s*<loc>https://tenniskb\.github\.io/blog/{re.escape(s)}/</loc>[\s\S]*?</url>\s*\n?")
        new = pat.sub("", sm_text)
        if new != sm_text:
            n += 1
        sm_text = new
    return sm_text, n


def ensure_vi_loc(sm_text, slugs, lastmod):
    added = 0
    for s in slugs:
        loc = f"https://tenniskb.github.io/vi/blog/{s}/"
        if f"<loc>{loc}</loc>" in sm_text:
            continue
        block = (f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
                 f"    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n")
        idx = sm_text.rfind("</urlset>")
        sm_text = sm_text[:idx] + block + sm_text[idx:]
        added += 1
    return sm_text, added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)
    from datetime import date
    lastmod = date.today().isoformat()

    A, B = classify(root)
    print(f"G2 duplicates: {len(A)}  G3b english-bodied: {len(B)}  write={args.write}")

    # G2
    g2_changed = 0
    for slug, bp in A:
        text = bp.read_text(encoding="utf-8", errors="ignore")
        tag = f'<link rel="canonical" href="/vi/blog/{slug}/">'
        if CANON.search(text):
            new = CANON.sub(lambda m: tag, text, count=1)
        elif "</title>" in text:
            # these /blog/ pages carry no canonical at all -> insert one
            new = text.replace("</title>", "</title>\n    " + tag, 1)
        else:
            new = text
        new = ALT.sub("", new)
        if new != text:
            g2_changed += 1
            if args.write:
                bp.write_text(new, encoding="utf-8", newline="")

    # G3b
    g3_changed = 0
    for slug, bp in B:
        text = bp.read_text(encoding="utf-8", errors="ignore")
        m = HTML_TAG.search(text)
        if not m:
            continue
        tag = m.group(0)
        newtag = re.sub(r"""(lang\s*=\s*["']?)vi(["\']?)""", r"\1en\2", tag, count=1, flags=re.I)
        if newtag == tag:
            continue
        g3_changed += 1
        if args.write:
            bp.write_text(text[:m.start()] + newtag + text[m.end():], encoding="utf-8", newline="")

    # sitemap
    smp = root / "sitemap.xml"
    sm = smp.read_text(encoding="utf-8", errors="ignore")
    sm, dropped = drop_sitemap_blog(sm, [s for s, _ in A])
    vp = root / "vi" / "sitemap.xml"
    vsm = vp.read_text(encoding="utf-8", errors="ignore")
    vsm, added = ensure_vi_loc(vsm, [s for s, _ in A], lastmod)

    print(f"G2 pages changed={g2_changed}  G3b pages changed={g3_changed}  sitemap dropped={dropped} added={added}")
    if args.write:
        smp.write_text(sm, encoding="utf-8", newline="")
        (root / "sitemap.xml.gz").write_bytes(gzip.compress(sm.encode(), mtime=0))
        vp.write_text(vsm, encoding="utf-8", newline="")
        (root / "vi" / "sitemap.xml.gz").write_bytes(gzip.compress(vsm.encode(), mtime=0))
        print("  wrote pages + sitemap.xml(.gz) + vi/sitemap.xml(.gz)")
    else:
        print("  (dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
