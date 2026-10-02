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
