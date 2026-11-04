"""Install click-nav (prev / next / hub) on handbook pages:
- vi/handbook/*.html (42 numbered chapters): TP-NAV house block with VI labels,
  ordered by directory number; also a hub link back to vi/handbook/.
- en/handbooks/*_chapters/*.html: fill missing prev/next sibling links (EN labels).
Insertion point: immediately before the LAST </body> (rfind — pages may end with
</html>). Idempotent via TP-NAV-START / data-clicknav markers.
Dry-run default, --apply writes.
"""
import re, sys, glob, os

APPLY = '--apply' in sys.argv

def insert_before_body(h, block):
    i = h.rfind('</body>')
    if i == -1:
        return None
    return h[:i] + block + h[i:]

# ---------- vi/handbook ----------
chapters = sorted(
    (f for f in glob.glob('vi/handbook/*/index.html')),
    key=lambda p: p)
# natural sort by leading number in dir name
def ch_key(p):
    m = re.search(r'(\d+)', p)
    return (int(m.group(1)) if m else 9999, p)
chapters = [c for c in chapters if re.search(r'vi/handbook[\\/]\d', c)]
chapters.sort(key=ch_key)
hub = '/vi/handbook/'
added = 0
for i, f in enumerate(chapters):
    h = open(f, encoding='utf-8', errors='replace').read()
    if 'TP-NAV-START' in h:
        continue
    prv = chapters[i - 1] if i > 0 else None
    nxt = chapters[i + 1] if i + 1 < len(chapters) else None
    def rel(other):
        return os.path.basename(os.path.dirname(other)) + '/'
    parts = [f'<a href="{hub}">M\u1ee5c l\u1ee5c</a>']
    if prv:
        parts.append(f'<a href="{rel(prv)}">\u2190 Trang tr\u01b0\u1edbc</a>')
    if nxt:
        parts.append(f'<a href="{rel(nxt)}">Trang sau \u2192</a>')
    block = ('\n<!-- TP-NAV-START -->\n<hr />\n<p style="text-align:center; margin:2rem 0; '
             'font-size:0.95rem;">\n' + ' &nbsp;|&nbsp; '.join(parts) +
             '\n</p>\n<!-- TP-NAV-END -->\n')
    h2 = insert_before_body(h, block)
    if h2:
        added += 1
        if APPLY:
            open(f, 'w', encoding='utf-8', newline='\n').write(h2)
        print(f'vi/handbook: {os.path.basename(os.path.dirname(f))} '
              f'({"prev" if prv else "-"}/{"next" if nxt else "-"})')
print('vi/handbook chapters updated:', added, '/', len(chapters))

# ---------- en/handbooks chapter series ----------
fixed = 0
for d in sorted(glob.glob('en/handbooks/*_chapters')):
    chs = sorted(glob.glob(d + '/*.html'))
    for i, c in enumerate(chs):
        h = open(c, encoding='utf-8', errors='replace').read()
        if 'data-clicknav' in h:
            continue
        prv = chs[i - 1] if i > 0 else None
        nxt = chs[i + 1] if i + 1 < len(chs) else None
        parts = ['<a href="../">Handbook overview</a>']
        if prv:
            parts.append(f'<a href="{os.path.basename(prv)}">&#8592; Previous chapter</a>')
        if nxt:
            parts.append(f'<a href="{os.path.basename(nxt)}">Next chapter &#8594;</a>')
        block = ('\n<!-- click-nav (auto) -->\n<hr />\n<p data-clicknav '
                 'style="text-align:center; margin:2rem 0; font-size:0.95rem;">\n'
                 + ' &nbsp;|&nbsp; '.join(parts) + '\n</p>\n')
        need = (prv and os.path.basename(prv) not in h) or (nxt and os.path.basename(nxt) not in h)
        if not need:
            continue
        h2 = insert_before_body(h, block)
        if h2:
            fixed += 1
            if APPLY:
                open(c, 'w', encoding='utf-8', newline='\n').write(h2)
            print(f'en/handbooks: {os.path.basename(c)[:60]}')
print('en/handbooks chapter files updated:', fixed)
