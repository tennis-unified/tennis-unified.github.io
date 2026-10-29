#!/usr/bin/env python3
"""Measure and (optionally) repair the host and escaping of sitemap.xml / robots.txt.

Why this exists
---------------
D1 made every canonical in this tree root-relative so that one tree serves both
hosts that deploy it. `sitemap.xml` cannot follow D1: the sitemap protocol
requires absolute <loc> values. So the sitemap is the one artifact that has to
name a host explicitly -- and it named the wrong one.

Measured on 2026-10-28, before this tool existed:

    sitemap.xml   5,744 <loc>, ALL https://tennis-unified.github.io, 0 tenniskb
    robots.txt    Sitemap: https://tennis-unified.github.io/sitemap.xml

That is a fork leftover: this repo is the primary (all SEO work and the voice
pass landed here, and it is what Pages deploys for tenniskb.github.io), but its
own sitemap advertised the mirror host. A crawler on the primary host was told
"these URLs live somewhere else" while every canonical on those pages said "I am
here". Sitemap and canonical disagreeing about the host is a documented cause of
ignored sitemaps and index churn.

A second defect was found while measuring: 280 <loc> values contain literal
spaces (560 characters), because 280 directories in this tree have spaces in
their names ("Elite Manual", "Choking & Amygdala"). Spaces are not legal in a
URI and are not legal in a sitemap <loc>; they resolve only because servers are
lenient. Percent-encoding them makes the URLs correct without changing a single
path.

What it checks
--------------
1. host        -- how many <loc> name each host; must all be the canonical host
2. unsafe      -- characters that are not legal in a URI path
3. xml         -- the file still parses as a sitemap urlset
4. on-disk     -- a <loc> whose path has no matching file/dir here (a sitemap
                  listing 404s is worse than a sitemap with the wrong host)
5. robots      -- the Sitemap: directive points at the same host

Report mode changes nothing. `--write` applies the host repoint and the
percent-encoding, then re-verifies in the same process. Both edits are
mechanical and fully reversible with git; no path is added, removed or renamed.

Usage
-----
  python scripts/seo/sitemap_host.py                  # report
  python scripts/seo/sitemap_host.py --verify         # report, exit 1 on defect
  python scripts/seo/sitemap_host.py --write          # repair, then verify
  python scripts/seo/sitemap_host.py --host https://example.github.io
"""

import argparse
import gzip
import html
import io
import os
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from urllib.parse import quote, unquote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITEMAP = os.path.join(ROOT, "sitemap.xml")
ROBOTS = os.path.join(ROOT, "robots.txt")
DEFAULT_HOST = "https://tenniskb.github.io"

# RFC 3986 pchar + "/" -- everything else must be percent-encoded in a path.
SAFE = "/:@!$&'()*+,;=-._~"
LOC_RE = re.compile(r"<loc>(.*?)</loc>", re.S)
SITEMAP_DIRECTIVE = re.compile(r"^(\s*Sitemap:\s*)(\S+)(\s*)$", re.I | re.M)
HOST_RE = re.compile(r"^https?://([^/]+)")


def read(path):
    with open(path, "rb") as fh:
        return fh.read().decode("utf-8")


def write(path, text):
    with open(path, "wb") as fh:
        fh.write(text.encode("utf-8"))


def unsafe_chars(url):
    """Characters that are illegal in a URI path. A valid %XX escape is legal."""
    bad = set()
    i = 0
    while i < len(url):
        if re.match(r"%[0-9A-Fa-f]{2}", url[i : i + 3]):
            i += 3
            continue
        c = url[i]
        if not (c.isalnum() or c in SAFE):
            bad.add(c)
        i += 1
    return sorted(bad)


def on_disk(url):
    """Does a <loc> path resolve to a file or a directory index in this tree?"""
    m = re.match(r"^https?://[^/]+(/.*)?$", url)
    path = unquote(m.group(1) or "/") if m else "/"
    path = posixpath.normpath("/" + path.lstrip("/"))
    target = os.path.join(ROOT, path.lstrip("/").replace("/", os.sep))
    if os.path.isfile(target):
        return True
    if os.path.isdir(target):
        return any(
            os.path.isfile(os.path.join(target, i)) for i in ("index.html", "index.htm")
        )
    return False


def gz_in_sync():
    """Is sitemap.xml.gz a gzip of the current sitemap.xml?

    It is a tracked, served artifact. A repair that rewrites sitemap.xml and
    leaves the .gz holding the old host is only half a repair.
    """
    path = SITEMAP + ".gz"
    if not os.path.exists(path):
        return None
    try:
        with gzip.open(path, "rb") as fh:
            return fh.read() == open(SITEMAP, "rb").read()
    except (OSError, EOFError):
        return False


def regen_gz():
    """Rewrite the .gz only when its *content* is stale, so reruns are no-ops."""
    path = SITEMAP + ".gz"
    if not os.path.exists(path):
        return False
    if gz_in_sync():
        return False
    data = open(SITEMAP, "rb").read()
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as fh:
        fh.write(data)
    with open(path, "wb") as fh:
        fh.write(buf.getvalue())
    return True


