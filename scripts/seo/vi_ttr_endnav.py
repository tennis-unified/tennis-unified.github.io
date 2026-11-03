#!/usr/bin/env python3
"""Restore the BOTTOM-NAV end-nav on vi/tennis-technical-reference pages.

Measured 2026-11-03: the VI translation of the tennis-technical-reference
corpus dropped the tu-bottom-nav end-nav that every EN twin carries. The
orphan audit shows the consequence: 152 self-canonical VI overview pages
(e.g. `backhand/One-Handed Backhand (1HBH)/`) with ZERO inbound <a href> —
their detail siblings (`backhand/one-handed-backhand-(1hbh)/`) link the
overview on EN (4x) but not on VI (0x).

For every VI ttr page that (a) has no BOTTOM-NAV block and (b) has an EN
twin at the mirrored path that HAS one, mirror the EN block with:
  - `← Prev` -> `← Trước`, `Next ->` -> `Tiếp ->`   (site's VI convention)
  - `🏠 Home`, href `/` -> `/vi/`, `Trang chủ`
  - article hrefs rewritten to their `/vi/...` form ONLY when the target
    exists on disk (never invent a link); otherwise the EN href is kept.
  - the prev/next chip captions taken from the TARGET page's own first h1
    (so VI pages show VI captions, EN targets keep EN captions).

Idempotent: pages already containing BOTTOM-NAV-START are skipped.

Usage:
  python vi_ttr_endnav.py --root .            # report
  python vi_ttr_endnav.py --root . --write    # apply
"""
import argparse
import os
import re

NAV_RE = re.compile(r"<!-- BOTTOM-NAV-START -->[\s\S]*?<!-- BOTTOM-NAV-END -->")
H1_RE = re.compile(r"<h1[^>]*>([\s\S]*?)</h1>", re.I)
TAG_RE = re.compile(r"<[^>]+>")
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.I | re.S)


def clean(s):
    return re.sub(r"\s+", " ", TAG_RE.sub("", s)).strip()


def page_caption(path):
    """First h1 text of the target page, else first <title> segment."""
    try:
        t = open(path, encoding="utf-8", errors="replace").read(200000)
    except OSError:
        return None
    m = H1_RE.search(t)
    if m:
        c = clean(m.group(1))
        if c:
            return c
    m = TITLE_RE.search(t)
    if m:
        return clean(m.group(1)).split(" - ")[0]
    return None


def vi_exists(root, en_href):
    """Does the /vi twin of an EN root-relative href exist on disk?"""
    p = en_href.split("#")[0].split("?")[0]
    if not p.startswith("/"):
        return None
    vi_p = "/vi" + p
    rel = vi_p.strip("/")
    if rel == "":
        return "/vi/" if os.path.isfile(os.path.join(root, "vi", "index.html")) else None
    cand = [os.path.join(root, rel, "index.html"), os.path.join(root, rel)]
    for c in cand:
        if os.path.isfile(c):
            return vi_p if c.endswith("index.html") else vi_p
    return None


def transform_block(block, root, vi_page_rel):
    """Mirror an EN BOTTOM-NAV block for the VI page vi_page_rel."""

    def fix_href(m):
        href = m.group(1)
        if href.startswith("/tennis-technical-reference/"):
            vi = vi_exists(root, href)
            if vi:
                return f'href="{vi}"'
            return m.group(0)  # keep EN target; still a working link
        if href == "/":
            return 'href="/vi/"'
        return m.group(0)

    block = re.sub(r'href="([^"]*)"', fix_href, block)
    block = block.replace("← Prev", "← Trước").replace("Next →", "Tiếp →")
    block = block.replace("🏠 Home", "🏠 Trang chủ")

    # captions: swap each prev/next chip's <span> caption for the target
    # page's own h1 text (VI pages get VI captions).
    def fix_caption(m):
        a = m.group(1)  # the <a ...> with href captured inside
        hm = re.search(r'href="([^"]+)"', a)
        if not hm:
            return m.group(0)
        href = hm.group(1).split("#")[0].split("?")[0]
        if not href.startswith("/vi/"):
            return m.group(0)
        rel = href.strip("/") + ("/index.html" if not href.endswith(".html") else "")
        cap = page_caption(os.path.join(root, rel))
        if not cap:
            return m.group(0)
        return re.sub(
            r"(<span[^>]*>)[^<]*(</span>)",
            lambda s: s.group(1) + cap[:80] + s.group(2),
            m.group(0),
            count=1,
        )

    block = re.sub(
        r"(<a\s[^>]*href=\"[^\"]*\"[^>]*>[\s\S]*?)<span[^>]*>[^<]*</span>",
        lambda m: fix_caption(m) if "Trước" in m.group(0) or "Tiếp" in m.group(0)
        else m.group(0),
        block,
    )
    return block


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)
    base = os.path.join(root, "vi", "tennis-technical-reference")

    fixed = skipped_noen = skipped_hadnav = skipped_notwin = 0
    for dp, dn, fn in os.walk(base):
        for f in fn:
            if not f.endswith(".html"):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            text = open(p, encoding="utf-8", errors="replace").read()
            if "BOTTOM-NAV-START" in text:
                skipped_hadnav += 1
                continue
            en_rel = rel[len("vi/"):]
            en_p = os.path.join(root, en_rel.replace("/", os.sep))
            if not os.path.isfile(en_p):
                skipped_notwin += 1
                continue
            en_text = open(en_p, encoding="utf-8", errors="replace").read()
            m = NAV_RE.search(en_text)
            if not m:
                skipped_noen += 1
                continue
            block = transform_block(m.group(0), root, rel)
            # insert before the last </article> (EN placement), else before </main>
            if "</article>" in text:
                i = text.rfind("</article>")
                new = text[:i] + block + "\n" + text[i:]
            elif "</main>" in text:
                i = text.rfind("</main>")
                new = text[:i] + block + "\n" + text[i:]
            else:
                skipped_noen += 1
                continue
            fixed += 1
            if args.write:
                with open(p, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(new)

    print(f"pages given an end-nav   : {fixed}" + ("" if args.write else "  (dry run)"))
    print(f"skipped (already has nav): {skipped_hadnav}")
    print(f"skipped (EN twin no nav) : {skipped_noen}")
    print(f"skipped (no EN twin)     : {skipped_notwin}")


if __name__ == "__main__":
    main()
