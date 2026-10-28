# -*- coding: utf-8 -*-
"""
Surface metadata: give every real landing/section page a share card and a
self-canonical.

Scope is the surface only -- the pages people actually land on and share:
  /                       root landing
  /<section>/             every top-level section index
  /vi/<section>/          the Vietnamese twins

Article pages, blog posts, book readers and the `sources/` imports are NOT
touched; `seo_fix.py` and `d1_treewide.py` own the article spaces.

Three rules, all of them "derive, never invent":

  1. A page with <meta http-equiv="refresh"> is a redirect stub. Skip it.
     Its canonical already names the destination and it should be noindex.
  2. canonical (when missing) = the page's own root-relative path. Under D1
     that resolves to whichever host serves it.
  3. The og/twitter block copies the page's OWN <title> and
     <meta name="description"> verbatim -- already attribute-escaped, so they
     are pasted as-is. A page with no description gets no og:description
     rather than a written-for-it sentence.

The template is not invented either: it is the block already used by
/vi/doubles/, which is the one shape in this tree that is correct.

Usage:
  python scripts/seo/surface_meta.py            # dry run
  python scripts/seo/surface_meta.py --write
"""
import os
import re
import sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", "node_modules", "_tmp", ".workbuddy-ai"}
SKIP_PREFIX = ("books/",)  # the book shelf is another stream's working tree

OG_IMAGE = "https://tennis-unified.github.io/assets/images/01_kinetic_chain_vs_wave.png"
SITE_NAME = "Tennis Unified Library"

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.S | re.I)
DESC_RE = re.compile(r'<meta\s+name="description"\s+content="([^"]*)"', re.I)
CANON_RE = re.compile(r'<link\s+rel="canonical"', re.I)
OGTITLE_RE = re.compile(r'<meta\s+property="og:title"', re.I)
REFRESH_RE = re.compile(r'<meta\s+http-equiv="refresh"', re.I)
HEAD_END_RE = re.compile(r"</head>", re.I)


def surface_pages():
    """(relpath, url_path) for the surface only."""
    out = []
    if os.path.isfile(os.path.join(ROOT, "index.html")):
        out.append(("index.html", "/"))
    for name in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, name)
        if not os.path.isdir(d) or name in SKIP_DIRS:
            continue
        f = os.path.join(d, "index.html")
        if os.path.isfile(f):
            out.append((name + "/index.html", "/" + name + "/"))
    vid = os.path.join(ROOT, "vi")
    if os.path.isdir(vid):
        for name in sorted(os.listdir(vid)):
            d = os.path.join(vid, name)
            if not os.path.isdir(d):
                continue
            f = os.path.join(d, "index.html")
            if os.path.isfile(f):
                out.append(("vi/" + name + "/index.html", "/vi/" + name + "/"))
    return [p for p in out if not p[0].startswith(SKIP_PREFIX)]


def build_block(url, title, desc):
    lang_vi = url == "/vi/" or url.startswith("/vi/")
    loc, alt = ("vi_VN", "en_US") if lang_vi else ("en_US", "vi_VN")
    href = quote(url, safe="/:@!$&'()*+,;=~-._")
    lines = [
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:title" content="{title}">',
    ]
    if desc:
        lines.append(f'<meta property="og:description" content="{desc}">')
    lines += [
        f'<meta property="og:url" content="{href}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        f'<meta property="og:locale" content="{loc}">',
        f'<meta property="og:locale:alternate" content="{alt}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{title}">',
    ]
    if desc:
        lines.append(f'<meta name="twitter:description" content="{desc}">')
    lines.append(f'<meta name="twitter:image" content="{OG_IMAGE}">')
    return "".join("    " + ln + "\n" for ln in lines)


def main():
    write = "--write" in sys.argv
    n_canon = n_og = n_skip_stub = n_nodesc = n_files = 0
    nodesc_urls = []

    for rel, url in surface_pages():
        full = os.path.join(ROOT, rel.replace("/", os.sep))
        raw = open(full, "rb").read()
        text = raw.decode("utf-8")

        if REFRESH_RE.search(text):
            n_skip_stub += 1
            continue

        m = TITLE_RE.search(text)
        if not m:
            continue
        title = re.sub(r"\s+", " ", m.group(1)).strip()
        d = DESC_RE.search(text)
        desc = re.sub(r"\s+", " ", d.group(1)).strip() if d else ""
        if not desc:
            n_nodesc += 1
            nodesc_urls.append(url)

        add = ""
        if not CANON_RE.search(text):
            add += '    <link rel="canonical" href="%s">\n' % quote(
                url, safe="/:@!$&'()*+,;=~-._"
            )
            n_canon += 1
        if not OGTITLE_RE.search(text):
            add += build_block(url, title, desc)
            n_og += 1

        if not add:
            continue

        end = HEAD_END_RE.search(text)
        if not end:
            print(f"  SKIP (no </head>): {rel}")
            continue
        # keep the block on its own line even when </head> follows a long
        # single-line <script>/<link> run
        if not text[: end.start()].endswith("\n"):
            add = "\n" + add
        new = text[: end.start()] + add + text[end.start():]
        assert new.count("<title>") == text.count("<title>")
        n_files += 1
        if write:
            with open(full, "wb") as fh:
                fh.write(new.encode("utf-8"))

    print(f"canonical added        : {n_canon}")
    print(f"og/twitter block added : {n_og}")
    print(f"files written          : {n_files}")
    print(f"redirect stubs skipped : {n_skip_stub}")
    print(f"pages with no description (no og:description emitted): {n_nodesc}")
    for u in nodesc_urls:
        print(f"    {u}")
    if not write:
        print("\nDRY RUN -- nothing written. Re-run with --write.")


if __name__ == "__main__":
    main()
