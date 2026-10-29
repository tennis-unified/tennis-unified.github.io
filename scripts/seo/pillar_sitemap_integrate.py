#!/usr/bin/env python3
"""
pillar_sitemap_integrate.py — add the generated Pillars article URLs to the
sitemaps so Google discovers them. EN pages -> root sitemap.xml; VI pages ->
vi/sitemap.xml. Idempotent: skips any <loc> already present. Regenerates the
.gz counterparts.

Run AFTER pillar_static_gen.py (which writes _pillar_urls.txt).
"""
import argparse
import gzip
from datetime import date
from pathlib import Path

LASTMOD = date.today().isoformat()


def block(url):
    return (
        "  <url>\n"
        f"    <loc>{url}</loc>\n"
        f"    <lastmod>{LASTMOD}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        "    <priority>0.6</priority>\n"
        "  </url>\n"
    )


def integrate(xml_path, urls):
    xml = Path(xml_path)
    text = xml.read_text(encoding="utf-8")
    existing = set()
    # collect existing locs
    import re
    for m in re.finditer(r"<loc>([^<]+)</loc>", text):
        existing.add(m.group(1))
    new = [u for u in urls if u not in existing]
    if not new:
        return 0
    insertion = "".join(block(u) for u in new)
    # insert before </urlset>
    idx = text.rfind("</urlset>")
    if idx == -1:
        raise SystemExit(f"no </urlset> in {xml_path}")
    text = text[:idx] + insertion + text[idx:]
    xml.write_text(text, encoding="utf-8", newline="")
    return len(new)


def regz(xml_path):
    gz = Path(str(xml_path) + ".gz")
    data = Path(xml_path).read_text(encoding="utf-8").encode("utf-8")
    gz.write_bytes(gzip.compress(data, mtime=0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)
    urls = [u.strip() for u in (root / "_pillar_urls.txt").read_text(encoding="utf-8").splitlines() if u.strip()]
    en = [u for u in urls if "/vi/" not in u]
    vi = [u for u in urls if "/vi/" in u]
    print(f"urls total={len(urls)} en={len(en)} vi={len(vi)}")
    if not args.write:
        print("  (dry-run; rerun with --write to apply)")
        # still show how many are new
        for xml, grp in [("sitemap.xml", en), ("vi/sitemap.xml", vi)]:
            text = Path(root / xml).read_text(encoding="utf-8")
            import re
            existing = set(m.group(1) for m in re.finditer(r"<loc>([^<]+)</loc>", text))
            print(f"  {xml}: {len([u for u in grp if u not in existing])} new")
        return
    n1 = integrate(root / "sitemap.xml", en)
    n2 = integrate(root / "vi/sitemap.xml", vi)
    regz(root / "sitemap.xml")
    regz(root / "vi/sitemap.xml")
    print(f"added: root +{n1}, vi +{n2}; regenerated .gz")


if __name__ == "__main__":
    main()
