#!/usr/bin/env python3
"""tnkb retirement — convert each legacy page into a redirect stub (Option A).

The site is static GitHub Pages (no CNAME, no _config.yml), so a native HTTP 301
is impossible. The repo's established consolidation pattern (see articles/index.html)
is a per-page meta-refresh + canonical stub. We replace every legacy tnkb/ HTML page
with such a stub pointing at its path-equivalent root twin, preserving link equity
and avoiding 404s. The heavy 437 KB legacy pages are gone.

Safe gate (tnkb_gate.py) already verified: 0 missing root twins, 0 redirect loops.

Modes:
  (default)  report only — list path -> target and print sample stubs
  --explain  same as default (alias)
  --write    actually write the stubs in place

Idempotent: a file that already contains http-equiv=refresh is skipped.
Scoped: only files under tnkb/ are ever touched.
"""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TNKB = os.path.join(REPO, "tnkb")
REFRESH = '<meta http-equiv="refresh"'


def target_url(rel):
    if rel.endswith("index.html"):
        url = "/" + rel[: -len("index.html")]
    else:
        url = "/" + rel
    return url


def lang_of(rel):
    return "vi" if rel.startswith("vi/") else "en"


def stub(target, lang):
    return (
        "<!doctype html>\n"
        f'<html lang="{lang}">\n'
        "<head>\n"
        '  <meta charset="utf-8">\n'
        f'  <meta http-equiv="refresh" content="0; url={target}">\n'
        f'  <link rel="canonical" href="{target}">\n'
        f"  <title>Redirecting to {target}...</title>\n"
        '  <meta name="robots" content="noindex,follow">\n'
        f"  <script>window.location.replace('{target}' + window.location.search + "
        "window.location.hash);</script>\n"
        "</head>\n"
        "<body>\n"
        f'  <p>Redirecting to <a href="{target}">{target}</a>...</p>\n'
        "</body>\n"
        "</html>\n"
    )


def main():
    write = "--write" in sys.argv
    htmls = []
    for dp, _, fn in os.walk(TNKB):
        for f in fn:
            if f.endswith(".html"):
                htmls.append(
                    os.path.relpath(os.path.join(dp, f), REPO).replace("\\", "/")
                )
    htmls.sort()

    plan = []
    skipped = 0
    for p in htmls:
        assert p.startswith("tnkb/")
        rel = p[len("tnkb/"):]
        tgt = target_url(rel)
        lang = lang_of(rel)
        full = os.path.join(REPO, p)
        if not write:
            plan.append((p, tgt, lang))
            continue
        # idempotency: don't clobber an already-stubbed file
        try:
            cur = open(full, encoding="utf-8", errors="replace").read()
        except Exception:
            cur = ""
        if REFRESH in cur:
            skipped += 1
            continue
        open(full, "w", encoding="utf-8").write(stub(tgt, lang))
        plan.append((p, tgt, lang))

    if write:
        print(f"wrote {len(plan)} stubs; skipped {skipped} already-stubbed")
    else:
        print(f"would convert {len(htmls)} tnkb/ HTML files to redirect stubs"
              f"{' (--write to apply)' if not write else ''}")
        print("\nsample (path -> target [lang]):")
        for p, tgt, lang in plan[:12]:
            print(f"  {p} -> {tgt} [{lang}]")
        print("\nsample full stub (first path):")
        if plan:
            print(stub(plan[0][1], plan[0][2]))


if __name__ == "__main__":
    main()
