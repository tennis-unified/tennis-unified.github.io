"""Align an EN monograph PDF with its VI tcq-book reader, paragraph by paragraph.

Two modes, auto-detected:
- NUMBERED: the book uses numbered subsections ("1.1", "2.3"...) in both the
  VI reader (h3) and the EN PDF (ArialBold 10.5). Sections match by number.
- CHAPTER: no numbered subsections; VI reader has h2.ch-title chapters with
  unnumbered h3 runs; EN PDF has bold chapter headings only. Sections match
  by order (counts must be equal).

Within each section: 1:1 pairing when counts are equal, otherwise the EN
text is split into sentences and allocated proportionally over the VI
paragraphs (translation preserves sentence order - verified on books 1/11).

Output JSON: pairs [[vi_p_index, en_text]] (vi_p_index = index over ALL <p>
inside <main id="book-content">, document order), en_heading {num: text},
en_chapter_heads [text per VI ch-title, in order], report.

Usage: python align_en_vi.py <vi_reader.html> <en.pdf> <out.json>
"""
import json, re, sys
import fitz

VI_HTML, EN_PDF, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

NUM = re.compile(r'^(\d+\.\d+)\b')
UP = ('A-ZÀÁẢẠĂẮẰẲẴẶÂẤẦẨẪẬĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊ'
      'ÒÓỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢÙÚỦŨỤƯỨỪỬỮỰỲÝỶỸỴ')
SENT_RE = re.compile(r'(?<=[.!?…])(?=\s+[' + UP + r'"“(])')
def sentences(text):
    return [p.strip() for p in SENT_RE.split(text) if p.strip()]

# ---------- VI side ----------
h = open(VI_HTML, encoding='utf-8').read()
main_m = re.search(r'<main\b[^>]*id="book-content"[^>]*>([\s\S]*?)</main>', h)
if not main_m:
    sys.exit('FATAL: no <main id="book-content"> in ' + VI_HTML)
vi_body = main_m.group(1)
vi_blocks, p_idx = [], 0
for tm in re.finditer(r'<(h2|h3|p)\b([^>]*)>([\s\S]*?)</\1>', vi_body):
    tag, attrs, inner = tm.group(1), tm.group(2), tm.group(3)
    txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', inner)).strip()
    if not txt:
        continue
    if tag == 'p':
        vi_blocks.append([p_idx, tag, txt]); p_idx += 1
    else:
        vi_blocks.append([-1, tag, txt, attrs])

vi_secs, vi_chapters = [], []
for blk in vi_blocks:
    if blk[1] == 'h2':
        if 'toc-title' in blk[3] or 'part-title' in blk[3] or 'toc-heading' in blk[3]:
            continue
        vi_chapters.append({'head': blk[2], 'vi_ps': [], 'en_ps': [],
                            'sub_vi': [], 'sub_en': []})
    elif blk[1] == 'h3':
        if vi_chapters:
            k = NUM.match(blk[2])
            vi_chapters[-1]['sub_vi'].append(k.group(1) if k else None)
    elif blk[1] == 'p' and vi_chapters:
        vi_chapters[-1]['vi_ps'].append(blk)

# ---------- EN side ----------
doc = fitz.open(EN_PDF)
raw = []
for pno, page in enumerate(doc):
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for ln in b['lines']:
            txt = ''.join(s['text'] for s in ln['spans'])
            spans = [s for s in ln['spans'] if s['text'].strip()]
            if not txt.strip() or not spans:
                continue
            raw.append([pno, ln['bbox'][1], ln['bbox'][3], ln['bbox'][0],
                        ln['bbox'][2], max(s['size'] for s in spans),
                        any('Bold' in s['font'] for s in spans), txt.rstrip()])
body_x1 = [r[4] for r in raw if not r[6] and 9.5 <= r[5] <= 10.5]
RIGHT = sorted(body_x1)[int(len(body_x1) * 0.9)] if body_x1 else 1e9

