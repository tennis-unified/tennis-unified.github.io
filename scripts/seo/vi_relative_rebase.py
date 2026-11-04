#!/usr/bin/env python3
"""
vi_relative_rebase.py — VI pages copied from EN originals carry EN-relative links
(`../../../fundamentals/footwork/<slug>/`) that resolve into the EN tree. A VI page
offering its reader the EN page when the VI twin exists is a translation defect.

For every relative href (quoted AND unquoted/minified) in vi/**/*.html that
resolves OUTSIDE vi/:
  - compute the mirrored VI target (insert `vi/` after the repo root)
  - if that VI target exists on disk -> rewrite the href to it (recomputed
    relative, fragment/query preserved, trailing slash preserved)
  - else keep the EN target (intentional fallback for untranslated content)

Idempotent. --dry-run (default) / --apply.

Usage:
  python scripts/seo/vi_relative_rebase.py --root . [--apply]
"""
import argparse
import os
import re
import urllib.parse

SKIP_DIRS = {".git", "node_modules", "__pycache__", "sources", "_tmp", ".workbuddy-ai"}

QUOTED = re.compile(r'((?:<|\s))href="([^"]+)"')
UNQUOTED = re.compile(r'((?:<|\s))href=([^\s>"\']+)')
EXT_PREFIXES = ("/", "#", "mailto:", "tel:", "javascript:", "data:")


def strip_script_style(text):
    text = re.sub(r"<script\b[^>]*>[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<style\b[^>]*>[\s\S]*?</style>", " ", text, flags=re.I)
    return text


def walk_vi(root):
    vi = os.path.join(root, "vi")
    for dirpath, dirnames, filenames in os.walk(vi):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def rebase_one(href, page_dir, root):
    """Return the rebased href, or None if it should stay as-is."""
    if href.startswith(EXT_PREFIXES) or "://" in href:
        return None
    # split path from fragment/query
    m = re.match(r"([^#?]*)([#?].*)?$", href, re.S)
    path_part, suffix = m.group(1), m.group(2) or ""
    if not path_part:
        return None
    raw = urllib.parse.unquote(path_part)
    resolved = os.path.normpath(os.path.join(page_dir, raw)).replace(os.sep, "/")
    if resolved.startswith("vi/") or resolved.startswith(".."):
        return None  # already inside vi/, or escapes the repo
    was_dir = resolved.endswith("/") or "." not in os.path.basename(resolved)
    en_path = resolved.rstrip("/")
    if not os.path.exists(os.path.join(root, en_path)):
        return None  # EN target itself dead — separate problem, not a rebase
    vi_path = "vi/" + en_path
    if not os.path.exists(os.path.join(root, vi_path)):
        return None  # no VI twin — keep EN (untranslated content)
    new_rel = os.path.relpath(vi_path, page_dir).replace(os.sep, "/")
    if was_dir:
        new_rel += "/"
    if not new_rel.startswith("."):
        new_rel = "./" + new_rel
    # a rebase that lands on the linking page itself turns a language-switch or
    # section link into a self-link — keep the original instead
    if os.path.normpath(os.path.join(page_dir, new_rel)).replace(os.sep, "/").rstrip("/") == \
            os.path.normpath(page_dir).replace(os.sep, "/").rstrip("/"):
        return None
    return new_rel + suffix


def make_sub(page_dir, root, counter):
    def replace(match, quoted):
        anchor, href = match.group(1), match.group(2)
        new = rebase_one(href, page_dir, root)
        if new is None or new == href:
            return match.group(0)
        counter[0] += 1
        return '%shref="%s"' % (anchor, new) if quoted else "%shref=%s" % (anchor, new)

    return replace


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--paths-prefix", default="vi/",
                    help="only process pages under this prefix (default: vi/)")
    args = ap.parse_args()
    root = os.path.abspath(args.root)

    files_changed = 0
    for path in walk_vi(root):
        rel_page = os.path.relpath(path, root).replace(os.sep, "/")
        if not rel_page.replace(os.sep, "/").startswith(args.paths_prefix):
            continue
        with open(path, encoding="utf-8", errors="ignore") as f:
            text = f.read()
        page_dir = os.path.relpath(os.path.dirname(path), root).replace(os.sep, "/")
        counter = [0]
        rep = make_sub(page_dir, root, counter)
        # quoted pass, then unquoted pass (minified corpus uses both forms;
        # UNQUOTED excludes '"', so it never re-processes the quoted pass's output)
        new_text = QUOTED.sub(lambda m: rep(m, True), text)
        new_text = UNQUOTED.sub(lambda m: rep(m, False), new_text)
        if counter[0]:
            files_changed += 1
            print("%s: %d links rebased to /vi/" % (rel_page, counter[0]))
            if args.apply:
                with open(path, "w", encoding="utf-8", newline="") as f:
                    f.write(new_text)

    print("files: %d" % files_changed)
    if not args.apply:
        print("\nDRY RUN — no files written. Re-run with --apply.")


if __name__ == "__main__":
    main()
