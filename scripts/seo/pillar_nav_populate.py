#!/usr/bin/env python3
"""
pillar_nav_populate.py — restore the reader's runtime navigation on the static
Pillars pages (prev/next + language switcher).

Background (session report §38):
  `pillar_static_gen.py` builds each static page by transforming the reader shell
  (`<dir>/article.html`). That shell carries three pieces of navigation that only
  work because `article.html` runs JavaScript:

      renderNav()               fills #nav-prev / #nav-next from `var ARTS`
      updateLanguageToggles()   repoints .md-select__link at the language twin

  The generator strips that whole script (`RE_RENDER_SCRIPT`) because the body is
  now server-rendered — so every generated page kept the markup and lost the only
  thing that populated it. Two symmetric defects, measured 2026-10-29:

    1. prev/next: 2,558/2,558 pages carry `nav-prev href="#"` and
       `nav-next href="#"` — 5,116 anchors that resolve to the page itself.
    2. language switcher: 2,558/2,558 pages have a `.md-select__link` pair that
       disagrees with the page's OWN `<head>` alternates. The template value is
       the catalog root, and on the 10-Pillars pages it points at the 5-Pillars
       set: "Tiếng Việt" on a 10-Pillars EN article went to
       `/vi/Tenniskb-5 Pillars/`. 5,116 hrefs that contradict the hreflang the
       same file declares.

  Both sets are in the sitemap and self-canonical, so this is the crawlable
  representation of the Pillars set.

ORDERING AUTHORITY (prev/next)
  The order is the `var ARTS` array of that directory's reader, not the filename
  sort and not the ART number. Measured: in `Tenniskb-10 Pillars` the ARTS order
  is neither alphabetical nor numerically monotonic, so any other order would
  make prev/next disagree with the reader the user came from.

  `Tenniskb-5 Pillars` ARTS lists 211 of the 259 .md files (210 of 259 for VI):
  ART numbers are duplicated there (ART-133..142 appear twice), and the reader
  lists one of each pair. Those unlisted pages still have a static page and a
  sitemap entry, so they are appended after the ARTS block in filename order —
  they get a defined position instead of a dead anchor.

LANGUAGE SWITCHER
  Target comes from the page's own `<head>` `hreflang="en"` / `hreflang="vi"`
  alternates, which are already correct and already audited (they are the same
  values `hreflang_reciprocal.py` and `xdefault_audit.py` check). Reusing them
  means the visible switcher and the declared cluster cannot drift apart.

LABELS
  The reader writes `"Prev: ART-001"` / `"Trước: ART-001"`. The localized word is
  read back out of the page's own label span rather than hard-coded, so the VI
  pages keep "Trước"/"Tiếp Theo" without a language table here.

Idempotent: a page whose anchors and switcher already resolve is skipped, so a
rerun reports 0. Safe by default: DRY RUN unless --write.

Usage:
  python scripts/seo/pillar_nav_populate.py --root .            # dry-run
  python scripts/seo/pillar_nav_populate.py --root . --write
  python scripts/seo/pillar_nav_populate.py --root . --dir "Tenniskb-10 Pillars" --write
"""
import argparse
import json
import re
from pathlib import Path

DIRS = ("Tenniskb-10 Pillars", "Tenniskb-5 Pillars",
        "vi/Tenniskb-10 Pillars", "vi/Tenniskb-5 Pillars")

RE_ARTS = re.compile(r"var ARTS\s*=\s*(\[[\s\S]*?\]);")
RE_ARTNUM = re.compile(r"(ART-\d+)")

# One anchor, non-greedy to its own close tag. The inner <span> holds no </a>,
# so this cannot swallow the sibling anchors.
RE_PREV = re.compile(r'<a id="nav-prev"[^>]*>[\s\S]*?</a>')
RE_NEXT = re.compile(r'<a id="nav-next"[^>]*>[\s\S]*?</a>')
RE_PREV_LBL = re.compile(r'(<span id="nav-prev-label">)([^<]*)(</span>)')
RE_NEXT_LBL = re.compile(r'(<span id="nav-next-label">)([^<]*)(</span>)')

# The visible language switcher pair, and the head alternates it must agree with.
RE_SW = re.compile(r'<a href="([^"]*)" hreflang="(en|vi)" class="md-select__link">([^<]*)</a>')
RE_ALT = re.compile(r'<link rel="alternate" href="([^"]*)" hreflang="(en|vi|x-default)">')


def art_num(name):
    """Bare digits, matching the reader's ARTS[].num ("001", not "ART-001").

    The two sources disagree on shape — ARTS stores "001" while a filename match
    yields "ART-179" — so normalize here or the labels come out half-prefixed.
    """
    m = RE_ARTNUM.match(name)
    return m.group(1)[4:] if m else None


def order_for(dirpath):
    """Return [(stem, art_num), ...] in the reader's navigation order.

    ARTS entries name the .md file; the static page is the same stem with .html.
    Any .md on disk that ARTS does not list is appended in filename order.
    """
    dirpath = Path(dirpath)
    reader = dirpath / "article.html"
    arts = []
    if reader.is_file():
        m = RE_ARTS.search(reader.read_text(encoding="utf-8", errors="replace"))
        if m:
            arts = json.loads(m.group(1))

    seen, order = set(), []
    for a in arts:
        f = a.get("file")
        if not f:
            continue
        stem = Path(f).stem
        if stem in seen:
            continue
        seen.add(stem)
        num = a.get("num")
        order.append((stem, re.sub(r"^ART-", "", num) if num else art_num(stem)))

    for p in sorted(dirpath.glob("*.md")):
        if p.stem not in seen:
            seen.add(p.stem)
            order.append((p.stem, art_num(p.stem)))
    return order