paras, cur = [], None
for pno, y0, y1, x0, x1, sz, bold, txt in raw:
    if sz < 8.5:
        continue
    if bold:
        tag = 'h2' if sz >= 16 else 'h3'
        if cur:
            paras.append(['p'] + cur); cur = None
        if (paras and paras[-1][0] == tag and pno == paras[-1][2]
                and (y0 - paras[-1][3]) <= 19.0):
            paras[-1][1] += ' ' + txt; paras[-1][2], paras[-1][3] = pno, y1
        else:
            paras.append([tag, txt, pno, y1])
        continue
    if cur is None:
        cur = [txt, pno, y1, x1]; continue
    merge = (pno == cur[1] and (y0 - cur[2]) <= 19.0) or \
            (pno == cur[1] + 1 and cur[2] > 540 and cur[3] >= RIGHT - 15)
    if merge:
        cur[0] = txt if cur[0].endswith('-') else cur[0] + ' ' + txt
        cur[1], cur[2], cur[3] = pno, y1, x1
    else:
        paras.append(['p'] + cur); cur = [txt, pno, y1, x1]
if cur:
    paras.append(['p'] + cur)
en_blocks = [[t, re.sub(r'\s+', ' ', x).strip()] for t, x, *_ in paras]

# drop front matter
first_num = next((i for i, (t, x) in enumerate(en_blocks)
                  if t == 'h3' and NUM.match(x)), None)
if first_num is not None:
    en_blocks = en_blocks[first_num:]
else:
    # chapter mode: cut at the last bold heading before the first body para
    first_p = next((i for i, (t, x) in enumerate(en_blocks) if t == 'p'), None)
    if first_p is None:
        sys.exit('FATAL: no body text in EN PDF')
    start = max((i for i in range(first_p) if en_blocks[i][0] in ('h2', 'h3')),
                default=0)
    en_blocks = en_blocks[start:]

en_numbered = [x for t, x in en_blocks if t == 'h3' and NUM.match(x)]
vi_numbered = [s for c in vi_chapters for s in c['sub_vi'] if s]

# ---------- build section list ----------
sections = []  # {key, en_head, vi_ps [(pidx,txt)], en_ps [txt], kind}
en_heads_num, en_chapter_heads = {}, []
if len(en_numbered) >= 3 and len(vi_numbered) >= 3:
    mode = 'numbered'
    cur = None
    for t, x in en_blocks:
        k = NUM.match(x) if t == 'h3' else None
        if k:
            cur = {'key': k.group(1), 'en_head': NUM.sub('', x).strip(),
                   'vi_ps': [], 'en_ps': [], 'kind': 'h3'}
            sections.append(cur); en_heads_num[cur['key']] = cur['en_head']
        elif t == 'p' and cur is not None:
            cur['en_ps'].append(x)
    vi_sec_map = {}
    cur_key = None
    for blk in vi_blocks:
        if blk[1] == 'h3' and NUM.match(blk[2]):
            cur_key = NUM.match(blk[2]).group(1)
            vi_sec_map[cur_key] = []
        elif blk[1] == 'p' and cur_key:
            vi_sec_map[cur_key].append((blk[0], blk[2]))
    for s in sections:
        s['vi_ps'] = vi_sec_map.get(s['key'], [])
