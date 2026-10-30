# -*- coding: utf-8 -*-
"""
Declare the language cluster for blog article pairs that have none.

The class
---------
The blog exists in two namespaces at mirrored paths, `/blog/<slug>/` and
`/vi/blog/<slug>/`. Of the 863 slugs in each, 48 pairs were declared in §35/§36.
The rest — 797 pairs — carry **no `hreflang` at all**, and 771 of the English
pages and 788 of the Vietnamese pages carry no canonical either. Nothing in the
tree relates the English article to its Vietnamese translation, so the two
compete as unrelated documents and the Vietnamese one is never offered to a
Vietnamese searcher.

Why this is not a blanket sweep
-------------------------------
The 797 pairs are not one class. Five distinct things are mixed in, and only the
first is this tool's business:

  canonicalised-elsewhere : a canonical already points at another URL. Someone
                            has decided this copy is not the one to index — that
                            is the `blog/*-2/` and G2 duplicate class, "do not
                            sweep". Refuse.
  duplicate -2 slug       : the slug ends `-2`, or a `-2`-stripped sibling
                            directory exists. Two copies of one article with no
                            decision made. Refuse.
  en-path-not-english     : the `/blog/` page holds Vietnamese prose. Writing
                            `hreflang="en"` on it would be a false statement, and
                            it is a language-declaration defect (§29.5), not a
                            missing cluster. Refuse.
  vi-path-not-vietnamese  : the `/vi/blog/` page is not Vietnamese. Same reason.
  thin                    : less than 1500 characters of article text on either
                            side. A cluster is worth declaring between two
                            articles; declaring one around two stubs is metadata
                            work on a page that needs writing (§31.1). Refuse.

What is left is a pair where both paths exist, both hold the language their path
claims, both hold a real article, and nobody has claimed either is a duplicate.

The values written
------------------
Nothing here is chosen:

  canonical            root-relative self, per the D1 per-host rule
  hreflang="en"        the /blog/ URL      (same on both pages)
  hreflang="vi"        the /vi/blog/ URL   (same on both pages)
  hreflang="x-default" the /blog/ URL      (measured: x-default == en href on
                                            7,150/7,150 pages that carry one)

The annotation set is therefore **identical on both pages**, which is the
invariant; it is not mirrored, because a mirrored set would give each page a
different `en` href.

Placement
---------
Immediately after the `<title>` line, at that line's indent. The sibling
generated blog page `blog/1-mot-cu-anh-banh-se-bao-gom-nhung-yeu/` already places
its canonical exactly there, so this matches the generator's own output rather
than imposing a new position.

Sitemap
-------
Adding a canonical makes a page self-canonical, which is this repo's definition
of indexable (`sitemap_coverage.py`). So `--sitemap` also adds the URLs it just
made indexable: `/blog/` to `sitemap.xml`, `/vi/blog/` to `vi/sitemap.xml`,
skipping any URL already present in either file.

Usage
-----
    python scripts/seo/blog_cluster_fix.py             # dry run
    python scripts/seo/blog_cluster_fix.py --write
    python scripts/seo/blog_cluster_fix.py --write --sitemap
"""
import argparse
import difflib
import os
import re
import sys
import urllib.parse
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LINK_TAG = re.compile(r"<link\b[^>]*>", re.I)
TITLE_LINE = re.compile(r"^([ \t]*)<title\b", re.I | re.M)
HEAD_END = re.compile(r"</head\s*>", re.I)
ATTR = re.compile(
    r"""([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))"""
)
ART = re.compile(r"<article\b.*?</article>", re.I | re.S)
MAIN = re.compile(r"<main\b.*?</main>", re.I | re.S)
SCRIPT = re.compile(r"<(script|style)\b.*?</\1>", re.I | re.S)
TAG = re.compile(r"<[^>]+>")
LOC = re.compile(r"<loc>\s*(.*?)\s*</loc>", re.S)

VI_CHARS = set(
    "ăâđêôơư"
    "àáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ"
    "ĂÂĐÊÔƠƯÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ"
)

MIN_ARTICLE_CHARS = 1500
MAX_EN_VI_DENSITY = 5.0     # the /blog/ page must be English
MIN_VI_VI_DENSITY = 15.0    # the /vi/blog/ page must be Vietnamese
MAX_SIMILARITY = 0.85       # same threshold as find_blog_variants()

SITEMAP_EN = "sitemap.xml"
SITEMAP_VI = "vi/sitemap.xml"
TODAY = "2026-10-29"


