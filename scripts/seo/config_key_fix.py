#!/usr/bin/env python3
"""
config_key_fix.py — repair machine identifiers that a translation pass rewrote.

THE DEFECT
----------
A find-replace translated the English word `path` inside a Material for MkDocs
feature flag, on 62 pages under `vi/tennis-technical-reference/`:

    "features": [..., "navigation.đường", ...]      <- not a feature; silently ignored
    "features": [..., "navigation.path",   ...]     <- real: breadcrumb trail in sidebar

`navigation.path` is what the other 8,963 pages in the tree use, so the correct
value is not a guess — it is the overwhelming majority form. The corrupted token is
inert: Material does not recognise it, so the feature is simply off on those 62
pages and nothing warns.

SCOPE — measured, not assumed
-----------------------------
A scan of every `__config` JSON blob (9,360 pages) found exactly one non-ASCII token
inside a `features` array: `navigation.đường`, 62 pages. The only other non-ASCII in
those blobs is the `translations` sub-object, where Vietnamese text is CORRECT
(e.g. `"search.result.placeholder": "Nhập để bắt đầu tìm kiếm"`). So the fix is
restricted to the `features` array span and cannot touch `translations`.

WHY A SPAN-RESTRICTED STRING REPLACE, NOT A JSON ROUND-TRIP
-----------------------------------------------------------
Re-serialising the blob would reformat every page and produce a 62-file diff that no
one can review. Replacing the token inside the array span changes exactly the bytes
that are wrong. Each write is then validated: the blob must still parse as JSON, the
feature count must be unchanged, and no non-ASCII may remain in the array.

CAVEAT — THIS REPAIRS THE OUTPUT, NOT THE SOURCE
------------------------------------------------
This repo is a static mirror; the generator that emits `__config` is upstream and is
not here. Fixing these 62 files makes the live site correct now, but **a full rebuild
from the corrupted source will reintroduce it**. The source config must be fixed
wherever the site is built.

Idempotent. DRY RUN unless --write.
"""
import argparse
import json
import re
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "_tmp", ".workbuddy-ai"}
CFG_RE = re.compile(r'(<script[^>]*id="__config"[^>]*>)([\s\S]*?)(</script>)', re.I)
FEAT_KEY = re.compile(r'"features"\s*:\s*\[')
BAD = '"navigation.đường"'
GOOD = '"navigation.path"'


def array_span(blob, start):
    """Return (open_idx, close_idx) of the JSON array beginning at/after `start`."""
    i = blob.index("[", start)
    depth, j, in_str, esc = 0, i, False, False
    while j < len(blob):
        c = blob[j]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    return i, j
        j += 1
    raise ValueError("unbalanced features array")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)

    changed, already, skipped = 0, 0, 0
    rows = []

    for p in sorted(root.rglob("*.html")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        if BAD not in text:
            continue
        m = CFG_RE.search(text)
        if not m:
            skipped += 1
            continue
        blob = m.group(2)
        fk = FEAT_KEY.search(blob)
        if not fk:
            skipped += 1
            continue

        lo, hi = array_span(blob, fk.start())
        arr = blob[lo:hi + 1]
        if BAD not in arr:
            already += 1          # token lives outside features; leave it
            continue

        new_arr = arr.replace(BAD, GOOD)
        new_blob = blob[:lo] + new_arr + blob[hi + 1:]

        # ---- validate before accepting ----
        before = json.loads(blob)["features"]
        after = json.loads(new_blob)["features"]
        assert len(before) == len(after), f"feature count changed in {p}"
        assert GOOD.strip('"') in after, f"replacement missing in {p}"
        assert BAD.strip('"') not in after, f"bad token survived in {p}"
        assert all(ord(c) < 128 for c in "".join(after)), f"non-ascii left in {p}"

        changed += 1
        rows.append((str(p), len(before)))
        if args.write:
            new_text = text[:m.start(2)] + new_blob + text[m.end(2):]
            p.write_text(new_text, encoding="utf-8", newline="")

    print(f"pages repaired      : {changed}")
    print(f"token outside array : {already}")
    print(f"no __config/features: {skipped}")
    print(f"write               : {args.write}")
    if not args.write and rows:
        for path, n in rows[:5]:
            print(f"  {path}  ({n} features)")
        if len(rows) > 5:
            print(f"  ... and {len(rows) - 5} more")
    if not args.write:
        print("  (dry-run; rerun with --write to apply)")


if __name__ == "__main__":
    main()
