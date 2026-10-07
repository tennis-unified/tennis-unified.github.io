# -*- coding: utf-8 -*-
"""
Phase 2 - create en/index.html (the missing EN landing page).

The root index.html is the EN homepage but lives at "/". There is no "/en/"
landing page, so every internal href="/en/" 404s. This generates en/index.html
from the root index by:

  * rewriting root-relative links to their /en/ equivalents where that page
    exists under en/, and leaving them alone otherwise (the en/ tree only
    contains articles + the two pillar folders);
  * fixing <title>, canonical, and hreflang (absolute, with x-default).

Read-only on every other file. Writes exactly one new file.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

CANON = "https://tennis-unified.github.io"
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def read(p):
    with open(p, "r", encoding="utf-8", errors="surrogateescape", newline="") as f:
        return f.read()


def write(p, t):
    with open(p, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
        f.write(t)


def en_exists(root, url_path):
    """Does /en/<url_path>/index.html exist in the tree?"""
    rel = url_path.strip("/")
    if not rel:
        return True
    cand = os.path.join(root, "en", rel.replace("/", os.sep))
    return os.path.isfile(os.path.join(cand, "index.html")) or os.path.isfile(cand)


def main():
    src = os.path.join(ROOT, "index.html")
    dst = os.path.join(ROOT, "en", "index.html")
    html = read(src)

    # ---- 1. rewrite hrefs that have an /en/ twin -------------------------- #
    def fix_href(m):
        q = m.group(1)
        url = m.group(2)
        if not url.startswith("/") or url.startswith("//"):
            return m.group(0)
        if url.startswith("/en/") or url.startswith("/vi/"):
            return m.group(0)
        if url.startswith("/articles/") or re.match(r"^/Tenniskb-\d+ Pillars/", url):
            cand = "/en" + url
            if en_exists(ROOT, cand):
                return f'href{q}="{cand}"'
        return m.group(0)

    html = re.sub(r'href(["\'])(/[^"\']*)\1', fix_href, html)

    # ---- 2. title ---------------------------------------------------------- #
    html = re.sub(
        r"<title>[^<]*</title>",
        "<title>Tennis Unified Library — Tennis Knowledge Base</title>",
        html, count=1,
    )

    # ---- 3. canonical + hreflang ------------------------------------------- #
    # strip any existing canonical / alternate so we can insert cleanly
    html = re.sub(r'[ \t]*<link\s+rel="canonical"[^>]*>\r?\n?', "", html, flags=re.I)
    html = re.sub(r'[ \t]*<link\s+rel="alternate"[^>]*hreflang[^>]*>\r?\n?',
                  "", html, flags=re.I)

    block = (
        f'    <link rel="canonical" href="{CANON}/en/">\n'
        f'    <link rel="alternate" href="{CANON}/en/" hreflang="en">\n'
        f'    <link rel="alternate" href="{CANON}/vi/" hreflang="vi">\n'
        f'    <link rel="alternate" href="{CANON}/en/" hreflang="x-default">\n'
    )
    anchor = re.search(r'([ \t]*)<link\s+rel="icon"', html)
    if not anchor:
        anchor = re.search(r"([ \t]*)<meta\s+name=\"generator\"", html)
    if anchor:
        html = html[: anchor.start()] + block + html[anchor.start():]
    else:
        html = html.replace("</head>", block + "</head>", 1)

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    write(dst, html)
    print(f"wrote {dst}  ({len(html)} bytes)")
    print(f"  canonical : {CANON}/en/")
    print(f"  hreflang  : en, vi, x-default")


if __name__ == "__main__":
    main()
