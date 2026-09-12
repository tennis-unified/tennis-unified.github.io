#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, unquote
from posixpath import normpath, relpath
from html import unescape
import re

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "SITE_LINK_IMAGE_AUDIT.md"
HOSTS = {"tennis-unified.github.io", "www.tennis-unified.github.io"}
RE = re.compile(r'(?P<a>href|src)\s*=\s*(?P<q>["\'])(?P<u>.*?)(?P=q)', re.I)
IMG = {'.png','.jpg','.jpeg','.webp','.gif','.svg','.avif','.bmp'}
htmls = [p for p in ROOT.rglob('*.html') if '.git' not in p.parts]
files = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts}
lower = {}
for f in files: lower.setdefault(f.lower(), []).append(f)
fixes=[]; unresolved=[]; external=set()

def src_url(p):
 r=p.relative_to(ROOT).as_posix()
 return '/' if r=='index.html' else ('/'+r[:-10]+'/' if r.endswith('/index.html') else '/'+r)

def candidate(path):
 c=unquote(path.split('#')[0].split('?')[0]).lstrip('/')
 c=re.sub(r'/+','/',c)
 while c.startswith('../'): c=c[3:]
 x=[]
 if c in files: x.append(c)
 if c.endswith('/') and c[:-1]+'/index.html' in files: x.append(c[:-1]+'/index.html')
 if not c.endswith('.html'):
  if c+'.html' in files: x.append(c+'.html')
  if c.rstrip('/')+'/index.html' in files: x.append(c.rstrip('/')+'/index.html')
 if c.endswith('.html') and c[:-5]+'/index.html' in files: x.append(c[:-5]+'/index.html')
 x += lower.get(c.lower(),[])
 x=sorted(set(x))
 return x[0] if len(x)==1 else ('AMBIGUOUS' if x else None)

def replacement(p, target, raw):
 u=urlsplit(raw)
 target_url='/' if target=='index.html' else ('/'+target[:-10]+'/' if target.endswith('/index.html') else '/'+target)
 base=src_url(p); base=base if base.endswith('/') else base.rsplit('/',1)[0]+'/'
 path=target_url if raw.startswith('/') else relpath(target_url,base)
 return urlunsplit((u.scheme,u.netloc,path,u.query,u.fragment))

for p in htmls:
 text=p.read_text(encoding='utf-8',errors='ignore'); reps=[]
 for m in RE.finditer(text):
  a=m.group('a').lower(); raw=unescape(m.group('u').strip())
  if not raw or raw.startswith(('#','javascript:','mailto:','tel:','data:','blob:')): continue
  u=urlsplit(raw)
  if u.scheme or u.netloc or raw.startswith('//'):
   if u.netloc and u.netloc.lower() not in HOSTS: external.add(raw)
   continue
  base=src_url(p); base=base if base.endswith('/') else base.rsplit('/',1)[0]+'/'
  path='/' + normpath(base+u.path).lstrip('/') if not raw.startswith('/') else u.path
  t=candidate(path)
  if t and t!='AMBIGUOUS':
   clean=unquote(path).lstrip('/').rstrip('/')
   if not ((t=='index.html' and path=='/') or clean==t or clean+'/index.html'==t):
    new=replacement(p,t,raw)
    if new!=raw: reps.append((m.start('u'),m.end('u'),new,raw,t,a))
   continue
  if a=='src':
   name=Path(path).name.lower(); exact=[f for f in files if Path(f).name.lower()==name]
   stem=Path(name).stem; stems=[f for f in files if Path(f).stem.lower()==stem and Path(f).suffix.lower() in IMG]
   target=(exact[0] if len(exact)==1 else (stems[0] if len(stems)==1 else None))
   if target:
    new=replacement(p,target,raw); reps.append((m.start('u'),m.end('u'),new,raw,target,a)); continue
  unresolved.append((p.relative_to(ROOT).as_posix(),a,raw,path))
 if reps:
  for x in sorted(set(reps),reverse=True):
   i,j,new,old,target,a=x; text=text[:i]+new+text[j:]; fixes.append((p.relative_to(ROOT).as_posix(),a,old,new,target))
  p.write_text(text,encoding='utf-8')

fixes=sorted(set(fixes)); unresolved=sorted(set(unresolved))
lines=['# Tennis Unified — Link & Image Audit','',f'Scanned **{len(htmls):,} HTML pages**.','',f'- Automatic local repairs: **{len(fixes):,}**',f'- Unresolved local references: **{len(unresolved):,}**',f'- External URLs discovered (not tested by local pass): **{len(external):,}**','']
if fixes:
 lines+=['## Automatic repairs','']+[f'- `{p}` — `{a}` `{old}` → `{new}` (target `{t}`)' for p,a,old,new,t in fixes[:5000]]+['']
if unresolved:
 lines+=['## Unresolved local references','']+[f'- `{p}` — `{a}` `{raw}` → resolved `{path}`' for p,a,raw,path in unresolved[:5000]]+['']
REPORT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'HTML pages: {len(htmls)}'); print(f'Automatic repairs: {len(fixes)}'); print(f'Unresolved local: {len(unresolved)}'); print(f'External URLs discovered: {len(external)}')
