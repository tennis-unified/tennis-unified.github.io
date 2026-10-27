# -*- coding: utf-8 -*-
"""
SEO host-policy tooling for the tennis-unified tree (deployed verbatim to both
tenniskb.github.io and tennis-unified.github.io).

Decision D1  : PER-HOST self-canonical. The same tree is mirrored verbatim to
               tenniskb.github.io (upstream) and tennis-unified.github.io (fork),
               so an absolute host baked into the tree is wrong on one of them.
               Canonical + hreflang are therefore emitted ROOT-RELATIVE
               ("/en/articles/<slug>/"), which resolves to whichever host serves
               the page -- i.e. each host canonicalises to itself.
Decision D2  : the /articles/ mirror space is RETIRED. Each page becomes a
               one-line redirect stub (meta-refresh + noindex) to its
               /en/articles/<slug>/ twin and is dropped from the sitemap.
Decision D3  : the 17 extra-title blog copies are canonicalised (non-destructive)

Three commands:

  audit    - read-only. Report canonical / hreflang / sitemap state. Changes nothing.
  apply    - write canonical + hreflang into article bodies and stub pages,
             and rewrite the sitemap to the canonical host.
  verify   - assert the invariants hold. Exit 1 on any failure.

Usage:
  python scripts/seo/seo_fix.py audit  [--root DIR]
  python scripts/seo/seo_fix.py apply  [--root DIR] [--dry-run]
  python scripts/seo/seo_fix.py verify [--root DIR]
"""
import argparse
import os
import re
import sys

CANON_HOST = "https://tennis-unified.github.io"
ALT_HOSTS = ("https://tenniskb.github.io",)

def rewrite_robots(root, dry):
    """Under D1 the only advertised sitemap must be the canonical host's. The
    existing file lists BOTH hosts; the tenniskb line is dropped."""
    rb = os.path.join(root, "robots.txt")
    if not os.path.isfile(rb):
        return 0
    txt = read(rb)
    before = txt
    lines = []
    for ln in txt.splitlines():
        m = re.match(r"\s*Sitemap:\s*(https?://[^/\s]+)", ln)
        if m and m.group(1) != CANON_HOST:
            continue  # drop non-canonical-host sitemap lines
        lines.append(ln)
    txt = "\n".join(lines)
    if not txt.endswith("\n"):
        txt += "\n"
    if txt != before:
        if not dry:
            write(rb, txt)
        return 1
    return 0


ALT_SINGLE_RE = re.compile(
    r'(?P<indent>[ \t]*)<link\s+rel="alternate"\s+href="(?P<h>[^"]*)"\s+hreflang="(?P<l>[^"]*)"\s*/?>',
    re.I,
)

# Pages whose <title> marks them as redirect stubs -> not content, keep out of sitemap.
# NOTE: matched against get_title() output (inner text only, already stripped),
# so the pattern must NOT include the <title> tag itself.
STUB_TITLE_RE = re.compile(
    r"^\s*(Redirecting|Chuy\u1ec3n h\u01b0\u1edbng)\b", re.IGNORECASE
)

# Spaces that hold real, indexable content and get a self-canonical.
# D2: articles/ is retired into redirect stubs, so it is NOT a content space.
# D3 scope note: the blog is deliberately NOT given blanket self-canonicals --
# only the 17 extra-title duplicates are canonicalised to their primary slug
# (see canonicalise_blog_variants). Adding a self-canonical to all 722 blog
# pages was never part of the agreed change.
CONTENT_PREFIXES = ("en/articles/", "vi/articles/")
# Pages that get their relative hreflang absolutised without gaining a canonical.
HREFLANG_ONLY_PREFIXES = ("blog/", "vi/blog/")

sys.stdout.reconfigure(encoding="utf-8")


def walk_html(root, scoped=True):
    """Walk HTML. scoped=True visits only the content + stub spaces we care about
    (a full tree walk of 28 886 files over a 5 GB checkout takes many minutes and
    gets killed); scoped=False walks everything."""
    if scoped:
        bases = ("articles", "en/articles", "vi/articles", "blog", "vi/blog",
                 "gemini-notebooks", "vi/gemini-notebooks")
        for b in bases:
            d = os.path.join(root, b)
            if not os.path.isdir(d):
                continue
            for dirpath, dirnames, filenames in os.walk(d):
                for fn in filenames:
                    if fn.endswith(".html"):
                        yield os.path.join(dirpath, fn)
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [
            d for d in dirnames
            if d not in (".git", "node_modules", "__pycache__", ".workbuddy-ai")
        ]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def rel(root, path):
    return os.path.relpath(path, root).replace("\\", "/")


