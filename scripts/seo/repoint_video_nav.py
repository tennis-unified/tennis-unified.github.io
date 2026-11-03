#!/usr/bin/env python3
"""Repoint the global 'Video Library' nav links from the shadow tree
tennis-video-library/ to the reachable, canonical coach-video-library/.

Only the INDEX-level links are repointed (5 exact forms). Deeper subdir links
(e.g. /tennis-video-library/tennis-volley/) point at shadow dirs we KEEP, so
they are deliberately left untouched.

Usage:
  python repoint_video_nav.py --root .            # report
  python repoint_video_nav.py --root . --write    # apply
"""
import argparse
import os

SKIP_DIRS = {".git", "node_modules", "tnkb", "assets", "site", "__pycache__"}
# (old exact substring) -> (new exact substring). Index-level links only.
REPL = [
    ('href="/vi/tennis-video-library/"',      'href="/coach-video-library/"'),
    ('href="/tennis-video-library/"',         'href="/coach-video-library/"'),
    ('href="../tennis-video-library/"',       'href="../coach-video-library/"'),
    ('href="https://tennis-unified.github.io/vi/tennis-video-library/"',
     'href="https://tennis-unified.github.io/coach-video-library/"'),
    ('href="https://tennis-unified.github.io/tennis-video-library/"',
     'href="https://tennis-unified.github.io/coach-video-library/"'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    total = 0
    changed_files = 0
    per = {o: 0 for o, _ in REPL}
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if not f.lower().endswith((".html", ".htm")):
                continue
            p = os.path.join(dp, f)
            text = open(p, encoding="utf-8", errors="replace").read()
            new = text
            for old, rep in REPL:
                c = new.count(old)
                if c:
                    per[old] += c
                    total += c
                    new = new.replace(old, rep)
            if new != text:
                changed_files += 1
                if args.write:
                    open(p, "w", encoding="utf-8", newline="\n").write(new)
    print("total link repoints:", total)
    for o, c in per.items():
        print(f"  {c:6d}  {o}")
    print("files changed:", changed_files)
    if not args.write:
        print("(dry run; --write to apply)")


if __name__ == "__main__":
    main()
