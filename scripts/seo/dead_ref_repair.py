#!/usr/bin/env python3
"""
dead_ref_repair.py — two provable repairs from the dead_links census.

RULE 1 (repoint, 50 edges): the "Đọc bằng Tiếng Việt" cross-link on
tennis-technical-reference pages is generated from the article's heading id
rather than its directory name, so a parenthesised slug loses its parentheses:

    /vi/tennis-technical-reference/backhand/ground-reaction-force-grf/   (dead)
    vi/tennis-technical-reference/backhand/ground-reaction-force-(grf)/  (real)

The repair only fires when the parent directory contains EXACTLY ONE directory
whose slug form equals the dead slug - i.e. the same article, spelled the way
the filesystem spells it. Anything ambiguous or unmatched is reported, not
touched. 131 further links have no VI twin at all; those are a translation gap,
not a path bug, and are left alone.

RULE 2 (unlink, 22 edges): books/court_diagrams.html and its VI twin cite
vi/books/tennis_tactics_vi.html and vi/books/spatial_dynamics_tennis_vi.html.
Neither reader was ever built - the books exist only as PDFs - so the citation
link goes to a 404. The link is removed and its text kept: guessing that
Tennis_Tactics_Vietnamese_Final.pdf is the book behind "Read Baseline Tactics"
is exactly the kind of guess this repo has learned not to make.

Idempotent. Report by default.

Usage:
  python scripts/seo/dead_ref_repair.py --root . [--write]
"""
import argparse
import os
import re
import urllib.parse
from pathlib import Path

TECH = "vi/tennis-technical-reference/"
LINK = re.compile(r"<a\b[^>]*?href=\"([^\"]*)\"[^>]*>(.*?)</a>", re.I | re.S)
UNLINK_TARGETS = ("vi/books/tennis_tactics_vi.html",
                  "vi/books/spatial_dynamics_tennis_vi.html")


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def to_fs(href, page):
    """href -> repo-relative path (no query/fragment), or None if external."""
    t = href.split("#")[0].split("?")[0]
    if not t or re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", t, re.I):
        return None
    t = urllib.parse.unquote(t)
    p = t.lstrip("/") if t.startswith("/") else os.path.normpath(
        os.path.join(os.path.dirname(page), t))
    return p.replace("\\", "/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    os.chdir(args.root)

    pages = []
    for dp, dn, fn in os.walk("."):
        dn[:] = [d for d in dn if d not in {".git", "node_modules", "__pycache__", ".github"}]
        for f in fn:
            if f.lower().endswith((".html", ".htm")):
                rel = os.path.relpath(os.path.join(dp, f), ".").replace("\\", "/")
                if not (rel.startswith("tnkb/") or rel.startswith("sources/")):
                    pages.append(rel)

    repointed = unlinked = 0
    files_changed = 0
    ambiguous, unmatched = [], []
    touched = []

    for page in pages:
        text = Path(page).read_text(encoding="utf-8", errors="ignore")
        new = text
        n_re = n_un = 0

        for m in LINK.finditer(text):
            href, inner = m.group(1), m.group(2)
            fs = to_fs(href, page)
            if fs is None:
                continue

            # RULE 1
            had_slash = href.split("#")[0].split("?")[0].endswith("/")
            if fs.startswith(TECH) and had_slash:
                if os.path.isdir(fs):
                    continue
                parent, base = os.path.dirname(fs), os.path.basename(fs.rstrip("/"))
                if not os.path.isdir(parent):
                    unmatched.append((page, href))
                    continue
                cands = [d for d in os.listdir(parent)
                         if os.path.isdir(os.path.join(parent, d)) and slug(d) == base]
                if len(cands) == 1:
                    target = os.path.join(parent, cands[0]).replace("\\", "/")
                    # A relative href must stay relative TO THE PAGE, not to the
                    # repo root: dropping the ../../../ prefix turns a cross-tree
                    # link into a path inside the current article's own directory.
                    if href.startswith("/"):
                        new_path = "/" + target
                    else:
                        new_path = os.path.relpath(target, os.path.dirname(page) or ".")
                        new_path = new_path.replace("\\", "/")
                    # spaces and & are legal on disk but must be encoded in a URL;
                    # parens stay literal (they are legal and the tree already uses them)
                    new_path = urllib.parse.quote(new_path, safe="/()'!*._~-")
                    frag = ("#" + href.split("#", 1)[1]) if "#" in href else ""
                    new_href = new_path.rstrip("/") + "/" + frag
                    # guard: the replacement must resolve from the page, or it is
                    # not a repair (this is what caught the relative-path bug)
                    chk = to_fs(new_href, page)
                    if not chk or not (os.path.isdir(chk) or os.path.exists(chk)
                                       or os.path.exists(chk + "/index.html")):
                        print(f"  !! {page}: {href} -> {new_href} does not resolve, skipped")
                        continue
                    old_tag = m.group(0)
                    new_tag = old_tag.replace('href="' + href + '"', 'href="' + new_href + '"', 1)
                    if new_tag != old_tag and old_tag in new:
                        new = new.replace(old_tag, new_tag, 1)
                        n_re += 1
                elif len(cands) > 1:
                    ambiguous.append((page, href, cands))
                else:
                    unmatched.append((page, href))
                continue

            # RULE 2
            if fs in UNLINK_TARGETS:
                old_tag = m.group(0)
                if old_tag in new:
                    new = new.replace(old_tag, inner.strip(), 1)
                    n_un += 1

        if n_re or n_un:
            files_changed += 1
            repointed += n_re
            unlinked += n_un
            touched.append((page, n_re, n_un))
            if args.write:
                Path(page).write_text(new, encoding="utf-8", newline="")

    print(f"pages scanned: {len(pages)}   files changed: {files_changed}")
    print(f"  rule 1 repointed: {repointed}   rule 2 unlinked: {unlinked}")
    print(f"  ambiguous (left alone): {len(ambiguous)}   unmatched/no VI twin: {len(unmatched)}")
    for p, h, c in ambiguous[:5]:
        print(f"    AMBIGUOUS {p} {h} -> {c}")
    if not args.write:
        print("(dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
