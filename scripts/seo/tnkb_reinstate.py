"""Re-include the tenniskb/ archive in the site sections (user decision).

- Real-content index pages (>= 50 body words): drop the noindex robots meta,
  add a hreflang block (en/vi twins inside the archive + x-default), keep
  self-canonical.
- Thin pages (< 50 words): stay noindexed.
- Real pages' URLs appended to sitemap.xml.
Dry-run default, --apply writes.
"""
import re, sys, glob, os

APPLY = '--apply' in sys.argv
files = glob.glob('tenniskb/**/index.html', recursive=True)

def body_words(h):
    b = re.search(r'<body[\s\S]*?</body>', h, re.S)
    if not b:
        return 0
    t = re.sub(r'<script[\s\S]*?</script>|<style[\s\S]*?</style>|<nav[\s\S]*?</nav>', '', b.group(0))
    return len(re.sub(r'<[^>]+>', ' ', t).split())

def rel_of(f):
    return f.replace('tenniskb/', '').replace('tenniskb' + os.sep, '') \
            .replace(os.sep, '/').replace('/index.html', '').replace('index.html', '')

def url_of(rel):
    return '/tenniskb/' + rel + '/' if rel else '/tenniskb/'

rels = {}
for f in files:
    rels[rel_of(f)] = f

real, thin = [], []
for rel, f in rels.items():
    h = open(f, encoding='utf-8', errors='replace').read()
    (real if body_words(h) >= 50 else thin).append((rel, f, h))
print('real:', len(real), 'thin:', len(thin))

def lang_of(rel):
    return 'vi' if rel.startswith('vi/') else 'en'

def twin_of(rel):
    if rel.startswith('en/'):
        cand = 'vi/' + rel[3:]
    elif rel.startswith('vi/'):
        cand = 'en/' + rel[3:]
    else:
        return None
    return cand if cand in dict((r, f) for r, f, _ in real + thin) else None

changed = 0
sm_urls = []
for rel, f, h in real:
    orig = h
    # 1. drop noindex
    h = re.sub(r'\s*<meta name="robots" content="[^"]*noindex[^"]*">', '', h)
    # 2. hreflang block
    if 'hreflang' not in h:
        lang = lang_of(rel)
        twin = twin_of(rel)
        self_url = 'https://tenniskb.github.io' + url_of(rel)
        tags = []
        if twin:
            twin_url = 'https://tenniskb.github.io' + url_of(twin)
            other = 'en' if lang == 'vi' else 'vi'
            tags.append(f'  <link rel="alternate" href="{twin_url}" hreflang="{other}">')
            tags.append(f'  <link rel="alternate" href="{self_url}" hreflang="{lang}">')
            tags.append(f'  <link rel="alternate" href="{twin_url}" hreflang="x-default">')
        else:
            tags.append(f'  <link rel="alternate" href="{self_url}" hreflang="{lang}">')
            tags.append(f'  <link rel="alternate" href="{self_url}" hreflang="x-default">')
        block = '\n'.join(tags) + '\n'
        i = h.find('</head>')
        h = h[:i] + block + h[i:]
    if h != orig:
        changed += 1
        if APPLY:
            open(f, 'w', encoding='utf-8', newline='\n').write(h)
    sm_urls.append('https://tenniskb.github.io' + url_of(rel))

print('pages changed:', changed)
print('sitemap URLs to add:', len(sm_urls))
sm = open('sitemap.xml', encoding='utf-8').read()
have = sum(1 for u in sm_urls if u in sm)
print('already in sitemap:', have)
if APPLY:
    add = ''.join(f'  <url><loc>{u}</loc></url>\n' for u in sm_urls if u not in sm)
    if add:
        sm = sm.replace('</urlset>', add + '</urlset>')
        open('sitemap.xml', 'w', encoding='utf-8', newline='\n').write(sm)
        print('sitemap: added', add.count('<loc>'))
