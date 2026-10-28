# -*- coding: utf-8 -*-
"""
Audit and repair hreflang problems that hreflang_fix.py does not cover.

hreflang_fix.py fixed *broken* alternates -- ones pointing at a language HOME ("/",
"/vi/", "/en/") or at a path that does not exist. Two defects survived it:

  1. SECTION-HOME drift. An alternate points at a *section* home instead of the real
     twin, e.g. the page at
         tennis-technical-reference/tactical-tennis/1-movement-.../index.html
     declares hreflang="vi" -> /vi/tennis-technical-reference/tactical-tennis/
     although /vi/tennis-technical-reference/tactical-tennis/1-movement-.../ exists.
     A section home is not a language home, so the earlier tool skipped it.

  2. DUPLICATE language codes. The Vietnamese page of that same article carries
         hreflang="vi" -> ./                                          (itself, fine)
         hreflang="vi" -> /vi/tennis-technical-reference/tactical-tennis/   (duplicate!)
     and no hreflang="en" at all. Google discards a cluster with two tags for one
     language, so the whole pair goes dark.

The repair rule is one line: an alternate must name the language of its TARGET, not copy
the language of the tag it replaces. So a bad tag is repointed at the real twin and its
hreflang is set from the twin's own path (vi/... -> "vi", otherwise "en").

Safety: every rewrite is validated per page -- if it would leave duplicate language
codes, or introduce a language code the page already uses, the page is left untouched and
reported instead. Nothing is written unless --write is passed.

Classes reported but NEVER rewritten (they need a decision, not a sweep):
  articles  /articles/ -> /en/articles/ : same-language duplicates. Two English copies of
            one article cannot be reciprocal by construction; canonical is the right tool.
  archive   anything touching tnkb/ : deliberate frozen snapshot.
  vi-book   vi/book/chapter-* : belongs to the books stream.

Usage:
  python scripts/seo/hreflang_reciprocal.py              # report
  python scripts/seo/hreflang_reciprocal.py --explain     # + per-edge detail
  python scripts/seo/hreflang_reciprocal.py --write       # apply the safe repoints
"""
import os
import posixpath
import re
import sys
from urllib.parse import quote, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", "node_modules", "_tmp", ".workbuddy-ai"}
SKIP_PREFIX = ("books/",)

ALT_RE = re.compile(
    r'([ \t]*)<link\s+rel="alternate"\s+href="([^"]*)"\s+hreflang="([^"]*)"\s*/?>([ \t]*\r?\n)?',
    re.I,
)
HTML_LANG_RE = re.compile(r'<html[^>]*\blang="([^"]*)"', re.I)
SAFE = "/:@!$&'()*+,;=~-._"


def norm_key(path):
    """Root-relative key. Collapses '.'/'..' segments, and is filesystem-aware because
    directory names like '09.1-det-drills' contain a dot and would otherwise be taken
    for files by splitext()."""
    p = posixpath.normpath("/" + path.strip("/"))
    if not p.startswith("/"):
        p = "/" + p
    if p.endswith("/index.html") or p.endswith("/index.htm"):
        p = p.rsplit("/", 1)[0]
        return p if p.endswith("/") else p + "/"
    if p == "/":
        return "/"
    fs = os.path.join(ROOT, p.strip("/").replace("/", os.sep))
    if os.path.isdir(fs):
        return p + "/"
    if os.path.isfile(fs):
        return p
    if not os.path.splitext(p)[1]:
        return p + "/"
    return p


def resolve(base, href):
    p = unquote(href).split("#")[0].split("?")[0]
    if p.lower().startswith(("http://", "https://")):
        return ("ABS", p)
    if not p:
        return ("BAD", href)
    if p.startswith("/"):
        return ("REL", norm_key(p))
    return ("REL", norm_key(os.path.join(base, p).replace("\\", "/")))


def lang_of_key(key):
    return "vi" if key.startswith("/vi/") else "en"


def twin_key(rel):
    """Mirrored path: 'a/b/' <-> 'vi/a/b/'."""
    key = norm_key(rel).strip("/")
    if key.startswith("vi/"):
        return "/" + key[3:] + "/"
    return "/vi/" + key + "/"


