#!/usr/bin/env python3
"""
pillar_static_gen.py — generate a static, server-rendered HTML page per Pillars
article so the ~2,558 markdown articles become indexable.

Background (see session report §25.2):
  - EN articles:  Tenniskb-5 Pillars/*.md (259) + Tenniskb-10 Pillars/*.md (1020)
  - VI twins:     vi/Tenniskb-5 Pillars/*_VN.md (259) + vi/Tenniskb-10 Pillars/*_VN.md (1020)
  - They are served as text/markdown (not HTML) and the client-side reader
    (article.html) collapses every ?p= article to ONE canonical, so <=1 is
    ever indexed. Owner decided 2026-10-29: generate a static page per article.

What this does:
  For each .md, write a sibling <stem>.html by transforming the existing
  article.html shell (keeps brand/CSS/MathJax) with:
    - <title>            = article H1
    - canonical          = the static page's own URL
    - alternate en/vi    = this page + its language twin
    - alternate x-default= the EN twin URL
    - <meta description> = first paragraph
    - #article-body      = server-rendered markdown (Python `markdown`)
  The reader's renderArticle() script is stripped (content is now inline), so
  there is no client-side fetch that could re-overwrite the body.

EN<->VI pairing is by the ART-XXX number, robust to the slug map not matching.

Idempotent: rerun overwrites. Safe-by-default: DRY RUN unless --write.
Sitemap integration is a SEPARATE step (emits <root>/_pillar_urls.txt for it).

POST-NAV (added 2026-10-29, §38):
  The template's prev/next anchors and `.md-select__link` pair are placeholders
  that only the reader's JavaScript filled (`renderNav`, `updateLanguageToggles`),
  and build_page() strips exactly that script. So a generation pass used to ship
  2,558 pages with 5,116 dead `href="#"` anchors and 5,116 language-switcher hrefs
  pointing at a catalog root — 100% of pages, twice over. `--write` now ends with
  a call into `pillar_nav_populate.py`, which fills both from the `var ARTS` order
  and from each page's own `<head>` alternates. One implementation, shared with
  the standalone fixer, so a regeneration cannot reintroduce the defect.

Usage:
  python pillar_static_gen.py --root <repo>                 # dry-run, all
  python pillar_static_gen.py --root <repo> --limit 3       # pilot 3 per (set,lang)
  python pillar_static_gen.py --root <repo> --set t5 --write
  python pillar_static_gen.py --root <repo> --write         # generate all 2558
"""
import argparse
import json
import re
import sys
from pathlib import Path

import markdown

SITE = "https://tenniskb.github.io"

# (directory relative to repo root, language)
SET_DIRS = {
    "t5":  [("Tenniskb-5 Pillars", "en"), ("vi/Tenniskb-5 Pillars", "vi")],
    "t10": [("Tenniskb-10 Pillars", "en"), ("vi/Tenniskb-10 Pillars", "vi")],
}


def art_num(fname):
    m = re.match(r"(ART-\d+)", fname)
    return m.group(1) if m else None


def pair_key(s, p):
    """Language-twin key. T5 files are ART-XXX_<Slug>_EN/_VN.md and ART numbers
    are DUPLICATED (ART-133..142 twice), so pair by slug. T10 EN is
    ART-XXX-<slug>.md and VI is ART-XXX_VN.md (no slug), so pair by ART number
    normalized to int (fixes the 0991/991 zero-padding split)."""
    stem = p.stem
    if s == "t5":
        return re.sub(r"_(EN|VN)$", "", stem)
    # T10: exact ART string. Do NOT normalize to int — ART-0971 and ART-971 are
    # DIFFERENT articles (both exist), so int() would collide them.
    return art_num(stem) or stem


def strip_front_matter(md):
    return re.sub(r"^---\n[\s\S]*?\n---\n", "", md, count=1)


def preprocess(md):
    md = strip_front_matter(md)
    # mirror the reader's preprocessMarkdown arrow substitutions
    md = md.replace(r"$\rightarrow$", "\u2192").replace(r"$\to$", "\u2192").replace(r"$\leftarrow$", "\u2190")
    md = md.replace(r"\rightarrow", "\u2192").replace(r"\leftarrow", "\u2190")
    return md


