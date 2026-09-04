import os
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

repo_root = r"D:\Github Repos\research-intranet"
mkdocs_bin = os.path.join(repo_root, ".venv", "Scripts", "mkdocs.exe")
site_dir = os.path.join(repo_root, "site")

print("=== [1/3] Building English Site ===")
res_en = subprocess.run([mkdocs_bin, "build"], cwd=repo_root, capture_output=True, text=True, encoding="utf-8")
print("  MkDocs EN exit code:", res_en.returncode)
if res_en.returncode != 0:
    print("  MkDocs EN stderr:", res_en.stderr[:500])

print("=== [2/3] Building Vietnamese Site ===")
res_vi = subprocess.run([mkdocs_bin, "build", "-f", "mkdocs.vi.yml"], cwd=repo_root, capture_output=True, text=True, encoding="utf-8")
print("  MkDocs VI exit code:", res_vi.returncode)
if res_vi.returncode != 0:
    print("  MkDocs VI stderr:", res_vi.stderr[:500])

# Clean obsolete directory in site/book if exists
obsolete_en_slugs = [
    "chapter-01-the-kinetic-engine",
    "chapter-03-gravity-and-the-court",
    "chapter-04-blitz-chess-and-development",
    "chapter-07-the-kinetic-hammer",
    "chapter-13-the-bulletproof-body",
    "chapter-15-advanced-joint-kinetics-micro-dynamics",
]
for obs in obsolete_en_slugs:
    p = os.path.join(site_dir, "book", obs)
    if os.path.exists(p):
        try:
            shutil.rmtree(p)
            print(f"  Removed obsolete site directory: {obs}")
        except Exception as e:
            print(f"  Could not remove {obs}: {e}")

print("=== [3/3] Verifying Built Pages ===")
en_book = os.path.join(site_dir, "book")
vi_book = os.path.join(site_dir, "vi", "book")

en_pages = [f for f in sorted(os.listdir(en_book)) if os.path.isdir(os.path.join(en_book, f)) and f != "TUC" and f not in obsolete_en_slugs]
vi_pages = [f for f in sorted(os.listdir(vi_book)) if os.path.isdir(os.path.join(vi_book, f)) and f not in obsolete_en_slugs]

print(f"English Chapters ({len(en_pages)}):")
for p in en_pages:
    print(f"  EN: {p}")

print(f"\nVietnamese Chapters ({len(vi_pages)}):")
for p in vi_pages:
    print(f"  VI: {p}")

assert len(en_pages) == 16, f"Expected 16 EN chapters, got {len(en_pages)}"
assert len(vi_pages) == 16, f"Expected 16 VI chapters, got {len(vi_pages)}"
assert os.path.exists(os.path.join(en_book, "index.html")), "Missing EN book index.html"
assert os.path.exists(os.path.join(vi_book, "index.html")), "Missing VI book index.html"

print("\nALL 32 CHAPTERS BUILT AND VERIFIED SUCCESSFULLY!")