def measure(host):
    text = read(SITEMAP)
    raw_locs = LOC_RE.findall(text)
    locs = [html.unescape(x).strip() for x in raw_locs]

    hosts = Counter()
    for u in locs:
        m = HOST_RE.match(u)
        hosts[m.group(1) if m else "(relative)"] += 1

    bad_unsafe = [u for u in locs if unsafe_chars(u)]
    missing = [u for u in locs if not on_disk(u)]

    try:
        root = ET.fromstring(text)
        xml_ok = root.tag.endswith("urlset")
        xml_note = "ok (urlset)"
    except ET.ParseError as exc:
        xml_ok, xml_note = False, f"PARSE ERROR: {exc}"

    robots = read(ROBOTS) if os.path.exists(ROBOTS) else ""
    m = SITEMAP_DIRECTIVE.search(robots)
    robots_target = m.group(2) if m else None
    robots_ok = bool(robots_target) and robots_target.startswith(host + "/")

    return {
        "text": text,
        "locs": locs,
        "hosts": hosts,
        "unsafe": bad_unsafe,
        "missing": missing,
        "xml_ok": xml_ok,
        "xml_note": xml_note,
        "robots_target": robots_target,
        "robots_ok": robots_ok,
        "host": host,
    }


def report(r):
    print(f"sitemap.xml <loc> entries          : {len(r['locs']):,}")
    for h, n in r["hosts"].most_common():
        flag = "" if h == HOST_RE.match(r["host"]).group(1) else "   <-- not canonical"
        print(f"    {n:>6}  {h}{flag}")
    print(f"locs with unsafe characters        : {len(r['unsafe'])}")
    print(f"locs whose path is missing on disk : {len(r['missing'])}")
    print(f"sitemap parses as <urlset>         : {r['xml_note']}")
    print(f"robots.txt Sitemap: directive      : {r['robots_target']}")
    print(f"robots.txt agrees with canonical   : {'yes' if r['robots_ok'] else 'NO'}")
    gz = gz_in_sync()
    print(
        "sitemap.xml.gz matches sitemap.xml : "
        + ("absent" if gz is None else "yes" if gz else "NO")
    )

    if r["unsafe"]:
        print("\n-- unsafe (sample)")
        for u in r["unsafe"][:5]:
            print(f"  {u}\n      chars={unsafe_chars(u)}")
    if r["missing"]:
        print("\n-- path missing on disk (sample; NOT repaired by this tool)")
        for u in r["missing"][:10]:
            print(f"  {u}")

    wrong_host = sum(
        n for h, n in r["hosts"].items() if h != HOST_RE.match(r["host"]).group(1)
    )
    defects = (
        wrong_host
        + len(r["unsafe"])
        + (0 if r["xml_ok"] else 1)
        + (0 if r["robots_ok"] else 1)
        + (0 if gz in (None, True) else 1)
    )
    print(f"\nrepair-scope defects (host/escaping/xml/robots): {defects}")
    print(f"content defects (dead <loc>, needs a separate decision): {len(r['missing'])}")
    return defects


def repair(r, host):
    text = r["text"]
    old_hosts = [h for h in r["hosts"] if h != HOST_RE.match(host).group(1)]

    # 1. host, only inside <loc>, so nothing else in the file can be touched.
    def fix_loc(m):
        u = html.unescape(m.group(1)).strip()
        for h in old_hosts:
            u = re.sub(r"^https?://" + re.escape(h) + r"(?=/|$)", host, u)
        # 2. percent-encode anything not legal in a URI path. A bare % that does
        #    not start a valid escape becomes %25 first, so this is idempotent.
        u = re.sub(r"%(?![0-9A-Fa-f]{2})", "%25", u)
        u = quote(u, safe=SAFE + "%")
        # 3. XML-escape exactly once on the way back into the document. & is the
        #    only entity that can appear here, and only because it is legal in a
        #    URI path but not in XML text.
        return "<loc>" + u.replace("&", "&amp;") + "</loc>"

    new_text = LOC_RE.sub(fix_loc, text)

    if new_text != text:
        write(SITEMAP, new_text)

    # 3. robots.txt directive
    robots = read(ROBOTS)
    new_robots = SITEMAP_DIRECTIVE.sub(
        lambda m: m.group(1) + host + "/sitemap.xml" + m.group(3), robots
    )
    if new_robots != robots:
        write(ROBOTS, new_robots)

    return new_text != text, new_robots != robots


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    r = measure(args.host)
    print(f"canonical host                     : {args.host}\n")
    before = report(r)

    if args.write:
        changed_sitemap, changed_robots = repair(r, args.host)
        changed_gz = regen_gz()
        print(
            f"\nrewrote: sitemap={'yes' if changed_sitemap else 'no change'}"
            f"  robots={'yes' if changed_robots else 'no change'}"
            f"  gz={'yes' if changed_gz else 'no change'}"
        )
        print("\n--- re-measured ---")
        after = report(measure(args.host))
        return 1 if after else 0

    return 1 if (args.verify and before) else 0


if __name__ == "__main__":
    sys.exit(main())