def render(md):
    return markdown.markdown(preprocess(md), extensions=["tables", "fenced_code"])


def title_of(md):
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def desc_of(md):
    lines = strip_front_matter(md).splitlines()
    for i, l in enumerate(lines):
        if l.startswith("# "):
            for t in lines[i + 1:]:
                t = t.strip()
                if t and not t.startswith(("#", "*", ">", "`", "<")):
                    return (t[:155] + "\u2026") if len(t) > 155 else t
    return ""


def url_of(root, d, stem):
    # d may contain spaces; encode them as %20 (matches existing href convention)
    enc = (d + "/" + stem + ".html").replace(" ", "%20")
    return SITE + "/" + enc


# --- template transformation -------------------------------------------------
RE_CANON = re.compile(r'<link rel="canonical" href="[^"]*">')
RE_ALT_EN = re.compile(r'<link rel="alternate" href="[^"]*" hreflang="en">')
RE_ALT_VI = re.compile(r'<link rel="alternate" href="[^"]*" hreflang="vi">')
RE_TITLE = re.compile(r"<title>[^<]*</title>")
RE_DESC = re.compile(r'<meta name="description" content="[^"]*">')
RE_BODY = re.compile(r'<div id="article-body">.*?</div>', re.S)
RE_RENDER_SCRIPT = re.compile(r'<script>\s*// Article navigation data[\s\S]*?</script>')
RE_ALT_ANY = re.compile(r'[ \t]*<link rel="alternate"[^>]*>\s*\n')


def rel(u):
    """Root-relative href. The site is served on TWO hosts (tenniskb.github.io
    and tennis-unified.github.io), so an absolute canonical is a defect on one
    of them (canonical_audit class 3). Sitemap <loc> stays absolute separately."""
    return u[len(SITE):] if u.startswith(SITE) else u


def build_page(template, self_url, en_url, vi_url, title, desc, body_html, has_twin=True):
    # NOTE: use lambda replacers so dynamic content (which may contain LaTeX
    # backslashes like \oint) is inserted LITERALLY, not parsed as a re.sub
    # replacement escape ("bad escape \o").
    self_url, en_url, vi_url = rel(self_url), rel(en_url), rel(vi_url)
    t = template
    t = RE_CANON.sub(lambda m: f'<link rel="canonical" href="{self_url}">', t)
    if has_twin:
        # en alternate: for an EN page self==en_url; for a VI page it's the twin
        t = RE_ALT_EN.sub(lambda m: f'<link rel="alternate" href="{en_url}" hreflang="en">', t)
        t = RE_ALT_VI.sub(lambda m: f'<link rel="alternate" href="{vi_url}" hreflang="vi">', t)
        # insert x-default after the vi alternate
        t = RE_ALT_VI.sub(
            lambda m: m.group(0) + f'\n    <link rel="alternate" href="{en_url}" hreflang="x-default">',
            t, count=1,
        )
    else:
        # no true translation twin -> emit no cross-language alternate (a false
        # pairing would be a non-reciprocal edge). Canonical only.
        t = RE_ALT_ANY.sub("", t)
    t = RE_TITLE.sub(lambda m: f"<title>{title} - Tenniskb Pillars</title>", t)
    t = RE_DESC.sub(lambda m: f'<meta name="description" content="{desc}">', t)
    t = RE_BODY.sub(lambda m: f'<div id="article-body">{body_html}</div>', t)
    t = RE_RENDER_SCRIPT.sub(lambda m: "", t)  # drop client-side fetch/overwrite
    return t