else:
    mode = 'chapter'
    # Flat heading streams on both sides. VI stream = all h2/h3 (except
    # toc-title) each with its following paragraphs; EN stream = all bold
    # headings after the TOC's 'Contents' head, each with its paragraphs.
    # If counts drift, fall back to chapter-anchored alignment: match
    # Chương/Chapter N, Phần/Part, Phụ lục/Appendix, Lời kết/Conclusion,
    # Mở đầu/Introduction anchors, then per-chapter h3 matching with a
    # chapter-level pairing fallback for drifted chapters.
    def norm(s):
        return re.sub(r'\s+', ' ', s).strip().lower()
    heads_idx = [i for i, (t, x) in enumerate(en_blocks) if t in ('h2', 'h3')]
    toc_i = next((i for i in heads_idx if norm(en_blocks[i][1]) in
                  ('contents', 'muc luc', 'mục lục', 'table of contents')), None)
    if toc_i is not None:
        start = next((i for i in heads_idx if i > toc_i), None)
        if start is None:
            sys.exit('FATAL: no heading after Contents in EN PDF')
        en_blocks = en_blocks[start:]

    def build_streams():
        en_ch_list = []   # [ [head_text, [para...]] ]
        for t, x in en_blocks:
            if t in ('h2', 'h3'):
                en_ch_list.append([x, []])
            elif en_ch_list:
                en_ch_list[-1][1].append(x)
        vi_flat = []      # [ [tag, head_text, attrs, [(pidx, txt)]] ]
        for blk in vi_blocks:
            if blk[1] in ('h2', 'h3'):
                if blk[1] == 'h2' and ('toc-title' in blk[3] or 'toc-heading' in blk[3]):
                    continue
                vi_flat.append([blk[1], blk[2], blk[3], []])
            elif blk[1] == 'p' and vi_flat:
                vi_flat[-1][3].append((blk[0], blk[2]))
        return en_ch_list, vi_flat

    en_ch_list, vi_flat = build_streams()
    if len(en_ch_list) == len(vi_flat):
        for (eh, eps), (vtag, vhead, vattr, vps) in zip(en_ch_list, vi_flat):
            sections.append({'key': None, 'en_head': eh, 'vi_ps': vps,
                             'en_ps': eps, 'kind': vtag})
        en_chapter_heads = [{'tag': vtag, 'text': eh}
                            for (eh, _), (vtag, _, _, _) in zip(en_ch_list, vi_flat)]
    else:
        mode = 'anchored'
        ANCH = [
            (re.compile(r'^(?:chương|chapter)\s+(\d+)', re.I), 'ch'),
            (re.compile(r'^(?:phần|part)\s+([ivx\d]+)', re.I), 'part'),
            (re.compile(r'^phụ lục|^appendix', re.I), 'appendix'),
            (re.compile(r'^lời kết|^conclusion', re.I), 'conclusion'),
            (re.compile(r'^mở đầu|^introduction\b', re.I), 'intro'),
        ]
        def anchor_of(txt):
            for rx, kind in ANCH:
                mm = rx.match(txt)
                if mm:
                    return (kind, mm.group(1).lower() if mm.groups() else '')
            return None
        vi_anchors = [(i, anchor_of(v[1])) for i, v in enumerate(vi_flat)
                      if anchor_of(v[1])]
        en_anchors = [(i, anchor_of(e[0])) for i, e in enumerate(en_ch_list)
                      if anchor_of(e[0])]
        if len(vi_anchors) != len(en_anchors) or \
                [a for _, a in vi_anchors] != [a for _, a in en_anchors]:
            print('FATAL-ANCHOR: anchor mismatch')
            print('VI anchors:', [(i, v[1][:40], a) for (i, v), (_, a) in
                                  zip(enumerate(vi_flat), [a for _, a in vi_anchors]) if False]
                  if False else [(i, vi_flat[i][1][:40], a) for i, a in vi_anchors])
            print('EN anchors:', [(i, en_ch_list[i][0][:40], a) for i, a in en_anchors])
            sys.exit(1)
        # span boundaries in flat-list indexes
        vi_bounds = [i for i, _ in vi_anchors] + [len(vi_flat)]
        en_bounds = [i for i, _ in en_anchors] + [len(en_ch_list)]
        # leading span before the first anchor (content without anchor heads)
        if vi_bounds[0] > 0 or en_bounds[0] > 0:
            lead_v = vi_flat[:vi_bounds[0]]
            lead_e = en_ch_list[:en_bounds[0]]
            all_vps = [p for v in lead_v for p in v[3]]
            all_eps = [p for e in lead_e for p in e[1]]
            for v in lead_v:
                en_chapter_heads.append({'tag': v[0], 'text': None})
            if all_vps and all_eps:
                sections.append({'key': None, 'en_head': '(leading)',
                                 'vi_ps': all_vps, 'en_ps': all_eps,
                                 'kind': 'chapter'})
        for k in range(len(vi_anchors)):
            v_lo, v_hi = vi_bounds[k], vi_bounds[k + 1]
            e_lo, e_hi = en_bounds[k], en_bounds[k + 1]
            v_span = vi_flat[v_lo:v_hi]
            e_span = en_ch_list[e_lo:e_hi]
            v_subs = [v for v in v_span[1:]]
            e_subs = e_span[1:]
            # entry for the anchor head itself
            if len(v_subs) == len(e_subs):
                en_chapter_heads.append({'tag': v_span[0][0], 'text': e_span[0][0]})
                sections.append({'key': None, 'en_head': e_span[0][0],
                                 'vi_ps': v_span[0][3], 'en_ps': e_span[0][1],
                                 'kind': v_span[0][0]})
                for vv, ee in zip(v_subs, e_subs):
                    en_chapter_heads.append({'tag': vv[0], 'text': ee[0]})
                    sections.append({'key': None, 'en_head': ee[0],
                                     'vi_ps': vv[3], 'en_ps': ee[1],
                                     'kind': vv[0]})
            else:
                # drifted chapter: pair all paragraphs at chapter level
                all_vps = [p for v in v_span for p in v[3]]
                all_eps = [p for e in e_span for p in e[1]]
                en_chapter_heads.append({'tag': v_span[0][0], 'text': e_span[0][0]})
                for vv in v_subs:
                    en_chapter_heads.append({'tag': vv[0], 'text': None})
                sections.append({'key': None, 'en_head': e_span[0][0],
                                 'vi_ps': all_vps, 'en_ps': all_eps,
                                 'kind': 'chapter'})