def read(path):
    # byte-transparent: never translate CRLF
    with open(path, "r", encoding="utf-8", errors="surrogateescape",
              newline="") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", errors="surrogateescape",
              newline="") as f:
        f.write(text)


def get_title(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    return m.group(1).strip() if m else ""


def get_canonical(html):
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', html, re.I)
    return m.group(1).strip() if m else None


def get_hreflangs(html):
    out = {}
    for m in re.finditer(
        r'<link\s+rel="alternate"\s+href="([^"]*)"\s+hreflang="([^"]*)"', html, re.I
    ):
        out[m.group(2).strip()] = m.group(1).strip()
    return out


def self_url(page_rel):
    """Canonical URL for a tree-relative page path, emitted ROOT-RELATIVE so it
    resolves to whichever host serves the page (D1 per-host self-canonical).
    A relative canonical is resolved by Google against the document URL, so
    '/en/articles/x/' on tenniskb.github.io -> tenniskb.github.io/en/articles/x/
    and on tennis-unified.github.io -> tennis-unified.github.io/en/articles/x/."""
    p = page_rel
    if p.endswith("/index.html"):
        p = p[: -len("index.html")]
    elif p == "index.html":
        p = ""
    return f"/{p}"


# --------------------------------------------------------------------------- #
# sitemap
# --------------------------------------------------------------------------- #
def sitemap_hosts(xml):
    hosts = {}
    for m in re.finditer(r"<loc>(https://[^/]+)/", xml):
        hosts[m.group(1)] = hosts.get(m.group(1), 0) + 1
    return hosts


def cmd_audit(root):
    print(f"# AUDIT  root={root}")
    n_html = n_can = n_rel_alt = n_xdef = 0
    can_hosts = {}
    title_dupes = {}
    stub_pages = []

    for path in walk_html(root):
        html = read(path)
        n_html += 1
        r = rel(root, path)

        can = get_canonical(html)
        if can:
            n_can += 1
            h = re.match(r"(https?://[^/]+)", can)
            if h:
                can_hosts[h.group(1)] = can_hosts.get(h.group(1), 0) + 1

        alts = get_hreflangs(html)
        if alts:
            if any(not v.startswith("http") for v in alts.values()):
                n_rel_alt += 1
            if "x-default" in alts:
                n_xdef += 1

        if STUB_TITLE_RE.search(get_title(html)):
            stub_pages.append(r)

        t = get_title(html)
        if t and r.startswith("blog/"):
            title_dupes.setdefault(t.lower(), []).append(r)

    sp = os.path.join(root, "sitemap.xml")
    sitemap_info = "missing"
    if os.path.isfile(sp):
        xml = read(sp)
        locs = len(re.findall(r"<loc>", xml))
        hosts = sitemap_hosts(xml)
        malformed = len(re.findall(r"<loc>[^<]*index\.html/</loc>", xml))
        stub_in_sitemap = sum(
            1 for m in re.finditer(r"<loc>([^<]+)</loc>", xml)
            if re.search(r"/(gemini-notebooks|research/authoritative-sources)/", m.group(1))
        )
        sitemap_info = (
            f"{locs} locs; hosts={hosts}; malformed={malformed}; "
            f"stub-paths-listed={stub_in_sitemap}"
        )

    print(f"html files            : {n_html}")
    print(f"  with canonical      : {n_can}")
    print(f"  canonical hosts     : {can_hosts}")
    print(f"  relative hreflang   : {n_rel_alt}")
    print(f"  with x-default      : {n_xdef}")
    print(f"  redirect stubs      : {len(stub_pages)}")
    print(f"sitemap.xml           : {sitemap_info}")

    dupe_groups = {k: v for k, v in title_dupes.items() if len(v) > 1}
    extras = sum(len(v) - 1 for v in dupe_groups.values())
    print(f"blog duplicate titles : {len(dupe_groups)} groups / {extras} extra copies")

    rb = os.path.join(root, "robots.txt")
    if os.path.isfile(rb):
        hosts = set(re.findall(r"Sitemap:\s*(https?://[^/\s]+)", read(rb)))
        print(f"robots.txt sitemaps   : {sorted(hosts)}")
    return 0


# --------------------------------------------------------------------------- #
# apply
# --------------------------------------------------------------------------- #
ALT_BLOCK_RE = re.compile(
    r'(?P<indent>[ \t]*)<link\s+rel="alternate"\s+href="(?P<h1>[^"]*)"\s+hreflang="(?P<l1>[^"]*)">'
    r'(?P<mid>\s*)'
    r'<link\s+rel="alternate"\s+href="(?P<h2>[^"]*)"\s+hreflang="(?P<l2>[^"]*)">',
    re.I,
)
CANONICAL_RE = re.compile(r'(?P<indent>[ \t]*)<link\s+rel="canonical"\s+href="[^"]*">[ \t]*\r?\n?', re.I)


def absorb_html(page_rel, html, add_canonical=True):
    """Return (new_html, changed). Makes canonical absolute+self-referential and
    hreflangs absolute; adds x-default pointing at the EN twin.

    add_canonical=False  -> only absolutise hreflang (used for the blog, where we
    do not want to give 722 pages a blanket self-canonical)."""
    changed = False
    orig = html
    self_u = self_url(page_rel)

    # --- canonical ------------------------------------------------------- #
    can = get_canonical(html)
    if can is None and add_canonical:
        # insert just before the icon/generator lines inside <head>
        anchor = re.search(r'([ \t]*)<link\s+rel="icon"', html)
        if anchor:
            ins = f'{anchor.group(1)}<link rel="canonical" href="{self_u}">\n{anchor.group(1)}'
            html = html[: anchor.start()] + ins + html[anchor.start():]
            changed = True
    elif can is not None and can != self_u and (add_canonical or can.startswith("http")):
        # D1 per-host: rewrite legacy absolute canonicals
        # (https://tennis-unified.github.io/...) -- and any stale relative one --
        # to the ROOT-RELATIVE self URL, so each host canonicalises to itself.
        # On the blog (add_canonical=False) this only fires for a page that
        # already carried an absolute canonical; D3 later re-points variants at
        # their primary slug.
        m = re.search(r'<link\s+rel="canonical"\s+href="[^"]*"', html, re.I)
        if m:
            html = (html[: m.start()]
                    + f'<link rel="canonical" href="{self_u}"'
                    + html[m.end():])
            changed = True

    # --- hreflang -------------------------------------------------------- #
    def absify(href, base_rel):
        """Resolve a possibly-relative href (./, ../, /abs) to a ROOT-RELATIVE
        path (per-host D1). An absolute href is stripped down to its path."""
        if href.startswith("http"):
            m = re.match(r"https?://[^/]+(/.*)?$", href)
            return m.group(1) if (m and m.group(1)) else "/"
        if href.startswith("/"):
            path = href
        else:
            # resolve against the page's directory
            d = os.path.dirname(base_rel)
            path = os.path.normpath(os.path.join(d, href)) if d else os.path.normpath(href)
            path = path.replace(os.sep, "/")
            if path in (".", ""):
                path = "/"
            elif not path.startswith("/"):
                path = "/" + path
            if href.endswith("/") and not path.endswith("/"):
                path += "/"
        return path

    def repl(m):
        nonlocal changed
        ind = m.group("indent")
        # order-agnostic: build a lang->href map, then re-emit canonically
        pairs = {m.group("l1"): m.group("h1"), m.group("l2"): m.group("h2")}
        abs_map = {k: absify(v, page_rel) for k, v in pairs.items()}
        if abs_map != pairs:
            changed = True
        # keep en first if present, else source order
        order = [l for l in ("en", "vi") if l in abs_map]
        order += [l for l in abs_map if l not in order]
        block = "\n".join(
            f'{ind}<link rel="alternate" href="{abs_map[l]}" hreflang="{l}">'
            for l in order
        )
        # NOTE: do NOT inject x-default here. The dedicated "pair present but no
        # x-default" block below adds it exactly once when missing; injecting it
        # here made the rewrite non-idempotent (each run stacked another
        # x-default line, because a trailing x-default is not consumed by the
        # 2-line ALT_BLOCK_RE match).
        return block

    html = ALT_BLOCK_RE.sub(repl, html)

    # en/vi pair already present but no x-default -> append one (relative)
    if "x-default" not in get_hreflangs(html):
        alts = get_hreflangs(html)
        if "en" in alts and "vi" in alts:
            m2 = re.search(
                r'(?P<indent>[ \t]*)<link\s+rel="alternate"\s+href="[^"]*"\s+hreflang="(?:en|vi)">',
                html, re.I)
            if m2:
                ins = (f'\n{m2.group("indent")}<link rel="alternate" '
                       f'href="{absify(alts["en"], page_rel)}" hreflang="x-default">')
                html = html[: m2.end()] + ins + html[m2.end():]
                changed = True

    # --- lone hreflang (no en/vi pair) ----------------------------------- #
    # e.g. blog/mantis-* pages carry only hreflang="en" -> "./". Absolutise it;
    # do NOT invent a vi twin or an x-default we cannot verify.
    if not ALT_BLOCK_RE.search(html):
        def repl_single(m):
            nonlocal changed
            h, ind = m.group("h"), m.group("indent")
            h_abs = absify(h, page_rel)
            if h_abs != h:
                changed = True
            return (f'{ind}<link rel="alternate" href="{h_abs}" '
                    f'hreflang="{m.group("l")}">')
        html = ALT_SINGLE_RE.sub(repl_single, html)

    # --- safety: relativise any remaining absolute hreflang (per-host) ---- #
    # Catches a third/fourth alternate line that the pair-block did not own.
    def _rel_h(m):
        nonlocal changed
        h = m.group("h")
        if h.startswith("http"):
            mm = re.match(r"https?://[^/]+(/.*)?$", h)
            nh = mm.group(1) if (mm and mm.group(1)) else "/"
            changed = True
            return (f'{m.group("indent")}<link rel="alternate" '
                    f'href="{nh}" hreflang="{m.group("l")}">')
        return m.group(0)
    html = ALT_SINGLE_RE.sub(_rel_h, html)

    # --- og:url (D1 per-host, the audit's fourth host-bearing field) ------ #
    def _rel_og(m):
        nonlocal changed
        u = m.group("u")
        if u.startswith("http"):
            mm = re.match(r"https?://[^/]+(/.*)?$", u)
            nu = mm.group(1) if (mm and mm.group(1)) else "/"
            changed = True
            return f'<meta property="og:url" content="{nu}"'
        return m.group(0)
    html = re.sub(r'<meta\s+property="og:url"\s+content="(?P<u>[^"]*)"',
                  _rel_og, html, flags=re.I)

    # --- dedupe hreflang lines -------------------------------------------- #
    # The pair-rewrite above emits an x-default for the matched en/vi pair; if
    # the source block already carried an x-default on its own line (which the
    # 2-line ALT_BLOCK_RE does not consume) we would end with two. Keep the
    # first occurrence of each hreflang value.
    out_lines, seen_langs = [], set()
    for ln in html.split("\n"):
        mh = re.match(
            r'^[ \t]*<link\s+rel="alternate"\s+href="[^"]*"\s+hreflang="([^"]*)"\s*/?>[ \t\r]*$',
            ln, re.I)
        if mh:
            lg = mh.group(1)
            if lg in seen_langs:
                changed = True
                continue
            seen_langs.add(lg)
        out_lines.append(ln)
    html = "\n".join(out_lines)
    # Truth source for "changed": an actual before/after comparison. The
    # per-step flags can miss a silent rewrite (e.g. ALT_BLOCK_RE collapsing two
    # identical-lang lines into one when both are already relative).
    return html, (changed or html != orig)


# --------------------------------------------------------------------------- #
# D2 - retire the /articles/ mirror space as one-line redirect stubs
# --------------------------------------------------------------------------- #
ARTICLES_DIR = "articles"


def make_redirect_stub(target):
    """Minimal redirect stub. `target` is ROOT-RELATIVE (/en/articles/<slug>/),
    so the stub redirects correctly on whichever host serves it (per-host)."""
    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        "<title>Redirecting\u2026</title>\n"
        f'<link rel="canonical" href="{target}">\n'
        f'<meta http-equiv="refresh" content="0; url={target}">\n'
        '<meta name="robots" content="noindex">\n'
        "</head>\n"
        "<body>\n"
        f'<p>This page has moved to <a href="{target}">{target}</a>.</p>\n'
        "</body>\n"
        "</html>\n"
    )


