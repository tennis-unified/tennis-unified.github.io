"""Convert a VI tcq-book reader into a bilingual (VI/EN) reader in place.

House convention (mirrors vi/books/*_vi.html bilingual readers):
  <div class="bilingual-block stanza">
    <p class="lang-vi">…VI…</p><p class="lang-en">…EN…</p>
  </div>
CSS: .lang-en hidden by default; body.show-en shows EN and hides VI.
A toggle button (#lang-toggle) flips body.show-en (persisted in localStorage).
Numbered h3 headings gain a <span class="en-heading"> with the EN title.

Idempotent: skips work if body.show-en / #lang-toggle already present.
Dry-run by default; pass --apply to write. Byte-guarded, UTF-8 no BOM, LF.

Usage: python make_book_bilingual.py <vi_reader.html> <align.json> [--apply]
"""
import json, re, sys

path = sys.argv[1]
align_path = sys.argv[2]
apply = '--apply' in sys.argv

h = open(path, encoding='utf-8', newline='').read()
orig_len = len(h)
d = json.load(open(align_path, encoding='utf-8'))
pairs = dict((int(a), b) for a, b in d['pairs'])
en_heads = d['en_heading']

if 'bilingual-block stanza' in h:
    print('SKIP: already bilingual'); sys.exit(0)
# pre-wired template (has toggle + CSS but no stanzas): content-only inject
content_only = 'lang-toggle' in h and 'show-en' in h

main_m = re.search(r'<main\b[^>]*id="book-content"[^>]*>([\s\S]*?)</main>', h)
main = main_m.group(1)

NUM = re.compile(r'^(\d+\.\d+)\b')
en_chapter_heads = d.get('en_chapter_heads') or []

# --- 1. wrap paragraphs into stanzas; enhance headings ---
new_main, p_idx, wrapped, heads_done = [], 0, 0, 0
pos = 0
out_parts = []
head_order = -1  # index over VI h2/h3 (excluding toc-title) for chapter mode
for tm in re.finditer(r'<(h2|h3|p)\b([^>]*)>([\s\S]*?)</\1>', main):
    tag, attrs, inner = tm.group(1), tm.group(2), tm.group(3)
    start, end = tm.span()
    open_m = re.match(r'<' + tag + r'\b[^>]*>', tm.group(0))
    txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', inner)).strip()
    out_parts.append(main[pos:start])
    if tag == 'p':
        if p_idx in pairs and pairs[p_idx]:
            en = pairs[p_idx].replace('&', '&amp;').replace('<', '&lt;')
            out_parts.append(
                '<div class="bilingual-block stanza"><p class="lang-vi">'
                + inner + '</p><p class="lang-en">' + en + '</p></div>')
            wrapped += 1
        else:
            out_parts.append(tm.group(0))
        p_idx += 1
    elif tag in ('h2', 'h3'):
        is_toc = 'toc-title' in attrs or 'toc-heading' in attrs
        en_head = None
        if not is_toc:
            if en_chapter_heads:
                head_order += 1
                if head_order < len(en_chapter_heads):
                    en_head = en_chapter_heads[head_order].get('text')
            else:
                k = NUM.match(txt)
                if k and k.group(1) in en_heads:
                    en_head = en_heads[k.group(1)]
        if en_head:
            en_esc = en_head.replace('&', '&amp;').replace('<', '&lt;')
            close_i = tm.group(0).rfind('</' + tag + '>')
            out_parts.append(tm.group(0)[:close_i]
                             + '<span class="en-heading">' + en_esc + '</span>'
                             + '</' + tag + '>')
            heads_done += 1
        else:
            out_parts.append(tm.group(0))
    else:
        out_parts.append(tm.group(0))
    pos = end
out_parts.append(main[pos:])
new_main = ''.join(out_parts)
h = h[:main_m.start(1)] + new_main + h[main_m.end(1):]

# --- 2. CSS (append into the tcq-book <style> block) ---
CSS = '''
/* bilingual toggle (EN edition) */
.tcq-book .bilingual-block{margin:0 0 1.5em;}
.tcq-book .bilingual-block .lang-vi{margin:0 0 .4em;}
.tcq-book .bilingual-block .lang-en{display:none;margin:0;
  color:var(--tcq-ink-soft);font-size:.82em;line-height:1.7;font-style:italic;
  border-left:2px solid var(--tcq-gold);padding-left:1em;}
body.show-en .tcq-book .bilingual-block .lang-en{display:block;}
body.show-en .tcq-book .bilingual-block .lang-vi{display:none;}
.tcq-book .en-heading{display:none;}
body.show-en .tcq-book .en-heading{display:block;font-size:.6em;
  color:var(--tcq-gold);font-weight:600;letter-spacing:.02em;margin-top:.3em;
  font-family:"Segoe UI",system-ui,sans-serif;}
#lang-toggle{font:inherit;font-size:14px;background:transparent;
  color:var(--tcq-indigo,#1d5c63);border:1px solid var(--tcq-indigo,#1d5c63);
  border-radius:999px;padding:7px 18px;cursor:pointer;letter-spacing:.04em;}
#lang-toggle:hover{background:var(--tcq-indigo,#1d5c63);color:#fff;}
body.show-en #lang-toggle{background:var(--tcq-indigo,#1d5c63);color:#fff;}
'''
style_end = h.find('</style>')
if style_end == -1:
    sys.exit('FATAL: no </style>')
if not content_only:
    h = h[:style_end] + CSS + h[style_end:]

# --- 3. toggle button + script ---
TOGGLE_HTML = ('<button id="lang-toggle" type="button" '
               'aria-pressed="false">EN</button>\n')
anchor = h.find('id="pdf-open"')
if anchor == -1:
    sys.exit('FATAL: no pdf-open anchor for toggle placement')
if not content_only:
    # insert the button before the note-box (start of the note-box div)
    nb = h.find('<div class="note-box">')
    if nb == -1:
        nb = anchor
    h = h[:nb] + TOGGLE_HTML + h[nb:]

SCRIPT = '''<script>
(function(){
  var b=document.getElementById('lang-toggle');
  if(!b) return;
  function paint(){
    var on=document.body.classList.toggle('show-en', localStorage.getItem('book-en')==='1');
    b.setAttribute('aria-pressed', on?'true':'false');
    b.textContent = on ? 'VI' : 'EN';
  }
  b.addEventListener('click', function(){
    localStorage.setItem('book-en', document.body.classList.contains('show-en')?'0':'1');
    paint();
  });
  paint();
})();
</script>
'''
if not content_only:
    if re.search(r'</body>\s*$', h):
        h = re.sub(r'</body>\s*$', SCRIPT + '</body>', h)
    else:
        h = h + SCRIPT

if not apply:
    print(f'DRY-RUN: would wrap {wrapped} paragraphs, {heads_done} EN headings, '
          f'{orig_len} -> {len(h)} bytes')
    sys.exit(0)

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(h)
print(f'APPLIED: {wrapped} stanzas, {heads_done} EN headings, {orig_len} -> {len(h)} bytes')
# sanity
chk = open(path, encoding='utf-8').read()
assert chk.count('bilingual-block stanza') == wrapped
assert chk.count('class="lang-en"') == wrapped
assert chk.count('en-heading') >= heads_done
assert 'show-en' in chk
print('sanity OK')
