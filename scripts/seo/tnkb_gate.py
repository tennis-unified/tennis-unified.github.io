#!/usr/bin/env python3
"""tnkb retirement safe-gate (Option C from SEO-DECISION-tnkb-orphan-2026-10-28.md).

Before any legacy page is converted to a redirect stub, verify that every
`tnkb/` HTML file has a real root twin that itself is NOT a meta-refresh
redirect (which would create a redirect loop). Also confirm the 8 root-sitemap
tnkb URLs resolve to existing root files.

Read-only. No files are modified.
"""
import os
import re
import random

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TNKB = os.path.join(REPO, "tnkb")
SITEMAP = os.path.join(REPO, "sitemap.xml")

REFRESH_RE = re.compile(r'<meta\s+http-equiv=["\']refresh["\']', re.I)
H1_RE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.I | re.S)


def h1_of(path):
    try:
        t = open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return None
    m = H1_RE.search(t)
    if not m:
        return None
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()[:90]


def main():
    htmls = []
    for dp, _, fn in os.walk(TNKB):
        for f in fn:
            if f.endswith(".html"):
                htmls.append(
                    os.path.relpath(os.path.join(dp, f), REPO).replace("\\", "/")
                )
    htmls.sort()
    print("tnkb html files:", len(htmls))

    missing = []
    loop_risk = []
    for p in htmls:
        assert p.startswith("tnkb/")
        rootp = p[len("tnkb/"):]
        full = os.path.join(REPO, rootp)
        if not os.path.exists(full):
            missing.append((p, rootp))
            continue
        try:
            txt = open(full, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        if REFRESH_RE.search(txt):
            loop_risk.append(rootp)

    print("missing root twins:", len(missing))
    for m in missing[:80]:
        print("  MISSING", m[0], "->", m[1])
    print("root twins that are themselves refresh-redirects (loop risk):",
          len(loop_risk))
    for r in loop_risk[:80]:
        print("  LOOP", r)

    # sitemap URLs
    sm = open(SITEMAP, encoding="utf-8", errors="replace").read()
    urls = re.findall(r"https://tenniskb\.github\.io/tnkb/[^<\s]*", sm)
    print("\ntnkb root-sitemap urls:", len(urls))
    for u in urls:
        rel = u.replace("https://tenniskb.github.io/", "")
        if rel.endswith("/"):
            rel += "index.html"
        full = os.path.join(REPO, rel)
        print("  ", u, "EXISTS" if os.path.exists(full) else "MISSING-FILE=" + rel)

    # sample h1 comparison
    random.seed(7)
    samp = random.sample(htmls, min(15, len(htmls)))
    print("\n--- sample h1 (tnkb vs root) ---")
    for p in samp:
        rootp = p[len("tnkb/"):]
        print("T:", h1_of(os.path.join(REPO, p)))
        print("R:", h1_of(os.path.join(REPO, rootp)))
        print()


if __name__ == "__main__":
    main()