def retire_articles_stubs(root, dry):
    """D2: replace each articles/<slug>/index.html with a redirect stub to its
    /en/articles/<slug>/ twin. Only stub pages whose twin actually exists."""
    base = os.path.join(root, ARTICLES_DIR)
    if not os.path.isdir(base):
        return 0, 0
    done = skipped = 0
    for slug in sorted(os.listdir(base)):
        p = os.path.join(base, slug, "index.html")
        if not os.path.isfile(p):
            continue
        target = f"/en/articles/{slug}/"
        twin = os.path.join(root, "en", "articles", slug, "index.html")
        if not os.path.isfile(twin):
            skipped += 1
            continue
        stub = make_redirect_stub(target)
        if read(p) != stub:
            done += 1
            if not dry:
                write(p, stub)

    # The /articles/ landing (articles/index.html) is already a redirect stub;
    # normalise its canonical to the same ROOT-RELATIVE target (per-host).
    lp = os.path.join(base, "index.html")
    if os.path.isfile(lp):
        lhtml = read(lp)
        m = re.search(r'http-equiv="refresh"\s+content="0;\s*url=([^"]+)"', lhtml)
        if m:
            tgt = m.group(1).strip()
            m2 = re.search(r'<link\s+rel="canonical"\s+href="[^"]*"', lhtml)
            if m2 and m2.group(0) != f'<link rel="canonical" href="{tgt}"':
                nl = lhtml[: m2.start()] + f'<link rel="canonical" href="{tgt}"' + lhtml[m2.end():]
                done += 1
                if not dry:
                    write(lp, nl)
    return done, skipped