def post_nav(root, dirs):
    """Re-apply the reader's prev/next and language switcher to the pages just written.

    build_page() strips the reader's script, which is what filled these at runtime,
    so without this step every regenerated page ships the template's dead anchors.
    The logic lives in pillar_nav_populate.py so there is exactly one implementation
    of the ordering and one of the switcher target rule.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from pillar_nav_populate import already_done, order_for, rewrite
    except ImportError:
        print("  WARN pillar_nav_populate.py not importable — run it manually after this")
        return 0
    n = 0
    for d in dirs:
        dd = root / d
        if not dd.is_dir():
            continue
        order = order_for(dd)
        for i, (stem, _num) in enumerate(order):
            p = dd / (stem + ".html")
            if not p.is_file():
                continue
            html = p.read_text(encoding="utf-8")
            if already_done(html):
                continue
            new, ok = rewrite(html,
                              order[i - 1] if i > 0 else None,
                              order[i + 1] if i + 1 < len(order) else None)
            if ok:
                p.write_text(new, encoding="utf-8", newline="")
                n += 1
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--set", choices=["t5", "t10", "all"], default="all")
    ap.add_argument("--lang", choices=["en", "vi", "both"], default="both")
    ap.add_argument("--limit", type=int, default=None, help="max articles per (set,lang) — for piloting")
    ap.add_argument("--write", action="store_true", help="apply; default is dry-run")
    args = ap.parse_args()

    root = Path(args.root)
    sets = SET_DIRS.keys() if args.set == "all" else [args.set]

    # 1) collect all md files + build (set, art, lang) -> (dir, stem) map for twinning
    entries = []  # (set_name, lang, d, stem, path)
    keymap = {}
    for s in sets:
        for d, lang in SET_DIRS[s]:
            dd = root / d
            if not dd.is_dir():
                print(f"  WARN dir missing: {d}")
                continue
            for p in sorted(dd.glob("*.md")):
                stem = p.stem
                key = pair_key(s, p)
                entries.append((s, lang, d, stem, p))
                keymap[(s, key, lang)] = (d, stem)

    # 2) load templates (one per language)
    tmpl = {}
    for s in sets:
        for d, lang in SET_DIRS[s]:
            if lang in tmpl:
                continue
            tp = root / d / "article.html"
            if not tp.is_file():
                print(f"  WARN template missing: {tp}")
                continue
            tmpl[lang] = tp.read_text(encoding="utf-8")

    # 3) generate
    written = 0
    skipped = 0
    errors = 0
    urls = []
    for (s, lang, d, stem, p) in entries:
        if args.lang != "both" and lang != args.lang:
            continue
        # limit handling (per set+lang)
        if args.limit is not None:
            # count within this (s, lang) group as we go
            seen = sum(1 for e in entries
                       if e[0] == s and e[1] == lang and entries.index(e) <= entries.index((s, lang, d, stem, p)))
            if seen > args.limit:
                continue
        key = pair_key(s, p)
        other = "vi" if lang == "en" else "en"
        self_url = url_of(root, d, stem)
        twin = keymap.get((s, key, other))
        has_twin = twin is not None
        twin_url = url_of(root, twin[0], twin[1]) if twin else self_url
        en_url = self_url if lang == "en" else twin_url
        vi_url = twin_url if lang == "en" else self_url

        try:
            md = p.read_text(encoding="utf-8")
            title = title_of(md) or stem
            desc = desc_of(md)
            body = render(md)
            page = build_page(tmpl[lang], self_url, en_url, vi_url, title, desc, body, has_twin=has_twin)
        except Exception as e:
            print(f"  ERROR {p}: {e}")
            errors += 1
            continue

        out = p.with_suffix(".html")
        urls.append(self_url)
        if not args.write:
            print(f"  [dry] {out.relative_to(root)}  ({len(page)} B)  vi={twin_url != self_url}")
            written += 1
            continue
        try:
            out.write_text(page, encoding="utf-8", newline="")
            written += 1
        except Exception as e:
            print(f"  ERROR write {out}: {e}")
            errors += 1

    # write url list for sitemap integration
    if args.write:
        ul = root / "_pillar_urls.txt"
        ul.write_text("\n".join(urls) + "\n", encoding="utf-8")
        print(f"  wrote {ul.name}: {len(urls)} urls")
        navd = post_nav(root, [d for s in sets for d, _l in SET_DIRS[s]])
        print(f"  post-nav: filled prev/next + switcher on {navd} pages")

    print(f"\nSUMMARY: set={args.set} lang={args.lang} limit={args.limit} "
          f"write={args.write} -> generated={written} errors={errors}")
    if not args.write:
        print("  (dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