def attrs(tag):
    out = {}
    for m in ATTR.finditer(tag):
        key = m.group(1).lower()
        val = m.group(2)
        if val is None:
            val = m.group(3) if m.group(3) is not None else m.group(4)
        out[key] = val or ""
    return out


def parse_head(html):
    """(alternate langs, canonical href) from the whole document."""
    alts, canon = [], None
    for m in LINK_TAG.finditer(html):
        a = attrs(m.group(0))
        rel = (a.get("rel") or "").lower().split()
        if "alternate" in rel and "hreflang" in a:
            alts.append(a["hreflang"].strip().lower())
        elif "canonical" in rel:
            canon = a.get("href", "")
    return alts, canon


def article_text(html):
    m = ART.search(html) or MAIN.search(html)
    s = m.group(0) if m else html
    s = SCRIPT.sub(" ", s)
    s = TAG.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()


def vi_density(text):
    vi = sum(1 for c in text if c in VI_CHARS)
    ascii_alpha = sum(1 for c in text if c.isascii() and c.isalpha())
    total = vi + ascii_alpha
    return (vi / total * 100.0) if total else 0.0


def words(text):
    return re.findall(r"\w+", text.lower())


def same(a, b):
    return (a or "").rstrip("/") == (b or "").rstrip("/")


def classify(slug, en_html, vi_html):
    """Return (reason, None) to refuse, or (None, info) to accept."""
    en_alts, en_canon = parse_head(en_html)
    vi_alts, vi_canon = parse_head(vi_html)
    if en_alts or vi_alts:
        return "already-declared", None

    self_en = "/blog/%s/" % slug
    self_vi = "/vi/blog/%s/" % slug
    if (en_canon and not same(en_canon, self_en)) or (vi_canon and not same(vi_canon, self_vi)):
        return "canonicalised-elsewhere", None
    if slug.endswith("-2") or os.path.isdir(os.path.join(ROOT, "blog", slug[:-2])):
        return "duplicate -2 slug", None

    en_text, vi_text = article_text(en_html), article_text(vi_html)
    en_d, vi_d = vi_density(en_text), vi_density(vi_text)
    if en_d >= MAX_EN_VI_DENSITY:
        return "en-path-not-english", None
    if vi_d < MIN_VI_VI_DENSITY:
        return "vi-path-not-vietnamese", None
    if len(en_text) < MIN_ARTICLE_CHARS or len(vi_text) < MIN_ARTICLE_CHARS:
        return "thin", None
    ratio = difflib.SequenceMatcher(None, words(en_text), words(vi_text), autojunk=False).ratio()
    if ratio >= MAX_SIMILARITY:
        return "similar-dupe", None
    return None, dict(en_d=round(en_d, 2), vi_d=round(vi_d, 2), sim=round(ratio, 3),
                      en_len=len(en_text), vi_len=len(vi_text))


def block(self_url, twin_url, en_url, indent):
    rows = [
        ('canonical', self_url),
        ('en', en_url),
        ('vi', twin_url),
        ('x-default', en_url),
    ]
    out = []
    for kind, href in rows:
        if kind == "canonical":
            out.append('%s<link rel="canonical" href="%s">' % (indent, href))
        else:
            out.append('%s<link rel="alternate" href="%s" hreflang="%s">' % (indent, href, kind))
    return out