# ---------- pairing ----------
pairs, report = [], {'exact': 0, 'reflow': 0, 'tail': 0, 'empty': []}
def pair_section(s):
    vps, eps = s['vi_ps'], s['en_ps']
    m, n = len(vps), len(eps)
    if m == 0 or n == 0:
        report['empty'].append(s['en_head'][:40]); return
    if m == n:
        for (pidx, _), et in zip(vps, eps):
            pairs.append([pidx, et])
        report['exact'] += 1
        return
    if m > n:
        sents = []
        for et in eps:
            sents.extend(sentences(et))
        S = len(sents)
        vi_sent = [len(sentences(t)) for _, t in vps]
        S_vi = sum(vi_sent)
        if S >= m and S_vi > 0:
            prev, cum = 0, 0
            for i in range(m):
                cum += vi_sent[i]
                tgt = S if i == m - 1 else min(max(round(S * cum / S_vi), prev + 1), S - (m - 1 - i))
                pairs.append([vps[i][0], ' '.join(sents[prev:tgt]).strip()])
                prev = tgt
            report['reflow'] += 1
        else:
            for i in range(m):
                pairs.append([vps[i][0], eps[i] if i < n else ''])
            report['tail'] += 1
    else:
        for i, (pidx, _) in enumerate(vps):
            et = eps[i] if i == m - 1 else eps[i]
            if i == m - 1 and n > m:
                et = ' '.join(eps[i:]).strip()
            pairs.append([pidx, et])
        report['tail'] += 1

for s in sections:
    pair_section(s)

out = {'vi_html': VI_HTML, 'en_pdf': EN_PDF, 'mode': mode, 'p_count': p_idx,
       'en_heading': en_heads_num, 'en_chapter_heads': en_chapter_heads,
       'pairs': pairs, 'report': report}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'mode={mode} | VI <p>={p_idx} pairs={len(pairs)} '
      f'exact={report["exact"]} reflow={report["reflow"]} '
      f'tail={report["tail"]} empty={report["empty"]}')
bad = [p for p in pairs if not p[1]]
print('pairs with empty EN:', len(bad))
long_heads = [v for v in (en_heads_num or {}).values() if len(v) > 120]
long_heads += [x for x in en_chapter_heads if len(x) > 120]
print('suspiciously long headings (>120 chars):', len(long_heads))
