# -*- coding: utf-8 -*-
"""
Repair broken hreflang alternates.

Measured on this tree: 5,618 pages carry hreflang, and 593 of them are wrong --
their alternate points at the language HOME ("/" or "/vi/") or at a path that
does not exist on disk. A page at /system/06.03-dit-deep-dive/ declaring

    <link rel="alternate" href="/" hreflang="en">
    <link rel="alternate" href="/vi/" hreflang="vi">

is telling Google "this article is the homepage". That is worse than no hreflang:
it corrupts the cluster the homepage belongs to.

The site's convention is that a translation lives at the mirrored path --
/en-ish path/ <-> /vi/<same path>/. So for each broken page:

  * both sides exist  -> emit the pair, root-relative (D1), pointing at the
                         real twins;
  * one side missing  -> remove the alternate pair entirely. A page with no
                         translation must not claim one.

Only pages with a broken tag are touched. The 5,025 pages whose pair already
resolves correctly are left byte-identical.

Usage:
  python scripts/seo/hreflang_fix.py            # dry run
  python scripts/seo/hreflang_fix.py --write
"""
import os
import re
import sys
from urllib.parse import quote, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", "node_modules", "_tmp", ".workbuddy-ai"}
SKIP_PREFIX = ("books/",)  # the book shelf is another stream's working tree

ALT_RE = re.compile(
    r'[ \t]*<link\s+rel="alternate"\s+href="([^"]*)"\s+hreflang="([^"]*)"\s*/?>[ \t]*\r?\n?',
    re.I,
)
HOMES = {"/", "/vi/", "/en/"}


def exists_dir(d):
    fs = os.path.join(ROOT, d.replace("/", os.sep))
    return os.path.isdir(fs) and any(
        os.path.isfile(os.path.join(fs, i)) for i in ("index.html", "index.htm")
    )


def resolve(base, href):
    """hreflang href -> normalised root path ('/a/b/'), or 'ABS', or None."""
    p = unquote(href).split("#")[0].split("?")[0]
    if p.lower().startswith("http"):
        return "ABS"
    full = p if p.startswith("/") else "/" + os.path.normpath(
        os.path.join(base, p)
    ).replace("\\", "/")
    full = re.sub(r"/+", "/", full)
    if full.endswith("/index.html") or full.endswith("/index.htm"):
        full = full.rsplit("/", 1)[0] + "/"
    if not full.endswith("/") and not os.path.splitext(full)[1]:
        full += "/"
    return full


def target_exists(path):
    p = path.strip("/")
    if p == "":
        return os.path.isfile(os.path.join(ROOT, "index.html"))
    fs = os.path.join(ROOT, p.replace("/", os.sep))
    if os.path.isdir(fs):
        return any(
            os.path.isfile(os.path.join(fs, i)) for i in ("index.html", "index.htm")
        )
    return os.path.isfile(fs)


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


def main():
    write = "--write" in sys.argv
    n_pages = n_repoint = n_drop = 0
    dropped = []
    repointed = []

    for full, rel in iter_html():
        text = open(full, "rb").read().decode("utf-8")
        matches = list(ALT_RE.finditer(text))
        if not matches:
            continue

        base = os.path.dirname(rel)
        selfpath = "/" + (base + "/" if base else "")
        if selfpath in HOMES:
            continue

        broken = False
        for m in matches:
            tgt = resolve(base, m.group(1))
            if tgt == "ABS":
                continue
            if tgt in HOMES or not target_exists(tgt):
                broken = True
                break
        if not broken:
            continue

        n_pages += 1
        is_vi = base == "vi" or base.startswith("vi/")
        enpath = base[3:] if is_vi else base
        vipath = base if is_vi else ("vi/" + base if base else "vi")
        has_en = exists_dir(enpath) if enpath else False
        has_vi = exists_dir(vipath)

        had_x = any(m.group(2).lower() == "x-default" for m in matches)
        indent = re.match(r"[ \t]*", matches[0].group(0)).group(0)

        if has_en and has_vi:
            en_href = quote("/" + enpath + "/", safe="/:@!$&'()*+,;=~-._")
            vi_href = quote("/" + vipath + "/", safe="/:@!$&'()*+,;=~-._")
            block = [
                f'{indent}<link rel="alternate" href="{en_href}" hreflang="en">\n',
                f'{indent}<link rel="alternate" href="{vi_href}" hreflang="vi">\n',
            ]
            if had_x:
                block.append(
                    f'{indent}<link rel="alternate" href="{en_href}" hreflang="x-default">\n'
                )
            n_repoint += 1
            repointed.append((rel, en_href, vi_href))
        else:
            block = []  # no translation: claim none
            n_drop += 1
            dropped.append((rel, "en" if not has_en else "", "vi" if not has_vi else ""))

        # replace the span covering every alternate tag (they are one block)
        start = text.rfind("\n", 0, matches[0].start()) + 1
        end = matches[-1].end()
        text = text[:start] + "".join(block) + text[end:]

        if write:
            with open(full, "wb") as fh:
                fh.write(text.encode("utf-8"))

    print(f"pages with a broken alternate : {n_pages}")
    print(f"  repointed to real twins     : {n_repoint}")
    print(f"  pair removed (no twin)      : {n_drop}")
    if dropped:
        print("\n--- hreflang removed (no twin exists) ---")
        for rel, missing_en, missing_vi in dropped[:30]:
            miss = " ".join(x for x in (missing_en, missing_vi) if x)
            print(f"  {rel}   (no {miss} twin)")
        if len(dropped) > 30:
            print(f"  ... and {len(dropped)-30} more")
    if not write:
        print("\nDRY RUN -- nothing written. Re-run with --write.")


if __name__ == "__main__":
    main()
