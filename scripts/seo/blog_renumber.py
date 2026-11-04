"""Renumber the data-analytics article from the colliding 'Bài viết 149'
slot to the free slot 201, restore proper VI diacritics in its title
strings, and add the missing index entry in vi/articles/index.html
(resolves its orphan status). Dry-run default, --apply to write.
"""
import re, sys

APPLY = '--apply' in sys.argv
ART = 'vi/articles/VI-tenniskb-data-analytics-tennis-match-statistics-performance-metrics/index.html'
IDX = 'vi/articles/index.html'

OLD = 'Bài viết 149: Phân Tích Du Lieu Tennis - Thong Ke Tran Dau & Chi So Hieu Suat'
NEW = 'Bài viết 201: Phân Tích Dữ Liệu Tennis - Thống Kê Trận Đấu & Chỉ Số Hiệu Suất'

h = open(ART, encoding='utf-8', errors='replace').read()
n = h.count(OLD)
h2 = h.replace(OLD, NEW)
# also plain 'Bài viết 149' without suffix, if any remain
n2 = h2.count('Bài viết 149')
h2 = h2.replace('Bài viết 149', 'Bài viết 201')
print(f'article: {n} titled occurrences, {n2} bare occurrences')
assert 'Bài viết 149' not in h2
if APPLY and h2 != h:
    open(ART, 'w', encoding='utf-8', newline='\n').write(h2)

idx = open(IDX, encoding='utf-8', errors='replace').read()
slug = 'VI-tenniskb-data-analytics-tennis-match-statistics-performance-metrics'
entry = ('<li>\n<p><span class="twemoji lg middle"><svg xmlns="http://www.w3.org/2000/svg" '
         'viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6m4 '
         '18H6V4h7v5h5v11z"/></svg></span> <strong>201 — ' + NEW + '</strong></p>\n<hr />\n<p></p>\n'
         '<p><a class="md-button md-button--primary" href="/vi/articles/' + slug + '/">'
         '<span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">'
         '<path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11z"/></svg></span> '
         '\u0110\u1ecdc B\u00e0i Vi\u1ebft</a></p>\n</li>')
if slug not in idx:
    i200 = idx.find('200 — Bài viết 200')
    assert i200 != -1, 'slot-200 anchor not found'
    li_end = idx.find('</li>', i200)
    assert li_end != -1
    ins = li_end + len('</li>')
    idx2 = idx[:ins] + '\n' + entry + idx[ins:]
    print('index: entry inserted after slot 200')
else:
    idx2 = idx
    print('index: entry already present')
if APPLY and idx2 != idx:
    open(IDX, 'w', encoding='utf-8', newline='\n').write(idx2)
print('done (apply=%s)' % APPLY)
