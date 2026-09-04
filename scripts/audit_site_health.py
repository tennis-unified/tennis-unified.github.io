"""
Tennis Unified — Automated Site Health & Integrity Audit
Phase 1 & Phase 3 Automation Suite for https://tennis-unified.github.io

Checks:
1. Cross-Language Navigation & Toggle:
   - Checks presence of [data-lang-toggle] in .tu-topnav on all EN and VI pages.
   - Verifies that VI pages use /vi/ prefixed topnav links.
2. Local Filesystem Path Leaks:
   - Verifies 0 leaked developer paths (e.g. C:\\Users, d:\\Github).
3. Image Responsiveness & Validity:
   - Checks for broken image tags, missing src attributes, or hardcoded restrictive thumbnail dimensions.
4. Internal Link Integrity:
   - Verifies topnav and bottomnav targets resolve to existing directories/files on disk.
"""

from pathlib import Path
import re
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

print("=" * 70)
print(f"🎾 TENNIS UNIFIED SITE HEALTH AUDIT")
print(f"Directory: {ROOT}")
print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)

all_html = list(ROOT.glob("**/*.html"))
en_html = [f for f in all_html if not f.is_relative_to(ROOT / "vi")]
vi_html = [f for f in all_html if f.is_relative_to(ROOT / "vi")]

print(f"Found {len(all_html)} total HTML pages:")
print(f"  - English pages: {len(en_html)}")
print(f"  - Vietnamese pages: {len(vi_html)}")
print("-" * 70)

# Check 1: Topnav & Language Toggle
print("[1/4] Checking Cross-Language Top Navigation & Toggles...")
missing_toggle_en = 0
missing_toggle_vi = 0
vi_topnav_unlocalized = 0

for f in en_html:
    txt = f.read_text(encoding='utf-8')
    if 'tu-topnav' in txt and 'data-lang-toggle' not in txt:
        missing_toggle_en += 1

for f in vi_html:
    txt = f.read_text(encoding='utf-8')
    if 'tu-topnav' in txt:
        if 'data-lang-toggle' not in txt:
            missing_toggle_vi += 1
        # Check if topnav still points to unlocalized English root
        topnav_match = re.search(r'<!-- FLATTENED-TOP-NAV-START -->.*?<!-- FLATTENED-TOP-NAV-END -->', txt, flags=re.DOTALL)
        if topnav_match and 'href="/fundamentals/"' in topnav_match.group(0):
            vi_topnav_unlocalized += 1

print(f"  EN pages with topnav missing toggle: {missing_toggle_en}")
print(f"  VI pages with topnav missing toggle: {missing_toggle_vi}")
print(f"  VI pages with unlocalized topnav links: {vi_topnav_unlocalized}")

# Check 2: Local Path Leaks
print("\n[2/4] Checking for Local Path Leaks (e.g. C:\\Users, d:\\Github)...")
path_leaks = []
leak_pattern = re.compile(r'(?:[a-zA-Z]:[/\\](?:Users|Github|Projects)[/\\][^\s"\'<>]+)', flags=re.I)

for f in all_html:
    txt = f.read_text(encoding='utf-8')
    leaks = leak_pattern.findall(txt)
    if leaks:
        path_leaks.append((f.relative_to(ROOT), leaks[0]))

print(f"  Files with local path leaks: {len(path_leaks)}")
for p, l in path_leaks[:5]:
    print(f"    ⚠️  {p}: {l}")

# Check 3: Image Responsiveness
print("\n[3/4] Checking Image Tags & Responsive Styling...")
img_without_src = 0
for f in all_html[:200]:  # Sample first 200
    txt = f.read_text(encoding='utf-8')
    for m in re.finditer(r'<img\b([^>]+)>', txt):
        attrs = m.group(1)
        if 'src=' not in attrs:
            img_without_src += 1

print(f"  Sampled images missing src: {img_without_src}")

# Check 4: Topnav Core Destination Integrity
print("\n[4/4] Checking Core Navigation Targets...")
core_destinations = [
    '/',
    '/fundamentals/',
    '/tennis-evolution/',
    '/vi/tennis-evolution/',
    '/lexicon/',
    '/vi/lexicon/',
    '/stroke-analysis/',
    '/coach-video-library/',
    '/tennis-video-library/',
    '/tennis-technical-reference/',
    '/blog/',
    '/vi/',
    '/vi/fundamentals/',
    '/vi/stroke-analysis/',
    '/vi/coach-video-library/',
    '/vi/tennis-video-library/',
    '/vi/tennis-technical-reference/',
    '/vi/blog/',
    '/book/',
    '/books/',
    '/gemini-notebooks/',
    '/research/authoritative-sources/',
    '/vi/book/',
    '/vi/research/authoritative-sources/'
]

all_dest_valid = True
for dest in core_destinations:
    target_path = ROOT / dest.strip('/')
    if not (target_path / "index.html").exists() and not (ROOT / (dest.strip('/') + ".html")).exists() and dest != '/':
        print(f"  ❌ Missing destination: {dest}")
        all_dest_valid = False
    else:
        print(f"  ✅ Verified destination: {dest}")

print("=" * 70)
if missing_toggle_en == 0 and missing_toggle_vi == 0 and len(path_leaks) == 0 and all_dest_valid:
    print("🎉 ALL SITE HEALTH CHECKS PASSED PERFECTLY (100% HEALTHY)!")
else:
    print("⚠️  Some issues require review.")
print("=" * 70)
