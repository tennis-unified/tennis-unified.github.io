#!/usr/bin/env python3
"""
sections_fix.py — resolve the remaining non-reciprocal `sections` hreflang edges.

DESIGN NOTE (this is the important part)
----------------------------------------
An earlier revision of this script iterated `tennis-video-library/*/index.html`
with a glob and stripped the `vi` alternate from every page that was not a
near-duplicate of its coach-video-library twin. That touched 28 pages where the
measurement had found 10, and it broke 18 *genuine* EN<->VI pairs whose VI side
was then left pointing at a page that no longer pointed back. Net effect:
29 non-reciprocal edges became 36.

So this version does not guess a scope. It imports the checker, recomputes the
exact same edge set the checker reports, and acts only on the pages that appear
as the SOURCE of a one-way edge. The blast radius is therefore equal to the
measurement by construction, and there is a hard cap as a second safety net.

Rules applied per source page:
  * If the page's <link rel="canonical"> is one of its own one-way targets, the
    page is a canonicalised duplicate of that target (e.g. en/index.html, which
    duplicates "/" and carries the same tags). A canonicalised duplicate must not
    emit alternates -> remove ALL of them.
  * Otherwise the page claims a translation that does not claim it back (a false
    many-to-one or a claim on a translation that belongs to a different tree)
    -> remove only those specific alternates, leaving legitimate ones intact.

Idempotent. DRY RUN unless --write.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hreflang_reciprocal as hr  # noqa: E402

CANON_RE = hr.re.compile(r'<link\b(?=[^>]*\srel\s*=\s*["\']?canonical\b)[^>]*>', hr.re.I)
CAP = 40  # sanity bound; the measured baseline is 27 source pages


def edges(pages):
    """Recompute the checker's non-reciprocal edges, verbatim in spirit."""
    by_key = {p["key"]: rel for rel, p in pages.items()}
    out = {}
    for rel, p in pages.items():
        for lang, kind, tgt in p["alts"]:
            if kind != "REL":
                continue
            other = by_key.get(tgt)
            if other is None:
                continue
            if any(k2 == "REL" and t2 == p["key"] for (l2, k2, t2) in pages[other]["alts"]):
                continue
            if hr.classify(rel, tgt) != "sections":
                continue
            out.setdefault(rel, set()).add((lang, tgt))
    return out


def canonical_key(rel, text):
    m = CANON_RE.search(text)
    if not m:
        return None
    href = hr.re.search(r'\shref\s*=\s*"([^"]*)"', m.group(0))
    if not href:
        return None
    kind, key = hr.resolve(hr.os.path.dirname(rel), href.group(1))
    return key if kind == "REL" else None


def strip_tags(text, base, drop):
    """Remove only the alternate tags whose resolved (lang, target) is in `drop`."""
    keep, pos, removed = [], 0, []
    for m in hr.ALT_RE.finditer(text):
        lang = m.group(3).lower()
        kind, tgt = hr.resolve(base, m.group(2))
        if kind == "REL" and (lang, tgt) in drop:
            keep.append(text[pos:m.start()])
            pos = m.end()
            removed.append((lang, m.group(2), tgt))
    keep.append(text[pos:])
    return "".join(keep), removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--explain", action="store_true")
    args = ap.parse_args()

    pages = hr.build()
    bad = edges(pages)
    if len(bad) > CAP:
        sys.exit(f"REFUSING: {len(bad)} source pages exceeds cap {CAP}; scope drifted.")

    total_edges = sum(len(v) for v in bad.values())
    n_dup = n_partial = 0
    removed_edges = 0
    rows = []

    for rel in sorted(bad):
        p = pages[rel]
        text = Path(p["path"]).read_text(encoding="utf-8", errors="ignore")
        base = hr.os.path.dirname(rel)
        canon = canonical_key(rel, text)

        if canon is not None and any(tgt == canon for _l, tgt in bad[rel]):
            # duplicate page -> drop every alternate
            drop = {(m.group(3).lower(), hr.resolve(base, m.group(2))[1])
                    for m in hr.ALT_RE.finditer(text)}
            kind = "dup"
            n_dup += 1
        else:
            drop = set(bad[rel])
            kind = "partial"
            n_partial += 1

        new, removed = strip_tags(text, base, drop)
        removed_edges += len([1 for _l, _h, t in removed if any(t == t2 for _l2, t2 in bad[rel])])
        rows.append((kind, rel, len(bad[rel]), len(removed), canon))
        if new != text and args.write:
            Path(p["path"]).write_text(new, encoding="utf-8", newline="")

    print(f"edges measured      : {total_edges}")
    print(f"source pages        : {len(bad)}  (duplicate={n_dup}, partial={n_partial})")
    print(f"alternates removed  : {removed_edges}  write={args.write}")
    if args.explain:
        for kind, rel, ne, nr, canon in rows:
            print(f"  [{kind:<7}] {rel}  edges={ne} removed={nr} canon={canon}")
    if not args.write:
        print("  (dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
