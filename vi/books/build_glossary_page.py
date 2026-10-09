# -*- coding: utf-8 -*-
"""Generates glossary.html from tennis_glossary_vi.json (self-contained page)."""
import json, io, os

here = os.path.dirname(os.path.abspath(__file__))
data = json.load(io.open(os.path.join(here, "tennis_glossary_vi.json"), encoding="utf-8"))
CATS = data["categories"]
TERMS = data["terms"]
N = len(TERMS)

cats_json = json.dumps(CATS, ensure_ascii=False)
terms_json = json.dumps(TERMS, ensure_ascii=False, separators=(",", ":"))

PAGE = u"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Từ Điển Thuật Ngữ Quần Vợt Hiện Đại — %(N)d Thuật Ngữ | Tennis Unified</title>
<meta name="description" content="Từ điển thuật ngữ và khái niệm quần vợt hiện đại, chuẩn hóa tiếng Việt: %(N)d thuật ngữ thuộc %(NC)d chủ đề — sinh cơ học, kỹ thuật cú đánh, chiến thuật, đánh đôi, tâm lý, thể lực, dụng cụ, luật, chấn thương, mặt sân và phân tích dữ liệu. Tổng hợp từ toàn bộ 97 đầu sách của thư viện Tennis Unified.">
<meta name="keywords" content="từ điển quần vợt, thuật ngữ tennis, glossary tennis, thuật ngữ quần vợt tiếng Việt, forehand, backhand, topspin, kick serve, kinetic chain, đánh đôi, chiến thuật tennis">
<meta name="author" content="Tennis Unified">
<meta name="robots" content="index, follow">
<link rel="icon" href="/assets/images/favicon.png">
<meta property="og:type" content="website">
<meta property="og:title" content="Từ Điển Thuật Ngữ Quần Vợt Hiện Đại — Tennis Unified">
<meta property="og:description" content="%(N)d thuật ngữ và khái niệm quần vợt hiện đại, chuẩn hóa tiếng Việt, tổng hợp từ toàn bộ thư viện sách Tennis Unified.">
<meta property="og:locale" content="vi_VN">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,300..800;1,7..72,300..800&family=Montserrat:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/stylesheets/cerulean.min.css">
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/javascripts/lang-toggle.js" defer></script>
<script src="/assets/javascripts/darkmode.js" defer></script>
<style>
  /* Palette aliases -> the shared site tokens defined in /assets/css/site.css.
     The glossary used to ship its own court/chalk/mustard look; pointing the
     old names at the site tokens makes it follow the site theme (and the
     site's dark mode) instead of standing apart. */
  :root{
    --court-ink: var(--ink);
    --court-ink-soft: var(--ink-muted);
    --chalk: var(--bg);
    --chalk-dim: var(--border);
    --line-white: var(--card);
    --mustard: var(--accent);
    --mustard-soft: var(--accent-dark);
    --hairline: var(--border);
    --hairline-soft: var(--border);
    --card-bg: var(--card);
    --page-bg: var(--bg);
    --text-main: var(--ink);
    --text-dim: var(--muted);
    --serif: 'Literata', Georgia, 'Times New Roman', serif;
    --grotesk: 'Montserrat', -apple-system, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    --mono: 'Roboto Mono', 'SFMono-Regular', Consolas, monospace;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  html{scroll-behavior:smooth;}
  body{
    background: var(--page-bg);
    color: var(--text-main);
    font-family: var(--grotesk);
    line-height:1.5;
    transition: background .25s ease, color .25s ease;
  }
  a{color:inherit;}

  .toolbar{
    max-width:1120px; margin:0 auto; padding:20px 24px 0;
  }
  .glossary-hero{
    max-width:1120px; margin:0 auto; padding:28px 24px 0;
  }
  .glossary-hero h1{
    font-family: var(--grotesk); font-size:1.9rem; font-weight:700;
    margin:0 0 6px; color:var(--text-main); line-height:1.2;
  }
  .glossary-hero p{
    margin:0; color:var(--text-dim); font-size:.95rem;
  }
  .search-row{
    display:flex; gap:10px; flex-wrap:wrap; align-items:center;
  }
  #search{
    flex:1 1 260px;
    font-family: var(--serif);
    font-size:1.15rem;
    padding:12px 16px;
    border:1px solid var(--hairline);
    border-radius:10px;
    background: var(--card-bg);
    color: var(--text-main);
  }
  #search:focus{ outline:2px solid var(--mustard); outline-offset:1px; }
  .count-pill{
    font-family: var(--mono); font-size:.78rem; color:var(--text-dim);
    white-space:nowrap;
  }
  .chips{
    display:flex; gap:8px; flex-wrap:wrap; margin:14px 0 4px;
  }
  .chip{
    font-size:.82rem; padding:6px 12px; border-radius:999px;
    border:1px solid var(--hairline); background:transparent; color:var(--text-main);
    cursor:pointer; font-family: var(--grotesk);
    display:inline-flex; align-items:center; gap:6px;
  }
  .chip .chip-n{
    font-family: var(--mono); font-size:.68rem; opacity:.6;
  }
  .chip[aria-pressed="true"]{
    background: var(--mustard); border-color: var(--mustard); color: var(--court-ink);
    font-weight:600;
  }
  .chip[aria-pressed="true"] .chip-n{ opacity:.75; }

  .az-bar{
    display:flex; gap:2px; flex-wrap:wrap; align-items:center;
    margin:10px 0 0; padding:10px 0 0; border-top:1px solid var(--hairline-soft);
  }
  .az-bar span.az-label{
    font-family: var(--mono); font-size:.72rem; color:var(--text-dim);
    margin-right:8px; letter-spacing:.5px;
  }
  .az{
    font-family: var(--mono); font-size:.78rem; width:24px; height:24px;
    display:inline-flex; align-items:center; justify-content:center;
    border-radius:6px; border:1px solid transparent; background:transparent;
    color:var(--text-main); cursor:pointer; padding:0;
  }
  .az:hover{ border-color:var(--hairline); }
  .az[disabled]{ opacity:.25; cursor:default; }
  .az.on{ background:var(--mustard); color:var(--court-ink); font-weight:700; }

  main{ max-width:1120px; margin:0 auto; padding:20px 24px 80px; }
  .category-block{ margin-top:34px; }
  .category-title{
    font-family: var(--serif); font-size:1.05rem; font-weight:600;
    padding-bottom:6px; border-bottom:1px solid var(--hairline);
    color: var(--court-ink-soft);
    display:flex; align-items:baseline; justify-content:space-between; gap:12px;
  }
  .category-title .cat-n{
    font-family: var(--mono); font-size:.72rem; font-weight:400; color:var(--text-dim);
  }
  [data-theme="dark"] .category-title{ color: var(--court-ink); }

  .term-card{
    padding:16px 0; border-bottom:1px solid var(--hairline-soft);
    scroll-margin-top:120px;
  }
  .term-card:target{ background: rgba(201,138,44,0.10); }
  .term-head{
    display:flex; align-items:baseline; gap:10px; flex-wrap:wrap;
  }
  .term-vi{
    font-family: var(--serif); font-size:1.18rem; font-weight:600;
  }
  .term-en{
    font-family: var(--mono); font-size:.78rem; color: var(--text-dim);
  }
  .term-note{ font-size:.94rem; color: var(--text-dim); max-width:70ch; }
  .term-variants{
    font-size:.82rem; color: var(--text-dim);
  }
  .term-variants em{ font-style:normal; color: var(--text-main); border-bottom:1px dotted var(--hairline); }
  .term-sources{
    font-size:.8rem; color: var(--text-dim); display:flex; gap:8px; flex-wrap:wrap; align-items:baseline;
  }
  .term-sources .src-label{ font-family: var(--mono); font-size:.7rem; letter-spacing:.4px; opacity:.8; }
  .term-sources a{
    color: var(--court-ink-soft); text-decoration:none;
    border-bottom:1px dotted var(--hairline); padding-bottom:1px;
  }
  [data-theme="dark"] .term-sources a{ color: var(--court-ink-soft); }
  .term-sources a:hover{ border-bottom-color: var(--mustard); color: var(--mustard); }
  .anchor{
    font-family: var(--mono); font-size:.7rem; color:var(--text-dim);
    text-decoration:none; opacity:0; transition:opacity .15s ease;
  }
  .term-card:hover .anchor{ opacity:.6; }

  .empty-state{
    padding:60px 0; text-align:center; color:var(--text-dim); font-family: var(--serif); font-size:1.1rem;
  }

  .hub-note{
    margin-top:44px; padding:18px 20px; border:1px solid var(--hairline);
    border-radius:12px; background:var(--card-bg);
    font-size:.9rem; color:var(--text-dim);
  }
  .hub-note strong{ color:var(--text-main); }

  .top-link{
    position:fixed; right:20px; bottom:20px; z-index:30;
    width:42px; height:42px; border-radius:50%%;
    border:1px solid var(--hairline); background:var(--card-bg); color:var(--text-main);
    font-size:1rem; cursor:pointer; display:none; align-items:center; justify-content:center;
    box-shadow:0 2px 10px rgba(0,0,0,.12);
  }
  .top-link.show{ display:inline-flex; }

  @media (max-width:600px){
    .toolbar, main{ padding-left:16px; padding-right:16px; }
    .term-vi{ font-size:1.08rem; }
  }
  @media print{
    .toolbar, .top-link, .anchor, .term-sources{ display:none !important; }
    body{ background:#fff; color:#000; }
    .term-card{ break-inside:avoid; border-bottom:1px solid #ddd; }
    .category-title{ border-bottom:2px solid #000; }
  }
</style>
<script type="application/ld+json">
%(ld)s
</script>
</head>
<body data-theme="light">

<!-- FLATTENED-TOP-NAV-START -->
<header class="mm-top"><a class="mm-brand" href="/vi/">Tennis Unified</a><nav class="mm-nav" aria-label="Sections"><div class="mm-dropdown"><button class="mm-dropbtn" type="button" aria-haspopup="true" aria-expanded="false">Main <span class="mm-caret">&#9662;</span></button><div class="mm-dropmenu">
        <a href="/vi/">Trang chủ</a>
        <a href="/vi/fundamentals/">Nền tảng</a>
        <a href="/vi/doubles/">Đánh đôi</a>
        <a href="/vi/stroke-analysis/">Phân tích cú đánh</a>
        <a href="/vi/coach-video-library/">Thư viện HLV</a>
        <a href="/vi/tennis-video-library/">Thư viện Video</a>
        <a href="/vi/tennis-technical-reference/">Tra cứu kỹ thuật</a>
        <a href="/tnkb/vi/">Kho tri thức</a>
        <a href="/vi/tennis-evolution/">Tiến hóa quần vợt</a>
        <a href="/vi/blog/">Bài viết</a>
        <a href="/vi/book/">Sách Toàn diện</a>
        <a href="/vi/books/">Tủ sách Tennis</a>
        <a href="/vi/books/glossary.html" class="active">Từ điển thuật ngữ</a>
        <a href="/vi/books/court_diagrams.html">Sơ đồ chiến thuật</a>
        <a href="/vi/articles/">200 Bài Viết</a>
        <a href="/vi/Tenniskb-5 Pillars/">5 Trụ Cột</a>
        <a href="/vi/Tenniskb-10 Pillars/">10 Trụ Cột</a>
      </div></div></nav><div class="mm-right"><a class="tu-nav-lang mm-langbtn" href="/books/glossary.html" title="Switch language">&#127760; EN</a><button class="tu-nav-darkmode mm-darkbtn" type="button" aria-pressed="false" title="Dark Mode"><span class="tu-nav-emoji">&#127769;</span><span class="tu-nav-text">Dark Mode</span></button></div></header>
<!-- FLATTENED-TOP-NAV-END -->

<nav class="tu-breadcrumb" aria-label="Breadcrumb">
  <ol class="tu-breadcrumb__list">
    <li class="tu-breadcrumb__item"><a class="tu-breadcrumb__link" href="/vi/">Trang Chủ</a></li>
    <li class="tu-breadcrumb__sep">&rsaquo;</li>
    <li class="tu-breadcrumb__item"><a class="tu-breadcrumb__link" href="/vi/books/">Tủ sách Tennis</a></li>
    <li class="tu-breadcrumb__sep">&rsaquo;</li>
    <li class="tu-breadcrumb__item tu-breadcrumb__current" aria-current="page">Từ điển thuật ngữ</li>
  </ol>
</nav>

  <header class="glossary-hero">
    <h1>Từ Điển Thuật Ngữ Quần Vợt</h1>
    <p>Nguồn thuật ngữ chuẩn hóa &middot; %(N)d thuật ngữ &middot; %(NC)d chủ đề</p>
  </header>

  <div class="toolbar">
    <div class="search-row">
      <input id="search" type="text" placeholder="Tìm theo tiếng Việt hoặc tiếng Anh — ví dụ: “xoay trong khớp vai”, “kick serve”, “kinetic chain”…" autocomplete="off" aria-label="Tìm thuật ngữ">
      <span class="count-pill" id="countPill"></span>
    </div>
    <div class="chips" id="categoryChips" role="group" aria-label="Lọc theo chủ đề"></div>
    <div class="az-bar" id="azBar" role="group" aria-label="Lọc theo chữ cái đầu"></div>
  </div>

  <main id="results" aria-live="polite"></main>

  <button class="top-link" id="topLink" type="button" title="Lên đầu trang">↑</button>

  <script>
    const CATEGORY_LABELS = %(cats)s;
    const ALL_TERMS = %(terms)s;

    let activeCategory = 'all';
    let activeLetter = null;
    let activeTag = null;

    const resultsEl = document.getElementById('results');
    const searchEl = document.getElementById('search');
    const chipsEl = document.getElementById('categoryChips');
    const azEl = document.getElementById('azBar');
    const countEl = document.getElementById('countPill');
    const topLink = document.getElementById('topLink');

    function norm(s){
      return (s || '').toString().toLowerCase().normalize('NFD')
        .replace(/[\\u0300-\\u036f]/g, '')
        .replace(/\\u0111/g, 'd');
    }
    function esc(s){
      return (s || '').toString().replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }
    function initial(t){
      const n = norm(t.term_vi_standard).replace(/[^a-z0-9]/g, '');
      return n ? n[0].toUpperCase() : '#';
    }

    if (location.hash) {
      const h = decodeURIComponent(location.hash.slice(1));
      if (h.indexOf('tag=') === 0) activeTag = h.slice(4);
    }

    function counts(){
      const c = {};
      ALL_TERMS.forEach(t => { c[t.category] = (c[t.category] || 0) + 1; });
      return c;
    }

    function buildChips(){
      const c = counts();
      const cats = ['all'].concat(Object.keys(CATEGORY_LABELS).filter(k => c[k]));
      chipsEl.innerHTML = '';
      cats.forEach(k => {
        const btn = document.createElement('button');
        btn.className = 'chip';
        btn.type = 'button';
        const label = k === 'all' ? 'Tất cả' : CATEGORY_LABELS[k];
        btn.innerHTML = '<span>' + esc(label) + '</span><span class="chip-n">' + (k === 'all' ? ALL_TERMS.length : c[k]) + '</span>';
        btn.setAttribute('aria-pressed', k === activeCategory ? 'true' : 'false');
        btn.addEventListener('click', () => {
          activeCategory = k;
          [...chipsEl.children].forEach(x => x.setAttribute('aria-pressed', 'false'));
          btn.setAttribute('aria-pressed', 'true');
          render();
        });
        chipsEl.appendChild(btn);
      });
    }

    function buildAZ(){
      const used = {};
      ALL_TERMS.forEach(t => { used[initial(t)] = true; });
      const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
      azEl.innerHTML = '<span class="az-label">A–Z</span>';
      letters.forEach(L => {
        const b = document.createElement('button');
        b.className = 'az';
        b.type = 'button';
        b.textContent = L;
        if (!used[L]) b.disabled = true;
        b.addEventListener('click', () => {
          activeLetter = (activeLetter === L) ? null : L;
          [...azEl.querySelectorAll('.az')].forEach(x => x.classList.remove('on'));
          if (activeLetter) b.classList.add('on');
          render();
        });
        azEl.appendChild(b);
      });
    }

    function haystack(t){
      return norm([
        t.term_vi_standard, t.term_en, t.note,
        (t.variants_to_replace || []).join(' '),
        CATEGORY_LABELS[t.category] || ''
      ].join(' '));
    }
    function matches(t, q){
      if (!q) return true;
      const terms = norm(q).split(/\\s+/).filter(Boolean);
      const h = haystack(t);
      return terms.every(w => h.indexOf(w) !== -1);
    }

    function render(){
      const q = searchEl.value.trim();
      const filtered = ALL_TERMS.filter(t =>
        (activeCategory === 'all' || t.category === activeCategory) &&
        (!activeLetter || initial(t) === activeLetter) &&
        (!activeTag || t.category === activeTag) &&
        matches(t, q)
      );

      countEl.textContent = filtered.length + ' / ' + ALL_TERMS.length + ' thuật ngữ';

      if (!filtered.length){
        resultsEl.innerHTML = '<div class="empty-state">Không tìm thấy thuật ngữ phù hợp. Thử một từ khóa khác.</div>';
        return;
      }

      const byCat = {};
      filtered.forEach(t => { (byCat[t.category] = byCat[t.category] || []).push(t); });

      const order = Object.keys(CATEGORY_LABELS).filter(k => byCat[k]);
      resultsEl.innerHTML = order.map(cat => {
        const list = byCat[cat].slice().sort((a, b) =>
          a.term_vi_standard.localeCompare(b.term_vi_standard, 'vi'));
        return '<section class="category-block" id="cat-' + cat + '">' +
          '<h2 class="category-title"><span>' + esc(CATEGORY_LABELS[cat]) + '</span>' +
          '<span class="cat-n">' + list.length + ' thuật ngữ</span></h2>' +
          list.map(t => {
            const srcs = (t.sources || []).length
              ? '<div class="term-sources"><span class="src-label">NGUỒN:</span>' +
                t.sources.map(s => '<a href="' + esc(s.href) + '">' + esc(s.label) + '</a>').join('') +
                '</div>'
              : '';
            const vars = (t.variants_to_replace || []).length
              ? '<div class="term-variants">Thay thế cho: ' +
                t.variants_to_replace.map(v => '<em>' + esc(v) + '</em>').join(', ') + '</div>'
              : '';
            return '<article class="term-card" id="term-' + esc(t.id) + '">' +
              '<div class="term-head">' +
                '<span class="term-vi">' + esc(t.term_vi_standard) + '</span>' +
                '<span class="term-en">' + esc(t.term_en) + '</span>' +
                '<a class="anchor" href="#term-' + esc(t.id) + '">#' + esc(t.id) + '</a>' +
              '</div>' +
              (t.note ? '<div class="term-note">' + esc(t.note) + '</div>' : '') +
              vars + srcs +
            '</article>';
          }).join('') +
        '</section>';
      }).join('');
    }

    searchEl.addEventListener('input', render);

    window.addEventListener('scroll', () => {
      topLink.classList.toggle('show', window.scrollY > 600);
    });
    topLink.addEventListener('click', () => window.scrollTo({top:0, behavior:'smooth'}));

    buildChips();
    buildAZ();
    render();

    if (location.hash) {
      const el = document.getElementById(location.hash.slice(1));
      if (el) setTimeout(() => el.scrollIntoView({behavior:'smooth', block:'center'}), 120);
    }
  </script>
</body>
</html>
"""

# ── JSON-LD structured data ──
ld = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "DefinedTermSet",
            "@id": "https://tenniskb.github.io/vi/books/glossary.html#termset",
            "name": "Từ Điển Thuật Ngữ Quần Vợt Hiện Đại",
            "description": data["description"],
            "inLanguage": "vi",
            "url": "https://tenniskb.github.io/vi/books/glossary.html",
            "hasDefinedTerm": [
                {
                    "@type": "DefinedTerm",
                    "@id": "https://tenniskb.github.io/vi/books/glossary.html#term-" + t["id"],
                    "name": t["term_vi_standard"],
                    "alternateName": t["term_en"],
                    "description": t["note"],
                    "inDefinedTermSet": "https://tenniskb.github.io/vi/books/glossary.html#termset",
                }
                for t in TERMS
            ],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Thư Viện Sách", "item": "https://tenniskb.github.io/vi/books/index.html"},
                {"@type": "ListItem", "position": 2, "name": "Từ Điển Thuật Ngữ", "item": "https://tenniskb.github.io/vi/books/glossary.html"},
            ],
        },
    ],
}

out = PAGE % {
    "N": N,
    "NC": len([k for k in CATS if any(t["category"] == k for t in TERMS)]),
    "cats": cats_json,
    "terms": terms_json,
    "ld": json.dumps(ld, ensure_ascii=False, indent=1),
}

p = os.path.join(here, "glossary.html")
# newline="\r\n" keeps the file CRLF like the rest of the repo; writing with
# "\n" silently converted it to LF and made every line show as changed.
with io.open(p, "w", encoding="utf-8", newline="\r\n") as f:
    f.write(out)
print("wrote glossary.html", os.path.getsize(p), "bytes;", N, "terms")