def iter_html():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if not f.lower().endswith((".html", ".htm")):
                continue
            rel = os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/")
            if rel.startswith(SKIP_PREFIX):
                continue
            yield os.path.join(dp, f), rel


def classify(src_rel, tgt_key):
    s = "/" + src_rel
    if s.startswith("/tnkb/") or tgt_key.startswith("/tnkb/"):
        return "archive"
    if s.startswith("/articles/") and (
        tgt_key.startswith("/en/articles/") or tgt_key.startswith("/vi/articles/")
    ):
        return "articles"
    if s.startswith("/vi/book/") and "chapter" in s.lower():
        return "vi-book"
    return "sections"


def build():
    pages = {}
    for full, rel in iter_html():
        with open(full, "rb") as fh:
            text = fh.read().decode("utf-8", "replace")
        alts = []
        for m in ALT_RE.finditer(text):
            kind, tgt = resolve(os.path.dirname(rel), m.group(2))
            alts.append((m.group(3).lower(), kind, tgt))
        if not alts:
            continue
        hl = HTML_LANG_RE.search(text)
        pages[rel] = {
            "key": norm_key(rel),
            "lang": (hl.group(1).lower().split("-")[0] if hl else None),
            "alts": alts,
            "path": full,
        }
    return pages


def dup_langs(alts):
    seen, dup = {}, []
    for lang, kind, _t in alts:
        if kind != "REL":
            continue
        if lang in seen:
            dup.append(lang)
        seen[lang] = True
    return dup


def plan_repoints(pages):
    """Mechanical repairs, planned per page and validated before acceptance.

    D. target/language invariant: a tag's href must be the mirrored twin for the
       language it declares -- hreflang="<own language>" -> this page,
       hreflang="<twin language>" -> the twin. Every observed defect is a violation of
       this: a tag pointing at itself, at a section home, or with the two languages
       swapped (VI page carrying en->itself and vi->the English page).
    B. self-duplicate: two tags for the page's own language, both resolving to itself,
       and no tag at all for the twin's language.
    """
    by_key = {p["key"]: rel for rel, p in pages.items()}
    plan_d, plan_b, rejected = [], [], []

    for rel, p in pages.items():
        twin = twin_key(rel)
        twin_exists = twin in by_key and twin != p["key"]
        if not twin_exists:
            continue
        twin_lang = lang_of_key(twin)
        self_lang = "vi" if p["key"].startswith("/vi/") else "en"

        with open(p["path"], "rb") as fh:
            text = fh.read().decode("utf-8")
        parsed = []
        for m in ALT_RE.finditer(text):
            indent, href, lang, tail = m.group(1), m.group(2), m.group(3).lower(), m.group(4) or ""
            kind, tgt = resolve(os.path.dirname(rel), href)
            parsed.append((m, lang, kind, tgt, indent, tail))

        edits = []  # (rule, match, new_lang, new_target)
        for m, lang, kind, tgt, indent, tail in parsed:
            if kind != "REL" or lang == "x-default":
                continue  # x-default names no language; its href is fixed elsewhere
            # Invariant: a tag's target must be the mirrored twin FOR ITS DECLARED
            # LANGUAGE. The site's convention (see hreflang_fix.py) is that a
            # translation lives at the mirrored path, so:
            #   hreflang="<own language>"  -> this page
            #   hreflang="<twin language>" -> the twin
            # Most defects are tags that violate this by pointing at themselves, at a
            # section home, or with the two languages swapped.
            if lang == self_lang:
                if tgt != p["key"]:
                    edits.append(("D", m, self_lang, p["key"]))
            elif lang == twin_lang:
                if tgt != twin:
                    edits.append(("D", m, twin_lang, twin))

        if not edits:
            # ---- B: pure self-duplicate of the page's own language ----
            by_lang = {}
            for item in parsed:
                if item[2] == "REL":
                    by_lang.setdefault(item[1], []).append(item)
            if twin_lang in by_lang or len(by_lang.get(self_lang, [])) < 2:
                continue
            selfs = [x for x in by_lang[self_lang] if x[3] == p["key"]]
            if not selfs or len(selfs) != len(by_lang[self_lang]):
                rejected.append((rel, "duplicate lang but not a pure self-duplicate"))
                continue
            m = selfs[-1][0]
            edits.append(("B", m, twin_lang, twin))

        # validate the whole page
        sim = text
        for rule, m, new_lang, new_tgt in edits:
            tail = m.group(4) or ""
            new_tag = f'{m.group(1)}<link rel="alternate" href="{quote(new_tgt, safe=SAFE)}" hreflang="{new_lang}">{tail}'
            sim = sim.replace(m.group(0), new_tag, 1)
        sim_alts = [
            (mm.group(3).lower(), *resolve(os.path.dirname(rel), mm.group(2)))
            for mm in ALT_RE.finditer(sim)
        ]
        dups = dup_langs(sim_alts)
        if dups:
            rejected.append((rel, "would leave duplicate lang codes: " + ",".join(sorted(set(dups)))))
            continue

        bucket = {"B": plan_b}.get(edits[0][0], plan_d)
        for rule, m, new_lang, new_tgt in edits:
            tail = m.group(4) or ""
            new_tag = f'{m.group(1)}<link rel="alternate" href="{quote(new_tgt, safe=SAFE)}" hreflang="{new_lang}">{tail}'
            old_tgt = resolve(os.path.dirname(rel), m.group(2))[1]
            bucket.append((rel, m.group(0), new_tag, f"{old_tgt} -> {new_tgt} [{new_lang}]"))

    return plan_d, plan_b, rejected