def rewrite_sitemap(root, dry):
    sp = os.path.join(root, "sitemap.xml")
    if not os.path.isfile(sp):
        return 0, 0
    xml = read(sp)
    before = xml

    # 1. canonical host
    for h in ALT_HOSTS:
        xml = xml.replace(f"<loc>{h}/", f"<loc>{CANON_HOST}/")

    # 2. drop the malformed  .../index.html/  entry (with its <url> wrapper)
    xml = re.sub(
        r"[ \t]*<url>\s*<loc>[^<]*index\.html/</loc>[\s\S]*?</url>\s*\n?", "", xml
    )

    # 3. drop redirect-stub URLs from the sitemap
    xml = re.sub(
        r"[ \t]*<url>\s*<loc>[^<]*/(?:gemini-notebooks|research/authoritative-sources)/[^<]*</loc>[\s\S]*?</url>\s*\n?",
        "", xml,
    )

    # 3b. D2: drop the retired bare /articles/ space (now redirect stubs).
    #     Match host + "/articles/" only -- never /en/articles/ or /vi/articles/.
    xml = re.sub(
        r"[ \t]*<url>\s*<loc>https?://[^/<]+/articles/[^<]*</loc>[\s\S]*?</url>\s*\n?",
        "", xml,
    )

    # 4. XML-escape the loc TEXT (raw '&' in 40 URLs made the file invalid for
    #    every strict parser, including Google's). Escape the common entities
    #    only if not already escaped.
    def esc(m):
        u = m.group(1)
        u = u.replace("&", "&amp;")
        u = u.replace("<", "&lt;").replace(">", "&gt;")
        # undo double-escaping of entities we may have just created
        for e in ("&amp;amp;", "&amp;lt;", "&amp;gt;", "&amp;quot;", "&amp;apos;"):
            u = u.replace(e, e.replace("&amp;", "&"))
        return f"<loc>{u}</loc>"

    xml = re.sub(r"<loc>([^<]*)</loc>", esc, xml)

    removed = before.count("<loc>") - xml.count("<loc>")
    if not dry and xml != before:
        write(sp, xml)
    return (1 if xml != before else 0), removed


