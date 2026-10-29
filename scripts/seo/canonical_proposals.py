#!/usr/bin/env python3
"""
canonical_proposals.py — READ-ONLY measurement for the canonical-decision
proposals (owner chose "prepare proposals, apply only after sign-off").

Measures three groups and prints a structured report:
  G1. 600 /articles/ edges: /articles/<EN-slug>/ vs /en/articles/<EN-slug>/ vs
      /vi/articles/<VI-slug>/ — existence, sitemap membership, word-set Jaccard.
  G2. 18 /blog/<vi-slug>/ duplicates: /blog/<slug>/ + /vi/blog/<slug>/ both vi.
  G3. <html lang> mismatches: path-language vs declared lang across all pages.

No writes. Output is meant to feed CANONICAL-PROPOSALS-*.md.
"""
import re
import sys
import json
from pathlib import Path
from urllib.parse import unquote

SITE = "https://tenniskb.github.io"


def norm(url):
    if url.startswith(SITE):
        url = url[len(SITE):]
    url = unquote(url)
    if not url.startswith("/"):
        url = "/" + url
    return url


def locs_of(xml_path):
    out = set()
    if not Path(xml_path).is_file():
        return out
    t = Path(xml_path).read_text(encoding="utf-8", errors="ignore")
    for m in re.finditer(r"<loc>([^<]+)</loc>", t):
        out.add(norm(m.group(1)))
    return out


def page_info(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    lang = re.search(r'<html[^>]*\blang="([^"]*)"', t)
    can = re.search(r'<link rel="canonical" href="([^"]*)"', t)
    return {
        "lang": (lang.group(1) if lang else None),
        "canonical": (can.group(1) if can else None),
        "len": len(t),
    }


def words(p):
    t = p.read_text(encoding="utf-8", errors="ignore")
    t = re.sub(r"<script[\s\S]*?</script>", " ", t)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    toks = re.findall(r"[a-z0-9]+", t.lower())
    return set(toks)


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def main():
    root = Path(sys.argv[1])
    sm_root = locs_of(root / "sitemap.xml")
    sm_vi = locs_of(root / "vi" / "sitemap.xml")
    all_locs = sm_root | sm_vi

    def in_sm(path):
        p = path if path.endswith("/") else path + "/"
        return p in all_locs

    print("### SITEMAP")
    print(f"root locs={len(sm_root)} vi locs={len(sm_vi)} total={len(all_locs)}")

    # ---------- G1: /articles/ ----------
    art_dir = root / "articles"
    slugs = sorted(p.parent.name for p in art_dir.glob("*/index.html")) if art_dir.is_dir() else []
    print(f"\n### G1 /articles/ slugs={len(slugs)}")
    g1 = {"both": 0, "no_en": 0, "no_vi": 0, "sm_articles": 0, "sm_en": 0, "sm_vi": 0,
          "dup_hi": 0, "dup_lo": 0, "samples": []}
    for s in slugs:
        ap = root / "articles" / s / "index.html"
        ep = root / "en" / "articles" / s / "index.html"
        vslug = "VI-" + s[3:] if s.startswith("EN-") else s
        vp = root / "vi" / "articles" / vslug / "index.html"
        has_en = ep.is_file()
        has_vi = vp.is_file()
        if has_en:
            g1["both"] += 1
        else:
            g1["no_en"] += 1
        if not has_vi:
            g1["no_vi"] += 1
        if in_sm(f"/articles/{s}/"):
            g1["sm_articles"] += 1
        if in_sm(f"/en/articles/{s}/"):
            g1["sm_en"] += 1
        if has_vi and in_sm(f"/vi/articles/{vslug}/"):
            g1["sm_vi"] += 1
        if has_en:
            j = jaccard(words(ap), words(ep))
            if j >= 0.80:
                g1["dup_hi"] += 1
            else:
                g1["dup_lo"] += 1
            if len(g1["samples"]) < 3:
                g1["samples"].append((s, round(j, 3), page_info(ap)["len"], page_info(ep)["len"]))
    print(f"  have /en twin: {g1['both']}  missing: {g1['no_en']}")
    print(f"  missing /vi twin: {g1['no_vi']}")
    print(f"  in sitemap: /articles/={g1['sm_articles']} /en/articles/={g1['sm_en']} /vi/articles/={g1['sm_vi']}")
    print(f"  Jaccard>=0.80 (near-dup): {g1['dup_hi']}  <0.80: {g1['dup_lo']}")
    for s, j, la, le in g1["samples"]:
        print(f"    sample {s[:40]}… jaccard={j} len(art={la},en={le})")

    # ---------- G2: /blog/ vi-at-en-URL ----------
    blog_dir = root / "blog"
    bslugs = sorted(p.parent.name for p in blog_dir.glob("*/index.html")) if blog_dir.is_dir() else []
    print(f"\n### G2 /blog/ slugs={len(bslugs)}")
    g2 = []
    for s in bslugs:
        bp = root / "blog" / s / "index.html"
        vp = root / "vi" / "blog" / s / "index.html"
        if not vp.is_file():
            continue
        bi = page_info(bp)
        vi = page_info(vp)
        if bi["lang"] == "vi" and vi["lang"] == "vi":
            j = jaccard(words(bp), words(vp))
            g2.append({
                "slug": s,
                "jaccard": round(j, 3),
                "sm_en_path": in_sm(f"/blog/{s}/"),
                "sm_vi_path": in_sm(f"/vi/blog/{s}/"),
                "en_canonical": bi["canonical"],
                "vi_canonical": vi["canonical"],
            })
    print(f"  both-lang=vi pairs: {len(g2)}")
    for r in g2[:25]:
        print(f"    {r['slug'][:45]:45} j={r['jaccard']} sm(blog)={r['sm_en_path']} sm(vi/blog)={r['sm_vi_path']}")

    # ---------- G3: <html lang> mismatches ----------
    print("\n### G3 <html lang> mismatches")
    mism = {"vi_decl_en": 0, "en_decl_vi": 0, "other": 0, "total": 0, "samples": []}
    by_dir = {}
    for p in root.rglob("index.html"):
        rel = p.relative_to(root).as_posix()
        if rel.startswith("tnkb/") or rel.startswith("sources/"):
            continue
        path_lang = "vi" if rel.startswith("vi/") else "en"
        info = page_info(p)
        lang = info["lang"]
        if lang is None:
            continue
        if lang != path_lang:
            mism["total"] += 1
            key = f"{path_lang}_decl_{lang}"
            if key == "vi_decl_en":
                mism["vi_decl_en"] += 1
            elif key == "en_decl_vi":
                mism["en_decl_vi"] += 1
            else:
                mism["other"] += 1
            top = rel.split("/")[0] if "/" in rel else rel
            by_dir[top] = by_dir.get(top, 0) + 1
            if len(mism["samples"]) < 5:
                mism["samples"].append(rel)
    print(f"  total mismatches: {mism['total']}  vi-path-but-lang=en: {mism['vi_decl_en']}  en-path-but-lang=vi: {mism['en_decl_vi']}  other: {mism['other']}")
    print("  by top dir:", dict(sorted(by_dir.items(), key=lambda x: -x[1])[:12]))
    for s in mism["samples"]:
        print("   sample:", s)


if __name__ == "__main__":
    main()