def _set_href(anchor, href):
    """Point the anchor at `href`, or make it inert when href is None.

    Inert mirrors the reader's own boundary state (`visibility = "hidden"`): the
    element stays for layout, but with no href it is not a link, so nothing
    resolves to the page itself.
    """
    if href is not None:
        if 'href="' in anchor:
            return re.sub(r'href="[^"]*"', lambda m: f'href="{href}"', anchor, count=1)
        return anchor.replace("<a ", f'<a href="{href}" ', 1)
    # drop href, hide
    out = re.sub(r'\shref="[^"]*"', "", anchor, count=1)
    if "visibility:hidden" in out:
        return out          # already inert — rerun must not stack the declaration
    if 'style="' in out:
        # the existing style ends in ";" — strip it so we do not emit ";;"
        return re.sub(r'(style="[^"]*?);?"',
                      lambda m: m.group(1).rstrip(";") + ";visibility:hidden\"", out, count=1)
    return out.replace("<a ", '<a style="visibility:hidden" ', 1)


def _set_label(anchor, pattern, word, num):
    """Replace the label span text with "<localized word>: ART-<num>"."""
    if num is None:
        return anchor
    return pattern.sub(lambda m: m.group(1) + f"{word}: ART-{num}" + m.group(3), anchor, count=1)


def fix_switcher(html):
    """Point the visible language switcher at the twin the <head> already declares.

    Returns (new_html, n_changed). Pages with no en/vi alternate (no true twin)
    are left alone — there is no correct target to substitute, and inventing one
    would create a non-reciprocal edge.
    """
    alt = dict((h, u) for u, h in RE_ALT.findall(html))
    if "en" not in alt or "vi" not in alt:
        return html, 0

    n = [0]

    def rep(m):
        href, lang, text = m.group(1), m.group(2), m.group(3)
        want = alt[lang]
        if href == want:
            return m.group(0)
        n[0] += 1
        return f'<a href="{want}" hreflang="{lang}" class="md-select__link">{text}</a>'

    return RE_SW.sub(rep, html), n[0]


def rewrite(html, prev, nxt):
    """Fill the prev/next anchors and the language switcher.

    `prev`/`nxt` are (stem, num) or None.
    Returns (new_html, changed).
    """
    orig = html
    href_prev = f"{prev[0]}.html" if prev else None
    href_next = f"{nxt[0]}.html" if nxt else None

    mp = RE_PREV.search(html)
    if mp:
        a = mp.group(0)
        word = RE_PREV_LBL.search(a)
        word = word.group(2).split(":")[0].strip() if word else "Prev"
        a2 = _set_label(_set_href(a, href_prev), RE_PREV_LBL, word, prev[1] if prev else None)
        html = html[:mp.start()] + a2 + html[mp.end():]

    mn = RE_NEXT.search(html)
    if mn:
        a = mn.group(0)
        word = RE_NEXT_LBL.search(a)
        word = word.group(2).split(":")[0].strip() if word else "Next"
        a2 = _set_label(_set_href(a, href_next), RE_NEXT_LBL, word, nxt[1] if nxt else None)
        html = html[:mn.start()] + a2 + html[mn.end():]

    html, _ = fix_switcher(html)
    return html, html != orig


def already_done(html):
    """True when the anchors resolve and the switcher agrees with the head."""
    mp = RE_PREV.search(html)
    mn = RE_NEXT.search(html)
    if not mp or not mn:
        return False
    for a in (mp.group(0), mn.group(0)):
        m = re.search(r'href="([^"]*)"', a)
        if m and (m.group(1) in ("#", "")):
            return False
    _, sw = fix_switcher(html)
    return sw == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--dir", action="append", default=None,
                    help="limit to one directory (repeatable)")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    targets = args.dir or DIRS

    total_changed = total_skipped = total_missing = total_sw = 0
    for d in targets:
        dd = root / d
        if not dd.is_dir():
            print(f"  WARN dir missing: {d}")
            continue
        order = order_for(dd)
        changed = skipped = missing = swfixed = 0
        for i, (stem, num) in enumerate(order):
            page = dd / (stem + ".html")
            if not page.is_file():
                missing += 1
                print(f"  MISSING {d}/{stem}.html")
                continue
            html = page.read_text(encoding="utf-8")
            if already_done(html):
                skipped += 1
                continue
            prev = order[i - 1] if i > 0 else None
            nxt = order[i + 1] if i + 1 < len(order) else None
            new, ok = rewrite(html, prev, nxt)
            if not ok:
                skipped += 1
                continue
            changed += 1
            swfixed += fix_switcher(html)[1]
            if args.write:
                page.write_text(new, encoding="utf-8", newline="")
        print(f"  {d:26s} order={len(order):5d}  changed={changed:5d}  "
              f"switcher={swfixed:5d}  skipped={skipped:5d}  missing={missing:3d}")
        total_changed += changed
        total_skipped += skipped
        total_missing += missing
        total_sw += swfixed

    print(f"\nSUMMARY: write={args.write} pages_changed={total_changed} "
          f"switcher_hrefs={total_sw} skipped={total_skipped} missing={total_missing}")
    if not args.write:
        print("  (dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
