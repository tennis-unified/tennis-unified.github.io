# -*- coding: utf-8 -*-
"""
Phase 4 - extend search/search_index.json to cover the content spaces that are
currently missing.

The shipped index (4 062 docs) covers /foundation, /anatomy-lab, /elite,
/advanced, /angle-atlas ... but ZERO docs from the article spaces. The newest
third of the library is therefore invisible to on-site search.

This appends docs for:
    articles/**, en/articles/**, vi/articles/**   (the 200-article surface)
    vi/blog/**, blog/**                           (blog, EN side only if absent)

Schema matches the existing entries exactly: {"location","text","title"}.
Idempotent: re-running replaces previously-added docs instead of duplicating.
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IDX = os.path.join(ROOT, "search", "search_index.json")

MARK = "__seo_added__"          # marker stored under config to make runs idempotent

# NOTE: /articles/ is deliberately NOT indexed. It is the D2 mirror space --
# a byte-identical clone of /en/articles/ (see the plan). Indexing it would put
# two identical results in search for every article.
SPACES = ("en/articles", "vi/articles", "vi/blog")

# Cap per-doc text so one pathological page (97 KB observed) cannot bloat the
# index. Median doc is ~770 B; 8 KB comfortably covers a real article body.
MAX_TEXT = 8000


def read(p):
    with open(p, "r", encoding="utf-8", errors="surrogateescape", newline="") as f:
        return f.read()


def write(p, t):
    with open(p, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
        f.write(t)


def page_text(html):
    """Strip a page down to searchable prose the way MkDocs does."""
    # drop script/style/nav
    t = re.sub(r"<(script|style|nav|header|footer)[\s\S]*?</\1>", " ", html, flags=re.I)
    m = re.search(r"<article[\s\S]*?</article>", t, re.I)
    if m:
        t = m.group(0)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&nbsp;", " ", t)
    t = re.sub(r"&amp;", "&", t)
    t = re.sub(r"&[a-z]+;", " ", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()


def page_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    if not m:
        return ""
    t = re.sub(r"<[^>]+>", "", m.group(1))
    return t.strip()


def main():
    data = json.loads(read(IDX))
    cfg = data.setdefault("config", {})
    docs = data["docs"]

    # idempotency: drop docs added by a previous run of this script
    if cfg.get(MARK):
        docs[:] = [d for d in docs if not d.get(MARK)]
    base_count = len(docs)

    added = 0
    seen_locations = {d.get("location", "") for d in docs}

    for space in SPACES:
        d = os.path.join(ROOT, space)
        if not os.path.isdir(d):
            continue
        for dirpath, dirnames, filenames in os.walk(d):
            dirnames[:] = [x for x in dirnames
                           if x not in (".git", "__pycache__", "articles_md")]
            if "index.html" not in filenames:
                continue
            p = os.path.join(dirpath, "index.html")
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            loc = rel[: -len("index.html")]      # MkDocs style: dir path
            if loc in seen_locations:
                continue
            try:
                html = read(p)
            except Exception:
                continue
            title = page_title(html)
            # skip redirect stubs
            if re.match(r"^\s*(Redirecting|Chuyển hướng)", title, re.I):
                continue
            text = page_text(html)
            if not text:
                continue
            docs.append({
                "location": loc,
                "text": text[:MAX_TEXT],
                "title": title,
                MARK: True,
            })
            seen_locations.add(loc)
            added += 1

    cfg[MARK] = True
    write(IDX, json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    size = os.path.getsize(IDX)
    print(f"search index: {base_count} -> {base_count + added} docs "
          f"(+{added}); file {size/1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
