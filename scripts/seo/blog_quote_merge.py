"""Merge the 3 thin Lewitology quote cards into their series base articles
(EN + VI twins), convert the cards into the house meta-refresh redirect
stubs, drop the card URLs from sitemap.xml, and repoint inbound links.

Cards -> bases:
  blog/prodigymaker-the-lewitology-tennis-wisdom-by-chris-lewit-{2,3}
      -> blog/prodigymaker-the-lewitology-tennis-wisdom-by-chris-lewit/
  blog/prodigymaker-the-lewitology-the-tennis-wisdom-of-chris-lewit-2
      -> blog/prodigymaker-the-lewitology-the-tennis-wisdom-of-chris-lewit/
(and vi/ twins, same slugs). Dry-run by default, --apply to write.
"""
import re, sys

APPLY = '--apply' in sys.argv
SERIES = [
    ('blog/prodigymaker-the-lewitology-tennis-wisdom-by-chris-lewit',
     ['blog/prodigymaker-the-lewitology-tennis-wisdom-by-chris-lewit-2',
      'blog/prodigymaker-the-lewitology-tennis-wisdom-by-chris-lewit-3']),
    ('blog/prodigymaker-the-lewitology-the-tennis-wisdom-of-chris-lewit',
     ['blog/prodigymaker-the-lewitology-the-tennis-wisdom-of-chris-lewit-2']),
]

def read(p):
    return open(p, encoding='utf-8', errors='replace').read()

def quote_ps(html):
    """Extract the quoted <p> blocks (curly quotes) from a card body."""
    out = []
    for m in re.finditer(r'<p[^>]*>(\s*&#8220;[\s\S]*?)</p>', html):
        out.append(m.group(0))
    return out

def insert_quotes(base_html, quotes):
    """Insert quote <p> blocks after the base's first quoted paragraph."""
    if not quotes:
        return base_html, 0
    # first quoted <p> in base
    m = re.search(r'<p[^>]*>\s*&#8220;[\s\S]*?</p>', base_html)
    anchor = m.end() if m else None
    if anchor is None:
        # fallback: after the byline paragraph (first <p> containing 'Chris Lewit, Prodigy Maker')
        m2 = re.search(r'<p[^>]*>[^<]*Chris Lewit, Prodigy Maker[\s\S]*?</p>', base_html)
        anchor = m2.end() if m2 else None
    if anchor is None:
        return base_html, 0
    block = '\n' + '\n'.join(quotes) + '\n'
    return base_html[:anchor] + block + base_html[anchor:], len(quotes)

def make_stub(target_url, title):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url={target_url}">
  <link rel="canonical" href="{target_url}">
  <title>Redirecting to {title}...</title>
  <meta name="robots" content="noindex,follow">
  <script>window.location.replace('{target_url}' + window.location.search + window.location.hash);</script>
</head>
<body>
  <p>Redirecting to <a href="{target_url}">{title}</a>...</p>
</body>
</html>
'''

changed = {'base_quotes': 0, 'stubs': 0, 'sitemap': 0, 'index_links': 0}
for base, cards in SERIES:
    for lang in ('', 'vi/'):
        bpath = lang + base + '/index.html'
        try:
            bh = read(bpath)
        except FileNotFoundError:
            print('MISSING base', bpath); continue
        quotes = []
        for c in cards:
            try:
                ch = read(lang + c + '/index.html')
            except FileNotFoundError:
                print('MISSING card', lang + c); continue
            quotes.extend(quote_ps(ch))
        bh2, n = insert_quotes(bh, quotes)
        if n and bh2 != bh:
            changed['base_quotes'] += n
            if APPLY:
                open(bpath, 'w', encoding='utf-8', newline='\n').write(bh2)
            print(f'base {bpath}: +{n} quotes')
        # convert cards to stubs
        target = '/' + bpath.replace('index.html', '')
        title_m = re.search(r'<title>([^<]*)</title>', bh)
        title = title_m.group(1).split(' - ')[0] if title_m else base
        for c in cards:
            cpath = lang + c + '/index.html'
            try:
                read(cpath)
            except FileNotFoundError:
                continue
            if APPLY:
                open(cpath, 'w', encoding='utf-8', newline='\n').write(
                    make_stub(target, title))
            changed['stubs'] += 1
            print(f'stub {cpath} -> {target}')

sm = read('sitemap.xml')
sm2 = sm
for lang in ('', 'vi/'):
    for _, cards in SERIES:
        for c in cards:
            url = f'https://tenniskb.github.io/{lang}{c}/'
            if url in sm2:
                sm2 = re.sub(r'\s*<url>\s*<loc>' + re.escape(url) + r'</loc>[\s\S]*?</url>', '', sm2)
                changed['sitemap'] += 1
if APPLY and sm2 != sm:
    open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(sm2)

# repoint inbound links (indexes etc.) from card URLs to base URLs
repoints = 0
for lang in ('', 'vi/'):
    burl = '/' + lang + SERIES[0][0] + '/' if False else None
for base, cards in SERIES:
    for lang in ('', 'vi/'):
        base_url = f'/{lang}{base}/'
        for c in cards:
            for f in ['blog/index.html', 'vi/blog/index.html']:
                h = read(f)
                h2 = h.replace(f'/{lang}{c}/', f'/{lang}{base}/')
                if h2 != h:
                    repoints += 1
                    if APPLY:
                        open(f, 'w', encoding='utf-8', newline='\n').write(h2)
changed['index_links'] = repoints
print('summary:', changed)