# --------------------------------------------------------------------------- #
# D3 - canonicalise the extra-title blog duplicates to their primary slug
#
# Discriminator: an explicit trailing -N on the slug is the duplicate marker,
# and a base slug (same name without -N) must exist. Measured on this tree:
#   * true duplicates (Toni Nadal, Lewitology, Bruguera, Spanish-method) all
#     carry a -2/-3/-4 suffix AND have a -N-less base sibling;
#   * the one title collision WITHOUT a suffix
#     (mantis-7-essential-tips... vs mantis-best-tennis-balls-for-grass-courts)
#     is two DIFFERENT articles sharing a wrong <title>. Body similarity cannot
#     separate them (0.998, higher than the real duplicates), so a similarity
#     test is actively misleading here -- the slug-suffix rule is the signal.
# --------------------------------------------------------------------------- #
def _base_slug(rel_path):
    """'blog/foo-2/index.html' -> 'blog/foo/index.html' (None if no -N suffix)."""
    m = re.match(r"^(.*?)-(\d+)/index\.html$", rel_path)
    return f"{m.group(1)}/index.html" if m else None


def find_blog_variants(root):
    """Return (pairs, skipped). A pair is emitted only when the variant slug
    ends in -N and the corresponding base slug exists in the tree. Primary =
    the base page. Never infers duplication from a title alone."""
    all_pages = {rel(root, p) for p in walk_html(root)}

    groups = {}
    for path in walk_html(root):
        r = rel(root, path)
        if not (r.startswith("blog/") or r.startswith("vi/blog/")):
            continue
        t = get_title(read(path))
        if t and not STUB_TITLE_RE.search(t):
            groups.setdefault(t.lower(), []).append(r)

    pairs, skipped = set(), []
    for t, files in groups.items():
        if len(files) < 2:
            continue
        emitted = False
        for v in files:
            base = _base_slug(v)
            if base and base in all_pages and base != v:
                pairs.add((v, base))
                emitted = True
        if not emitted:
            skipped.append((t, sorted(files)))
    return sorted(pairs), skipped


