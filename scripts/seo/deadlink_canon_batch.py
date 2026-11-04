#!/usr/bin/env python3
"""
deadlink_canon_batch.py — 2026-11-03 batch: two dead-link repoints, one truncated
index href, and the 8 root-hub duplicate canonicals (user-ratified policy: the
mirrored-path /en/ twin wins, sim threshold 0.85; see G1/G2 precedent).

Repairs
  R1  kinetic-chain slug: ../../biomechanics/the-kinetic-chain/ -> .../kinetic-chain/
      (51 EN + 3 VI referrers; target dir verified to exist at every referrer depth)
  R2  /vi/articles/the-chat/ -> /vi/handbook/29-the-chat/  (27 pages, 32 hrefs;
      anchor text "Thể Chất & Phục Hồi" matches the chapter-29 h1 "Thể Chất")
  R3  vi/articles/index.html: truncated href ...-retracti/ -> ...-retraction/
      (the generator cut the slug; the card pointed at a 404)
  R4  8 self-canonical root hubs (mental/{pressure,routine,visualization},
      patterns/{court-geometry,doubles,singles}, physical/{fitness,periodization})
      are near-duplicates of their linked /en/ twins (sim 0.860-0.919) -> canonical
      moves to the en twin; the 8 loser URLs are dropped from sitemap.xml (winners
      already listed). Pages stay 200-servable, no noindex (never both).

Idempotent. --dry-run (default) prints the plan; --apply writes.

Usage:
  python scripts/seo/deadlink_canon_batch.py --root . [--apply]
"""
import argparse
import os
import re
import sys

KINETIC_OLD = "../../biomechanics/the-kinetic-chain/"
KINETIC_NEW = "../../biomechanics/kinetic-chain/"
CHAT_OLD = 'href="/vi/articles/the-chat/"'
CHAT_NEW = 'href="/vi/handbook/29-the-chat/"'
TRUNCATED = "/vi/articles/VI-tenniskb-backhand-slice-drive-chest-compression-and-scapular-retracti/"
TRUNCATED_FIX = "/vi/articles/VI-tenniskb-backhand-slice-drive-chest-compression-and-scapular-retraction/"

DUP_HUBS = [
    ("mental", "pressure"), ("mental", "routine"), ("mental", "visualization"),
    ("patterns", "court-geometry"), ("patterns", "doubles"), ("patterns", "singles"),
    ("physical", "fitness"), ("physical", "periodization"),
]

SKIP_DIRS = {".git", "node_modules", "__pycache__", "sources", "_tmp", ".workbuddy-ai"}


def walk(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    n_kin_files = n_kin = n_chat_files = n_chat = 0
    for path in walk(root):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        orig = text
        k = text.count(KINETIC_OLD)
        c = text.count(CHAT_OLD)
        if rel == "vi/articles/index.html":
            t = text.count(TRUNCATED)
            if t:
                text = text.replace(TRUNCATED, TRUNCATED_FIX)
                print("R3 %s: truncated href fixed x%d" % (rel, t))
        if k:
            text = text.replace(KINETIC_OLD, KINETIC_NEW)
            n_kin_files += 1
            n_kin += k
        if c:
            text = text.replace(CHAT_OLD, CHAT_NEW)
            n_chat_files += 1
            n_chat += c
        if text != orig:
            print("R1/R2 %s: kinetic x%d, chat x%d" % (rel, k, c))
            if args.apply:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(text)
    print("R1 kinetic-chain: %d files, %d hrefs" % (n_kin_files, n_kin))
    print("R2 the-chat:      %d files, %d hrefs" % (n_chat_files, n_chat))

    # R4 — canonical moves
    for sec, leaf in DUP_HUBS:
        loser = os.path.join(root, sec, leaf, "index.html")
        rel = "%s/%s/index.html" % (sec, leaf)
        with open(loser, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        old = '<link rel="canonical" href="/%s/%s/">' % (sec, leaf)
        new = '<link rel="canonical" href="/en/%s/%s/">' % (sec, leaf)
        if old in text:
            print("R4 %s: canonical -> /en/%s/%s/" % (rel, sec, leaf))
            if args.apply:
                text2 = text.replace(old, new, 1)
                assert text2.replace(new, old, 1) == text, "byte-guard failed: " + rel
                with open(loser, "w", encoding="utf-8", newline="") as f:
                    f.write(text2)
        elif new in text:
            print("R4 %s: already canonical to en twin" % rel)
        else:
            print("R4 %s: canonical tag NOT FOUND — inspect manually" % rel)

    # R4b — sitemap removal
    smap = os.path.join(root, "sitemap.xml")
    with open(smap, encoding="utf-8", errors="ignore") as f:
        sm = f.read()
    removed = 0
    for sec, leaf in DUP_HUBS:
        pat = re.compile(
            r"<url>\s*<loc>https://tenniskb\.github\.io/%s/%s/</loc>.*?</url>\s*"
            % (re.escape(sec), re.escape(leaf)),
            re.S,
        )
        sm2, n = pat.subn("", sm)
        if n:
            removed += n
            sm = sm2
    print("R4b sitemap.xml: %d loser URLs removed" % removed)
    if args.apply and removed:
        with open(smap, "w", encoding="utf-8", newline="") as f:
            f.write(sm)

    if not args.apply:
        print("\nDRY RUN — no files written. Re-run with --apply.")


if __name__ == "__main__":
    main()
