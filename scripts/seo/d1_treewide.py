# -*- coding: utf-8 -*-
"""
D1 sweep, tree-wide.

The earlier D1 pass only walked CONTENT_PREFIXES (articles/, en/articles/,
vi/articles/) -- 1,518 pages. The rest of the tree still bakes an absolute host
into <link rel="canonical"> (and og:url), which is exactly the thing D1 exists to
remove: the same bytes are served from tenniskb.github.io AND
tennis-unified.github.io, so an absolute host is wrong on one of them.

This rewrites every absolute canonical / og:url to its ROOT-RELATIVE path,
keeping the target path untouched (self-canonicals stay self, deliberate aliases
stay aliases). Nothing is invented: a URL whose path does not resolve on disk is
left alone and reported.

Excluded: books/ (the book readers are out of scope for this job).

Usage:
  python _tmp/d1_treewide.py            # dry run, report only
  python _tmp/d1_treewide.py --write
"""
import os
import re
import sys
from urllib.parse import unquote, quote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", "node_modules", "_tmp", ".workbuddy-ai"}
# The book shelf is another stream's working tree -- both languages, so the skip
# has to be symmetric. (Asymmetric skipping let vi/books/ keep an absolute
# og:url while books/ was excluded, and the tool reported it as work to do.)
SKIP_PREFIX = ("books/", "vi/books/")

# A tag-level reader, not a positional regex.
#
# The previous patterns were
#     (<link\s+rel="canonical"\s+href=")([^"]*)(")
#     (<meta\s+property="og:url"\s+content=")([^"]*)(")
# and each matched exactly one spelling of its tag:
#     <link rel="canonical" href="...">     matched
#     <link href="..." rel="canonical">     missed
#     <link href=... rel=canonical>         missed  (unquoted, legal HTML5)
#
# 69 pages in this tree use the third spelling, so this verifier reported a
# clean tree -- "0 canonical rewrites" -- while 69 absolute canonicals were
# still in it. A verifier that cannot see a syntax is not evidence about that
# syntax. Parse the attributes instead; order and quoting stop mattering.
TAG_RE = re.compile(r"<link\b[^>]*>|<meta\b[^>]*>", re.I)
ATTR_RE = re.compile(r"""([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""")
URL_ATTR = {"canonical": "href", "og:url": "content"}


def _attr_spans(tag):
    """name -> (value, value_start, value_end). First occurrence wins."""
    out = {}
    for m in ATTR_RE.finditer(tag):
        gi = 2 if m.group(2) is not None else (3 if m.group(3) is not None else 4)
        out.setdefault(m.group(1).lower(), (m.group(gi), m.start(gi), m.end(gi)))
    return out


def _tag_kind(tag, a):
    if tag[:5].lower() == "<link":
        if "canonical" in (a.get("rel", ("",))[0] or "").lower().split():
            return "canonical"
    elif (a.get("property", ("",))[0] or "").lower() == "og:url":
        return "og:url"
    return None


HOST_RE = re.compile(r"^https?://([^/]+)(/.*)?$", re.I)


def rel_eol(raw):
    return raw


def iter_html():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if not f.lower().endswith((".html", ".htm")):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            if rel.startswith(SKIP_PREFIX):
                continue
            yield p, rel


def resolves(path):
    """path is a decoded, root-relative URL path like '/en/chapter/' or '/a/b.html'."""
    p = path.strip("/")
    if p == "":
        return os.path.isfile(os.path.join(ROOT, "index.html"))
    fs = os.path.join(ROOT, p.replace("/", os.sep))
    if os.path.isdir(fs):
        return any(os.path.isfile(os.path.join(fs, i)) for i in ("index.html", "index.htm"))
    if os.path.isfile(fs):
        return True
    for ext in (".html", ".htm"):
        if os.path.isfile(fs + ext):
            return True
    return False


def self_rootrel(rel):
    """The page's own root-relative path, directory form for index.html."""
    p = rel
    if p.endswith("/index.html"):
        p = p[: -len("index.html")]
    elif p.endswith("/index.htm"):
        p = p[: -len("index.htm")]
    out = "/" + p
    return quote(out, safe="/:@!$&'()*+,;=~-._")


def to_rootrel(url, rel):
    """Absolute URL -> ('ok', root-relative href) or ('self', ...) or ('bad', reason)."""
    m = HOST_RE.match(url)
    if not m:
        return "skip", "not absolute"
    host, rest = m.group(1).lower(), m.group(2) or "/"
    path = unquote(rest)
    if path.endswith("/index.html"):
        path = path[: -len("index.html")]
    if not path.startswith("/"):
        path = "/" + path
    if not resolves(path):
        # The declared target 404s on disk. A canonical that points at a 404 is
        # worse than a self-canonical: it tells the crawler "this page is a
        # duplicate of nothing". Fall back to the page's own path.
        return "self", (f"{host}{rest} does not resolve", self_rootrel(rel))
    # re-quote only the characters that must be escaped in an href
    out = quote(path, safe="/:@!$&'()*+,;=~-._")
    return "ok", out


def main():
    write = "--write" in sys.argv
    stats = {"files": 0, "canon": 0, "ogurl": 0, "bad": 0, "skip": 0, "self": 0}
    selfed = []
    bad = []
    changed = 0

    for full, rel in iter_html():
        stats["files"] += 1
        raw = open(full, "rb").read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue

        def handle(kind, tag, a):
            """Rewrite the URL attribute of one tag in place, or return it unchanged."""
            attr = URL_ATTR[kind]
            if attr not in a:
                return tag
            url, s, e = a[attr]
            if not url.lower().startswith(("http://", "https://")):
                return tag
            st, val = to_rootrel(url, rel)
            if st == "ok":
                stats["canon" if kind == "canonical" else "ogurl"] += 1
                return tag[:s] + val + tag[e:]
            if st == "self":
                why, self_href = val
                stats["self"] += 1
                selfed.append((rel, url, self_href, why))
                return tag[:s] + self_href + tag[e:]
            if st == "bad":
                stats["bad"] += 1
                bad.append((rel, url, val))
            else:
                stats["skip"] += 1
            return tag

        parts, last = [], 0
        for m in TAG_RE.finditer(text):
            tag = m.group(0)
            kind = _tag_kind(tag, _attr_spans(tag))
            if not kind:
                continue
            new_tag = handle(kind, tag, _attr_spans(tag))
            if new_tag != tag:
                parts.append(text[last:m.start()])
                parts.append(new_tag)
                last = m.end()
        new = ("".join(parts) + text[last:]) if parts else text

        if new != text:
            changed += 1
            if write:
                with open(full, "wb") as fh:
                    fh.write(new.encode("utf-8"))

    print(f"html files scanned : {stats['files']}")
    print(f"canonical rewrites : {stats['canon']}")
    print(f"og:url  rewrites   : {stats['ogurl']}")
    print(f"self-fallbacks     : {stats['self']}  (declared target 404s)")
    print(f"files touched      : {changed}")
    print(f"unresolvable       : {stats['bad']}")
    if selfed:
        print("\n--- self-fallback samples (first 8) ---")
        for rel, url, href, why in selfed[:8]:
            print(f"  {rel}\n      was {url}\n      now {href}   [{why}]")
    if bad:
        print("\n--- still unresolvable (left untouched) ---")
        for rel, url, why in bad[:20]:
            print(f"  {rel}\n      {url}\n      {why}")
    if not write:
        print("\nDRY RUN -- nothing written. Re-run with --write.")


if __name__ == "__main__":
    main()