def canonicalise_blog_variants(root, dry):
    pairs, skipped = find_blog_variants(root)
    done = 0
    for variant, primary in pairs:
        p = os.path.join(root, variant.replace("/", os.sep))
        if not os.path.isfile(p):
            continue
        html = read(p)
        target = self_url(primary)
        m = re.search(r'<link\s+rel="canonical"\s+href="[^"]*"', html, re.I)
        if m:
            new = html[: m.start()] + f'<link rel="canonical" href="{target}"' + html[m.end():]
        else:
            anchor = re.search(r'([ \t]*)<link\s+rel="icon"', html)
            if not anchor:
                continue
            ins = f'{anchor.group(1)}<link rel="canonical" href="{target}">\n{anchor.group(1)}'
            new = html[: anchor.start()] + ins + html[anchor.start():]
        if new != html:
            done += 1
            if not dry:
                write(p, new)
    return done, pairs, skipped


def cmd_apply(root, dry):
    n_changed = 0
    n_can_added = 0
    n_alt_abs = 0

    # pass 0 (D2): retire /articles/ into one-line redirect stubs
    n_stub, n_stub_skip = retire_articles_stubs(root, dry)

    # pass 1: content spaces -> canonical + root-relative hreflang
    for path in walk_html(root):
        r = rel(root, path)
        if not r.startswith(CONTENT_PREFIXES):
            continue
        html = read(path)
        if STUB_TITLE_RE.search(get_title(html)):
            continue
        had_can = get_canonical(html) is not None
        new, changed = absorb_html(r, html, add_canonical=True)
        if changed:
            n_changed += 1
            if not had_can and get_canonical(new):
                n_can_added += 1
            if any(v.startswith("http") for v in get_hreflangs(new).values()):
                n_alt_abs += 1
            if not dry:
                write(path, new)

    # pass 2: blog -> absolutise hreflang only, no blanket canonical
    n_blog_alt = 0
    for path in walk_html(root):
        r = rel(root, path)
        if not r.startswith(HREFLANG_ONLY_PREFIXES):
            continue
        html = read(path)
        if not get_hreflangs(html):
            continue
        new, changed = absorb_html(r, html, add_canonical=False)
        if changed:
            n_blog_alt += 1
            if not dry:
                write(path, new)

    # pass 3 (D3): canonicalise extra-title blog duplicates
    n_var, pairs, skipped = canonicalise_blog_variants(root, dry)

    # pass 4: any remaining absolute canonical on OUR OWN host -> root-relative
    # (catches gemini-notebooks stubs etc. that are outside the managed spaces).
    n_canon_rel = 0
    for path in walk_html(root):
        html = read(path)
        can = get_canonical(html)
        if can and can.startswith("http"):
            host = re.match(r"(https?://[^/]+)", can).group(1)
            if host == CANON_HOST or host in ALT_HOSTS:
                m = re.search(r'<link\s+rel="canonical"\s+href="[^"]*"', html, re.I)
                if m:
                    pth = re.sub(r"^https?://[^/]+", "", can) or "/"
                    new = (html[: m.start()]
                           + f'<link rel="canonical" href="{pth}"'
                           + html[m.end():])
                    n_canon_rel += 1
                    if not dry:
                        write(path, new)

    sm_changed, removed = rewrite_sitemap(root, dry)
    rb_changed = rewrite_robots(root, dry)
    tag = "DRY-RUN" if dry else "APPLIED"
    print(f"[{tag}] articles-stubbed={n_stub} stub-skipped={n_stub_skip} "
          f"content-pages-changed={n_changed} canonical-added={n_can_added} "
          f"canonical-relativised={n_canon_rel} "
          f"hreflang-relative={n_alt_abs} blog-hreflang-rel={n_blog_alt} "
          f"blog-variants-canonicalised={n_var} sitemap-changed={sm_changed} "
          f"sitemap-locs-removed={removed} robots-changed={rb_changed}")
    if skipped:
        print(f"  ! {len(skipped)} ambiguous title group(s) SKIPPED (no safe primary):")
        for t, files in skipped[:10]:
            print(f"      {t[:70]}  ({len(files)} pages)")
    if dry:
        for v, p in pairs:
            print(f"      var: {v}  ->  {p}")
    return 0


