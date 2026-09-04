#!/bin/bash
# Build the site and copy PDFs after (mkdocs cleans anything not in docs/).

set -e
cd "D:/Github Repos/research-intranet"

echo "[1/3] Running mkdocs build..."
.venv/Scripts/mkdocs.exe build 2>&1 | tail -3

echo "[2/3] Copying PDF library..."
mkdir -p site/books
SRC="D:/New Tennis Knowledge/Tennis Books"

copy_pdfs() {
  local dir="$1"
  if [ ! -d "$dir" ]; then return; fi
  for f in "$dir"/*.pdf; do
    if [ ! -f "$f" ]; then continue; fi
    size=$(stat -c %s "$f" 2>/dev/null || stat -f %z "$f" 2>/dev/null)
    if [ -n "$size" ] && [ "$size" -lt 130000000 ] && [ "$size" -gt 100000 ]; then
      cp "$f" site/books/
    fi
  done
}

# 1. Main Tennis Books folder
copy_pdfs "$SRC"

# 2. Tennis Books Collection folder
copy_pdfs "$SRC/Tennis Books Collection"

# 3. Tennis Books from Archieve.org folder
copy_pdfs "$SRC/Tennis Books from Archieve.org"

# Dedupe by md5 — keep the first occurrence, then re-create canonical aliases
python -c "
import os, hashlib, shutil
seen = set()
for f in sorted(os.listdir('site/books')):
    if not f.lower().endswith('.pdf'): continue
    p = os.path.join('site/books', f)
    try:
        h = hashlib.md5(open(p,'rb').read()).hexdigest()
    except: continue
    if h in seen:
        os.remove(p)
    else:
        seen.add(h)

# Recreate canonical aliases (so reader pages can reference friendly names)
aliases = {
    'absolute-tennis.pdf': '1. Absolute tennis.pdf',
    'HIIT-Laursen-Buchheit.pdf': 'Science-And-Application-Of-High-Intensity-Interval-Training-Solutions-To-The-Programming-2019-pdf.pdf',
}
for alias, source in aliases.items():
    src = os.path.join('site/books', source)
    dst = os.path.join('site/books', alias)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
"

echo "[3/3] Summary:"
echo "  HTML pages: $(find site -name '*.html' | wc -l)"
echo "  PDF files in site/books: $(find site/books -name '*.pdf' | wc -l)"
echo "  Total site size: $(du -sh site | cut -f1)"
echo "  Books PDF size: $(du -sh site/books | cut -f1)"
