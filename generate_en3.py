import json
from pathlib import Path

base = Path(r'D:\Github Repos\tennis-unified')

# Load article metadata
with open(base / 'articles_metadata.json', 'r', encoding='utf-8') as f:
    articles_data = json.load(f)

# Load all content files using pathlib
content_files = {}
content_dir = base / 'article_content'
for i in range(34, 44):
    filename = f'{i:02d}_content.html'
    path = content_dir / filename
    with open(path, 'r', encoding='utf-8') as f:
        content_files[f'{i:02d}'] = f.read()

print('Content files loaded:', list(content_files.keys()))

# Read reference page
ref_path = base / 'en/articles/EN-tenniskb-kinetic-chain-efficiency-and-energy-leak-audits/index.html'
with open(ref_path, 'r', encoding='utf-8') as f:
    ref_page = f.read()

# Extract templates
article_start = ref_page.find('<article class="md-content__inner md-typeset">')
head_template = ref_page[:article_start]

article_end = ref_page.find('</article>', article_start)
article_template = ref_page[article_start:article_end]

foot_template = ref_page[article_end + len('</article>'):]

breadcrumb_start = article_template.find('<!-- TP-BREADCRUMB-START -->')
breadcrumb_end = article_template.find('<!-- TP-NAV-END -->')
breadcrumb_template = article_template[breadcrumb_start:breadcrumb_end + len('<!-- TP-NAV-END -->')]

nav_start = article_template.find('<!-- TP-NAV-START -->')
nav_end = article_template.find('<!-- TP-NAV-END -->', nav_start)
nav_template = article_template[nav_start:nav_end + len('<!-- TP-NAV-END -->')]

pillar_slugs = {"biomechanics": "biomechanics", "neurology": "neurology"}

def generate_en_page(article_meta, content_html):
    slug = article_meta["slug"]
    title = article_meta["title"]
    pillar = article_meta["pillar"]
    pillar_title = article_meta["pillar_title"]
    prev_slug = article_meta["prev"]
    next_slug = article_meta["next"]
    
    vi_slug = "VI-" + slug[3:]
    
    head = head_template.replace(
        'Kinetic Chain Efficiency and Energy Leak Audits - Tennis Unified Library',
        f'{title} - Tennis Unified Library'
    ).replace(
        'TennisKB — Kinetic Chain Efficiency and Energy Leak Audits | Tennis Future Lab',
        f'TennisKB — {title} | Tennis Future Lab'
    ).replace(
        '/en/articles/EN-tenniskb-kinetic-chain-efficiency-and-energy-leak-audits/',
        f'/en/articles/{slug}/'
    ).replace(
        '/vi/articles/VI-tenniskb-kinetic-chain-efficiency-and-energy-leak-audits/',
        f'/vi/articles/{vi_slug}/'
    )
    
    breadcrumb = breadcrumb_template.replace(
        'Kinetic Chain Efficiency and Energy Leak Audits',
        title
    ).replace(
        '/en/articles/biomechanics/',
        f'/en/articles/{pillar_slugs[pillar]}/'
    ).replace(
        'Applied Biomechanics & Kinetics',
        pillar_title
    )
    
    nav = nav_template.replace(
        'href="/en/articles/EN-tenniskb-the-stretch-shortening-cycle-ssc-in-lower-chain-loading/"',
        f'href="/en/articles/{prev_slug}/"'
    ).replace(
        'href="/en/articles/EN-tenniskb-pelvic-snap-and-separation-angle-dynamics/"',
        f'href="/en/articles/{next_slug}/"'
    )
    
    article_content = f'{breadcrumb}\n\n<h1 id="content">{title}</h1>\n\n{content_html}\n\n{nav}'
    
    full_page = head + f'<article class="md-content__inner md-typeset">\n\n{article_content}\n\n</article>\n' + foot_template
    
    return full_page

# Write all EN pages
for i, article_meta in enumerate(articles_data):
    num = f"{34+i:02d}"
    content = content_files[num]
    page = generate_en_page(article_meta, content)
    
    slug = article_meta["slug"]
    out_dir = base / 'en/articles' / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / 'index.html'
    
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(page)
    
    print(f'Written: {slug} ({len(page)} chars)')

print('All EN pages generated!')