# --------------------------------------------------------------------------- #
# verify
# --------------------------------------------------------------------------- #
def cmd_verify(root):
    fails = []

    for path in walk_html(root):
        r = rel(root, path)
        html = read(path)
        is_stub = bool(STUB_TITLE_RE.search(get_title(html)))
        managed = (r.startswith(CONTENT_PREFIXES)
                   or r.startswith(HREFLANG_ONLY_PREFIXES)
                   or r.startswith(ARTICLES_DIR + "/"))

        can = get_canonical(html)
        # D1: managed canonicals must be ROOT-RELATIVE (per-host self-canonical)
        if can and managed and not can.startswith("/"):
            fails.append(f"non-root-relative canonical: {r} -> {can}")

        # D2: every articles/<slug>/ page must be a redirect stub
        if r.startswith(ARTICLES_DIR + "/") and r.endswith("/index.html"):
            if not is_stub or 'http-equiv="refresh"' not in html:
                fails.append(f"articles/ page is not a redirect stub: {r}")

        alts = get_hreflangs(html)
        if managed:
            for lang, v in alts.items():
                if not v.startswith("/"):
                    fails.append(f"non-root-relative hreflang[{lang}]: {r} -> {v}")
            # duplicate <link rel="alternate"> lines are a defect; count ONLY the
            # head alternate links (body language-switcher <a hreflang> is legit).
            for lg in ("en", "vi", "x-default"):
                n = len(re.findall(
                    rf'<link\s+rel="alternate"[^>]*hreflang="{re.escape(lg)}"',
                    html, re.I))
                if n > 1:
                    fails.append(f"duplicate hreflang[{lg}]: {r}")
            # x-default is required only where a real en/vi pair exists
            if "en" in alts and "vi" in alts and "x-default" not in alts:
                fails.append(f"hreflang without x-default: {r}")

    sp = os.path.join(root, "sitemap.xml")
    if os.path.isfile(sp):
        xml = read(sp)
        for m in re.finditer(r"<loc>([^<]+)</loc>", xml):
            u = m.group(1)
            if not u.startswith(CANON_HOST + "/"):
                fails.append(f"sitemap wrong host: {u}")
            if u.endswith("index.html/"):
                fails.append(f"sitemap malformed: {u}")
            if re.search(r"/(gemini-notebooks|research/authoritative-sources)/", u):
                fails.append(f"sitemap lists stub: {u}")
            if re.match(r"https?://[^/<]+/articles/", u):
                fails.append(f"sitemap lists retired /articles/: {u}")

    rb = os.path.join(root, "robots.txt")
    if os.path.isfile(rb):
        for h in re.findall(r"Sitemap:\s*(https?://[^/\s]+)", read(rb)):
            if h != CANON_HOST:
                fails.append(f"robots.txt sitemap host: {h}")

    if fails:
        print(f"FAIL ({len(fails)}):")
        for f in fails[:40]:
            print("  -", f)
        if len(fails) > 40:
            print(f"  ... +{len(fails) - 40} more")
        return 1
    print("VERIFY OK — 0 failures")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["audit", "apply", "verify"])
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if a.cmd == "audit":
        return cmd_audit(root)
    if a.cmd == "apply":
        return cmd_apply(root, a.dry_run)
    return cmd_verify(root)


if __name__ == "__main__":
    sys.exit(main())
