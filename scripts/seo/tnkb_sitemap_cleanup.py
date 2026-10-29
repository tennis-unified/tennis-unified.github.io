#!/usr/bin/env python3
"""tnkb retirement — sitemap cleanup (part of Option A).

- Remove every <url> block whose <loc> contains '/tnkb/' from the ROOT sitemap.xml,
  so Google stops crawling the legacy paths. Regenerate sitemap.xml.gz.
- Delete the orphan tnkb/sitemap.xml (+ .gz).
- Regenerate vi/sitemap.xml.gz from vi/sitemap.xml (the memo notes vi/sitemap.xml.gz is
  stale and holds 451 legacy tnkb/vi URLs; vi/sitemap.xml itself is current).

Idempotent: removing a block that is not present is a no-op.
"""
import os
import re
import gzip

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def regzip(xml_path):
    gz_path = xml_path + ".gz"
    with open(xml_path, "rb") as f:
        data = f.read()
    with gzip.open(gz_path, "wb") as g:
        g.write(data)
    return gz_path


def main():
    # 1) root sitemap: drop tnkb url blocks
    sm = os.path.join(REPO, "sitemap.xml")
    txt = open(sm, encoding="utf-8").read()
    parts = re.split(r"(<url>.*?</url>)", txt, flags=re.S)
    out = []
    removed = 0
    for b in parts:
        if re.match(r"<url>.*?</url>", b, re.S) and "/tnkb/" in b:
            removed += 1
            continue
        out.append(b)
    new = "".join(out)
    open(sm, "w", encoding="utf-8").write(new)
    regzip(sm)
    print(f"root sitemap: removed {removed} tnkb <url> blocks; regenerated sitemap.xml.gz")

    # 2) delete orphan tnkb sitemaps
    for rel in ("tnkb/sitemap.xml", "tnkb/sitemap.xml.gz"):
        p = os.path.join(REPO, rel)
        if os.path.exists(p):
            os.remove(p)
            print(f"deleted orphan {rel}")

    # 3) regenerate vi sitemap gz from its xml (drops stale tnkb/vi urls)
    vi_sm = os.path.join(REPO, "vi", "sitemap.xml")
    if os.path.exists(vi_sm):
        regzip(vi_sm)
        print("regenerated vi/sitemap.xml.gz from vi/sitemap.xml (drops stale tnkb/vi urls)")


if __name__ == "__main__":
    main()
