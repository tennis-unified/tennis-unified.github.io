# AGENT GUIDELINES & ARCHITECTURE INSTRUCTIONS

> **CRITICAL DIRECTIVE FOR ALL AI AGENTS (Antigravity, Claude, Cursor, Copilot, Workbuddy):**  
> Read and adhere strictly to these guidelines before making changes or deployments to this repository.

---

## 1. GitHub Pages Deployment Architecture (DO NOT CHANGE TO LEGACY)

Both `tennis-unified.github.io` and `tenniskb.github.io` are large production knowledge bases (~5.3 GB, 28,000+ static files).

* **Builder Method:** **MUST ALWAYS USE GitHub Actions for Pages (`build_type: workflow`)**.
* **DO NOT REVERT TO LEGACY BUILDER:** The GitHub legacy builder enforces a strict **1 GB published site limit** and a **10-minute timeout**. Because the repository exceeds 5 GB, any legacy build will immediately fail with `"Page build failed."`
* **Production Branches:**
  - `tennis-unified/tennis-unified.github.io`: Production branch is **`main`**.
  - `tenniskb/tenniskb.github.io`: Production branch is **`master`**.
* **Workflow Configuration (`.github/workflows/deploy-pages.yml`):**
  - Always keep `fetch-depth: 1` under `actions/checkout@v4` to perform shallow cloning. This prevents downloading gigabytes of historical git objects and cuts build time drastically.
  - Deployment is fully automated on push to the production branch.

---

## 2. GitHub Releases & PDF Storage Policy

* **No Giant Binaries in Git:** Do not commit multi-hundred-megabyte raw PDFs directly into the repository.
* **Authoritative Release Repo:**
  - The ONLY active release repository is: [`tennis-unified/tennis-unified.github.io`](https://github.com/tennis-unified/tennis-unified.github.io).
  - Current raw English source doubles books live under release tag: [`sources-v1`](https://github.com/tennis-unified/tennis-unified.github.io/releases/tag/sources-v1).
* **Non-Existent Repos (NEVER LINK TO THESE):**
  - `https://github.com/tennis-unified/books` ❌ **DOES NOT EXIST (404)**
  - `https://github.com/tennis-unified/tnkbgap` ❌ **DOES NOT EXIST (404)**
  - Never generate or restore iframe / button links pointing to `tennis-unified/books` or `tennis-unified/tnkbgap`.
* **Book Reader Rules (`vi/books/read/*`):**
  - If a book has an active self-hosted PDF (e.g. `/vi/books/*_Vietnamese_Final.pdf`) or an active release asset on `sources-v1`, link to it.
  - If a book does **not** have an uploaded PDF, **keep the reader block stripped**. Never re-add broken Google Viewer iframes or dead download buttons.

---

## 3. Formatting & Code Integrity

* **Line Endings (CRLF):** Files in this repository are edited on Windows and use CRLF line endings. Preserve existing line endings (`newline=""` in Python scripts).
* **Mirror Parity:** `tennis-unified` and `tenniskb` are sister mirrors. Structural fixes, reader links, and article additions should be kept synchronized between both repositories.
* **Cleanup:** Never commit agent scratch files, logs, or temporary directories (e.g. `.workbuddy-ai/`, `tmp_*`).

---

## 4. Verified Operational Notes (measured 2026-10-02, not assumed)

* **Local checkout -> remote mapping (do not guess):**
  - `D:\Github Repos\tennis-unified` -> remote `origin` = `tennis-unified/tennis-unified.github.io`, branch `main`.
  - `D:\Github Repos\tenniskb` -> remote **`origin`** = `tenniskb/tenniskb.github.io`, branch `master` (this is the live site). The same directory also carries a second remote `hpd` = `henryPhamDuc/tenniskb`, which is a different, non-production copy. Always push to `origin`.
* **Credentials are per-account; never echo a token into logs, docs or commits.** The PAT embedded in each repository's `origin` URL is valid for that repository only. The token embedded in `D:\Github Repos\tenniskb-repo` returns HTTP 401 (expired) - do not rely on it.
* **Diagnosing a deploy:** while `build_type: workflow` is active, the legacy `GET /repos/{owner}/{repo}/pages/builds` endpoint returns stale history and is NOT authoritative. Read Actions runs instead (`GET /repos/{owner}/{repo}/actions/runs`). Workflows in these repos: `Deploy GitHub Pages`, `Site Health Audit`, `Link and Image Audit`.
* **Legacy-builder failure signature:** `status=errored`, `duration=0`, `error.message="Page build failed."` with no console output means the published site exceeded the legacy 1 GB limit / 10-minute timeout. That is an infrastructure symptom, never a content bug - keep the Actions workflow as the Pages source and do not delete content to "make the build fit".
* **Patching generated HTML:** read and write bytes and preserve the file's existing EOL. If `git diff --stat` reports a whole file changed instead of only the intended lines, the edit converted CRLF to LF; revert with `git checkout -- <path>` and redo with EOL preservation.
* **200-article knowledge base pipeline (articles 145-200):** `scripts/gen145_200.py` (with `gen145_200_data_*.py` and `gen145_200_pools_*.py`), `scripts/deploy_145_200.py`, `scripts/verify_145_200.py`, `scripts/audit_vi_leaks_145_200.py`, `scripts/vi_title_overrides.py`, `scripts/build_video_map_145_200.py`, `scripts/update_sitemap_145_200.py`. Titles come from `scripts/articles_200_data.json` and `scripts/articles_145_200_meta.json`; any catalogue VI title still written in English must be overridden through `vi_title_overrides.py` before rendering, and the same mapping must also be applied to the landing and pillar index pages.
* **Mirroring content:** the two sites are separate repositories, not forks. A content change is complete only when it exists in both `main` (tennis-unified) and `master` (tenniskb). Article pages, the root `/articles/` mirror, `sitemap.xml` and `sitemap.xml.gz` must match in both.