def insert_after_title(html):
    """Return (new_html, n_lines) or raise ValueError with a reason."""
    head = HEAD_END.search(html)
    if not head:
        raise ValueError("no </head>")
    head_html = html[: head.end()]
    titles = list(TITLE_LINE.finditer(head_html))
    if len(titles) != 1:
        raise ValueError("%d <title> tags in head" % len(titles))
    return titles[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--sitemap", action="store_true", help="also add the newly indexable URLs")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    blog_dir = os.path.join(ROOT, "blog")
    slugs = sorted(d for d in os.listdir(blog_dir)
                   if os.path.isfile(os.path.join(blog_dir, d, "index.html")))

    plan, refused, absent = [], Counter(), 0
    for slug in slugs:
        ep = os.path.join(ROOT, "blog", slug, "index.html")
        vp = os.path.join(ROOT, "vi", "blog", slug, "index.html")
        if not os.path.isfile(vp):
            absent += 1
            continue
        en_html = open(ep, encoding="utf-8", errors="replace").read()
        vi_html = open(vp, encoding="utf-8", errors="replace").read()
        reason, info = classify(slug, en_html, vi_html)
        if reason:
            refused[reason] += 1
            continue
        en_url = "/blog/%s/" % slug
        vi_url = "/vi/blog/%s/" % slug
        plan.append((slug, ep, vp, en_url, vi_url, info))

    print("slugs under blog/                 : %d" % len(slugs))
    print("  no /vi/blog/ twin               : %d" % absent)
    print("  refused                         : %d" % sum(refused.values()))
    for k, v in refused.most_common():
        print("     %-26s %d" % (k, v))
    print("  pairs to declare                : %d  (%d files)" % (len(plan), len(plan) * 2))
    print()

    if plan:
        import statistics
        print("accepted pair evidence:")
        print("   EN VI-density  median %5.2f%%  max %5.2f%%" % (
            statistics.median([p[5]["en_d"] for p in plan]), max(p[5]["en_d"] for p in plan)))
        print("   VI VI-density  median %5.2f%%  min %5.2f%%" % (
            statistics.median([p[5]["vi_d"] for p in plan]), min(p[5]["vi_d"] for p in plan)))
        print("   similarity     median %5.3f   max %5.3f" % (
            statistics.median([p[5]["sim"] for p in plan]), max(p[5]["sim"] for p in plan)))
        print()

    # ---- build edits ----
    edits = []
    for slug, ep, vp, en_url, vi_url, info in plan:
        for path, self_url, indent_src in ((ep, en_url, ep), (vp, vi_url, vp)):
            html = open(path, encoding="utf-8", errors="replace").read()
            try:
                m = insert_after_title(html)
            except ValueError as e:
                print("   SKIP %s: %s" % (path.replace(ROOT + os.sep, ""), e))
                continue
            indent = m.group(1)
            lines = block(self_url, vi_url, en_url, indent)
            nl = html.find("\n", m.end())
            if nl == -1:
                print("   SKIP %s: title line unterminated" % path)
                continue
            new = html[: nl + 1] + "\n".join(lines) + "\n" + html[nl + 1:]
            edits.append((path, new, lines))

    print("files to edit: %d" % len(edits))
    if args.verbose or not args.write:
        for path, _, lines in edits[:6]:
            print("   %s" % path.replace(ROOT + os.sep, "").replace(os.sep, "/"))
            for l in lines:
                print("      + %s" % l)
        if len(edits) > 6:
            print("   ... %d more" % (len(edits) - 6))
        print()

    if not args.write:
        print("DRY RUN. Re-run with --write to apply.")
        return 0

    for path, new, _ in edits:
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write(new)
    print("wrote %d files" % len(edits))

    # ---- sitemap ----
    if args.sitemap:
        def existing(sm):
            p = os.path.join(ROOT, sm)
            if not os.path.isfile(p):
                return set()
            t = open(p, encoding="utf-8", errors="replace").read()
            return {urllib.parse.unquote(urllib.parse.urlsplit(m.group(1).strip()).path)
                    for m in LOC.finditer(t)}

        have_en, have_vi = existing(SITEMAP_EN), existing(SITEMAP_VI)
        add_en = [p[3] for p in plan if p[3] not in have_en and p[3] not in have_vi]
        add_vi = [p[4] for p in plan if p[4] not in have_en and p[4] not in have_vi]
        # Each file already has a house style for blog entries; match it rather
        # than inventing one: root uses weekly/0.6, vi/sitemap uses monthly/0.6.
        for sm, urls, freq in ((SITEMAP_EN, add_en, "weekly"), (SITEMAP_VI, add_vi, "monthly")):
            if not urls:
                print("%s: nothing to add" % sm)
                continue
            p = os.path.join(ROOT, sm)
            t = open(p, encoding="utf-8", errors="replace").read()
            close = t.rfind("</urlset>")
            chunk = "".join(
                "  <url>\n"
                "    <loc>https://tenniskb.github.io%s</loc>\n"
                "    <lastmod>%s</lastmod>\n"
                "    <changefreq>%s</changefreq>\n"
                "    <priority>0.6</priority>\n"
                "  </url>\n" % (u, TODAY, freq) for u in urls)
            t = t[:close] + chunk + t[close:]
            with open(p, "w", encoding="utf-8", newline="") as fh:
                fh.write(t)
            print("%s: +%d URLs (%s, 0.6)" % (sm, len(urls), freq))
    return 0


if __name__ == "__main__":
    sys.exit(main())