def main():
    write = "--write" in sys.argv
    pages = build()
    by_key = {p["key"]: rel for rel, p in pages.items()}

    buckets = {"articles": [], "vi-book": [], "archive": [], "sections": []}
    for rel, p in pages.items():
        for lang, kind, tgt in p["alts"]:
            if kind != "REL":
                continue
            other = by_key.get(tgt)
            if other is None:
                continue
            if any(k2 == "REL" and t2 == p["key"] for (l2, k2, t2) in pages[other]["alts"]):
                continue
            buckets[classify(rel, tgt)].append((rel, tgt, other, lang))

    dupe_pages = [(rel, dup_langs(p["alts"])) for rel, p in pages.items() if dup_langs(p["alts"])]

    print(f"pages with hreflang             : {len(pages):,}")
    print(f"non-reciprocal edges            : {sum(len(v) for v in buckets.values()):,}")
    for k in ("articles", "vi-book", "archive", "sections"):
        print(f"  {k:<9} : {len(buckets[k]):,}")
    print(f"pages with duplicate lang codes : {len(dupe_pages):,}")

    plan_d, plan_b, rejected = plan_repoints(pages)
    print(f"\nD. target/language invariant  : {len(plan_d)}")
    for rel, _o, _n, reason in plan_d[:6]:
        print(f"  {rel}\n      {reason}")
    if len(plan_d) > 6:
        print(f"  ... and {len(plan_d) - 6} more")
    print(f"B. self-duplicate repoints    : {len(plan_b)}")
    if rejected:
        print(f"\nrejected (need a human) : {len(rejected)}")
        for rel, why in rejected[:10]:
            print(f"  {rel}: {why}")

    if "--explain" in sys.argv:
        print("\n--- sections edges (need judgment, not rewritten) ---")
        for rel, tgt, other, lang in buckets["sections"][:40]:
            print(f"  {rel}  --[{lang}]-->  {tgt}")

    if not write:
        print("\nREPORT ONLY. Re-run with --write to apply D and B.")
        return

    touched = 0
    for rel, old, new, _reason in plan_d + plan_b:
        path = pages[rel]["path"]
        with open(path, "rb") as fh:
            text = fh.read().decode("utf-8")
        if old not in text:
            print(f"  SKIP (tag moved): {rel}")
            continue
        text = text.replace(old, new, 1)
        with open(path, "wb") as fh:
            fh.write(text.encode("utf-8"))
        touched += 1
    n_pages = len({r for r, *_ in plan_d + plan_b})
    print(f"\nrewrote {touched} alternate tags across {n_pages} pages")


if __name__ == "__main__":
    main()
