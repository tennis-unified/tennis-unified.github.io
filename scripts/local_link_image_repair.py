#!/usr/bin/env python3
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, unquote
from posixpath import normpath, relpath
from html import unescape
from collections import Counter
import re

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "SITE_LINK_IMAGE_AUDIT.md"
HOSTS = {"tennis-unified.github.io", "www.tennis-unified.github.io"}
RE = re.compile(r'(?P<a>href|src)\s*=\s*(?P<q>["\'])(?P<u>.*?)(?P=q)', re.I)
IMG = {'.png','.jpg','.jpeg','.webp','.gif','.svg','.avif','.bmp','.ico'}
htmls = [p for p in ROOT.rglob('*.html') if '.git' not in p.parts]
files = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts}
lower = {}
for f in files: lower.setdefault(f.lower(), []).append(f)
fixes=[]; unresolved=Counter(); external=set()

def src_url(p):
 r=p.relative_to(ROOT).as_posix()
 if r=='index.html': return '/'
 if r.endswith('/index.html'): return '/'+r[:-10]+'/'
 return '/'+r

def route_candidates(path):
 c=unquote(path.split('#')[0].split('?')[0]).replace('\\','/').lstrip('/')
 c=re.sub(r'/+','/',c)
 if c in ('','.'): return ['index.html']
 out=[]
 for q in (c, c.rstrip('/')):
  if q in files: out.append(q)
  if q and q+'/index.html' in files: out.append(q+'/index.html')
  if q and not q.endswith('.html') and q+'.html' in files: out.append(q+'.html')
  if q.lower() in lower: out.extend(lower[q.lower()])
 out=sorted(set(out))
 return out

def replacement(p, target, raw):
 u=urlsplit(raw)
 if target=='index.html': target_url='/'
 elif target.endswith('/index.html'): target_url='/'+target[:-10]+'/'
 else: target_url='/'+target
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
  joined=normpath(base+u.path) if not raw.startswith('/') else normpath(u.path)
  if joined.startswith('../') or joined=='..':
   unresolved[(p.relative_to(ROOT).as_posix(),a,raw,'OUTSIDE_SITE')]+=1
   continue
  path='/' + joined.lstrip('/')
  cands=route_candidates(path)
  t=cands[0] if len(cands)==1 else None
  if t:
   clean=unquote(path).lstrip('/').rstrip('/')
   canonical = t=='index.html' and clean=='' or clean==t or clean+'/index.html'==t
   if not canonical:
    new=replacement(p,t,raw)
    if new!=raw: reps.append((m.start('u'),m.end('u'),new,raw,t,a))
   continue
  if a=='src':
   name=Path(path).name.lower(); exact=[f for f in files if Path(f).name.lower()==name]
   stem=Path(name).stem; stems=[f for f in files if Path(f).stem.lower()==stem and Path(f).suffix.lower() in IMG]
   target=(exact[0] if len(exact)==1 else (stems[0] if len(stems)==1 else None))
   if target:
    new=replacement(p,target,raw); reps.append((m.start('u'),m.end('u'),new,raw,target,a)); continue
  unresolved[(p.relative_to(ROOT).as_posix(),a,raw,path)]+=1
 if reps:
  for x in sorted(set(reps),reverse=True):
   i,j,new,old,target,a=x; text=text[:i]+new+text[j:]; fixes.append((p.relative_to(ROOT).as_posix(),a,old,new,target))
  p.write_text(text,encoding='utf-8')

fixes=sorted(set(fixes))
lines=['# Tennis Unified — Link & Image Audit','',f'Scanned **{len(htmls):,} HTML pages**.','',f'- Automatic local repairs: **{len(fixes):,}**',f'- Unique unresolved local references: **{len(unresolved):,}**',f'- Unresolved occurrences: **{sum(unresolved.values()):,}**',f'- External URLs discovered (not tested by local pass): **{len(external):,}**','', 'The local pass treats GitHub Pages directory routes (`/foo/` backed by `foo/index.html`) as valid and deduplicates repeated references.','']
if fixes:
 lines+=['## Automatic repairs','']+[f'- `{p}` — `{a}` `{old}` → `{new}` (target `{t}`)' for p,a,old,new,t in fixes[:10000]]+['']
if unresolved:
 lines+=['## Unresolved local references','']+[f'- `{p}` — `{a}` `{raw}` → `{path}` — **{n} occurrence(s)**' for (p,a,raw,path),n in unresolved.most_common(10000)]+['']
REPORT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(f'HTML pages: {len(htmls)}')
print(f'Automatic repairs: {len(fixes)}')
print(f'Unique unresolved local: {len(unresolved)}')
print(f'Unresolved occurrences: {sum(unresolved.values())}')
print(f'External URLs discovered: {len(external)}')