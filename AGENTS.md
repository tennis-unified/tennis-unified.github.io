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
  - `tenniskb/tenniskb.github.io`: Production branch is **`main`** (its default branch, and the
    only branch `deploy-pages.yml` triggers on). A stale `master` branch still exists from
    before 2026-10-02 - it is not built and not served; **never push to it**.
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

* **Line Endings (LF):** Both repositories are normalised to LF. `.gitattributes` carries `* text=auto eol=lf` and `core.autocrlf=false`, so git stores LF in the blob and checks LF out; a Windows working tree that still shows CRLF is stale, not authoritative. Write new files as LF (Python: open in binary, or `newline=""`), never reintroduce CRLF, and never delete the `.gitattributes` - removing it would let `git add` rewrite every touched file back to CRLF and desynchronise the two repos.
* **Mirror Parity:** `tennis-unified` and `tenniskb` are sister mirrors. Structural fixes, reader links, and article additions should be kept synchronized between both repositories.
* **Cleanup:** Never commit agent scratch files, logs, or temporary directories (e.g. `.workbuddy-ai/`, `tmp_*`).

---

## 4. Verified Operational Notes (measured 2026-10-02, not assumed)

* **Local checkout -> remote mapping (do not guess; re-verified 2026-10-10):**
  - `D:\Github Repos\tennis-unified` -> remote `origin` = `tennis-unified/tennis-unified.github.io`, branch `main`. It also carries `hpd` = `henryPhamDuc/tenniskb` (a different, non-production copy - never push there) and `tenniskb` = `tenniskb/tenniskb.github.io`.
  - `D:\Github Repos\tnkb-mirror-full` -> remote `origin` = `tenniskb/tenniskb.github.io`, branch `main` (this is the live mirror). `D:\Github Repos\tnkb-mirror` is a `--filter=blob:none` partial clone of the same repo.
  - `D:\Github Repos\tenniskb-repo` -> remote `origin` = `tenniskb/tenniskb` (the MkDocs source), branch `gh-pages`.
  - `D:\Github Repos\tenniskb` (the path previously documented here) **no longer exists**.
* **Credentials are per-account; never echo a token into logs, docs or commits.** The PAT embedded in each repository's `origin` URL is valid for that repository only. The token embedded in `D:\Github Repos\tenniskb-repo` returns HTTP 401 (expired) - do not rely on it.
* **Diagnosing a deploy:** while `build_type: workflow` is active, the legacy `GET /repos/{owner}/{repo}/pages/builds` endpoint returns stale history and is NOT authoritative. Read Actions runs instead (`GET /repos/{owner}/{repo}/actions/runs`). Workflows in these repos: `Deploy GitHub Pages`, `Site Health Audit`, `Link and Image Audit`.
* **Legacy-builder failure signature:** `status=errored`, `duration=0`, `error.message="Page build failed."` with no console output means the published site exceeded the legacy 1 GB limit / 10-minute timeout. That is an infrastructure symptom, never a content bug - keep the Actions workflow as the Pages source and do not delete content to "make the build fit".
* **Patching generated HTML:** read and write bytes and preserve the file's existing EOL. If `git diff --stat` reports a whole file changed instead of only the intended lines, the edit converted CRLF to LF; revert with `git checkout -- <path>` and redo with EOL preservation.
* **200-article knowledge base pipeline (articles 145-200):** `scripts/gen145_200.py` (with `gen145_200_data_*.py` and `gen145_200_pools_*.py`), `scripts/deploy_145_200.py`, `scripts/verify_145_200.py`, `scripts/audit_vi_leaks_145_200.py`, `scripts/vi_title_overrides.py`, `scripts/build_video_map_145_200.py`, `scripts/update_sitemap_145_200.py`. Titles come from `scripts/articles_200_data.json` and `scripts/articles_145_200_meta.json`; any catalogue VI title still written in English must be overridden through `vi_title_overrides.py` before rendering, and the same mapping must also be applied to the landing and pillar index pages.
* **Mirroring content:** `tennis-unified/tennis-unified.github.io` is a **fork** of `tenniskb/tenniskb.github.io`, and the tree is mirrored to it verbatim by `.github/workflows/mirror.yml` (server-side `merge-upstream`). A content change is complete only when it exists in both `main` branches. **The one deliberate divergence is `/articles/`** - the fork retired it into redirect stubs (SEO decision D2), this repo keeps all 200 pages as real content. See section 6.

---

## 6. SEO Host Policy (decisions D1 / D2 / D3)

The same bytes are served from two hosts, so any absolute host baked into a page is wrong on one of
them. That is the whole reason for these decisions - read them before touching `<head>` metadata.

* **D1 - per-host self-canonical.** `canonical`, `hreflang` and `og:url` are emitted **root-relative**
  (`/en/articles/<slug>/`), which resolves to whichever host serves the page. Never write
  `https://tenniskb.github.io/...` or `https://tennis-unified.github.io/...` into a page's canonical,
  hreflang or `og:url`. `og:image` is the exception: it must stay absolute, because the URL is consumed
  off-site by social crawlers.
* **The one sanctioned absolute host:** a sitemap `<loc>` must be a full URL per sitemaps.org, so
  `sitemap.xml` stays on `https://tennis-unified.github.io` and `robots.txt` advertises only that
  sitemap, on both hosts. This is deliberate - do not "fix" it into a relative URL, and do not add the
  second host back.
* **D2 - `/articles/` is the fork's decision, not this repo's.** Here `RETIRE_ARTICLES = False` in
  `scripts/seo/seo_fix.py`; `/articles/` holds 200 real pages, so it is a content space and gets the
  same treatment as `en/articles/` and `vi/articles/`. If D2 is ever adopted here, flip that flag and
  re-run `apply` + `verify` - it stubs all 200 pages at once.
* **D3 - extra-title blog copies.** 17 blog pages exist under a second title; their canonical points at
  the primary slug. The blog is otherwise **not** given blanket self-canonicals (722 pages) - that was
  never part of the agreed change.
* **Tooling.** `scripts/seo/seo_fix.py audit | apply [--dry-run] | verify` walks only
  `CONTENT_PREFIXES` (`articles/`, `en/articles/`, `vi/articles/`). `verify` exits 1 on any failure and
  is the gate - run it after every metadata change.
* **Tree-wide sweep.** Pages outside those three prefixes are not covered by `seo_fix.py`. Use
  `scripts/seo/d1_treewide.py` (`--write` to apply) to convert the remaining absolute canonicals and
  `og:url` to root-relative, tree-wide. It never invents a target: a URL whose path does not resolve on
  disk is reported, and a canonical whose declared target 404s is replaced with the page's own path
  rather than left pointing at nothing.


---

## 5. Mandatory Dual-Footer Standard for All HTML Pages

Every newly authored, migrated, or patched HTML page across both repositories **MUST ALWAYS** include both footer components before `</body>`:

1. **Material Design Footer (`md-footer`):**
```html
  <footer class="md-footer">
    <div class="md-footer-meta md-typeset">
      <div class="md-footer-meta__inner md-grid">
        <div class="md-copyright">
          <div class="md-copyright__highlight">
            © 2026 Henry Phạm Đức · Tennis Future Lab Research · All contents are for educational purpose.
          </div>
        </div>
      </div>
    </div>
  </footer>
</div>
```

2. **Tennis Unified Custom Pill Footer (`tu-footer`):**
```html
<footer class="tu-footer" style="background: var(--card); border-top: 1px solid var(--border); color: var(--ink-muted); padding: 1.5rem 1rem; text-align: center; font-size: 0.92rem; margin-top: 3rem;">
  <!-- For Vietnamese pages: -->
  <div style="font-size: 0.85rem; color: var(--accent-dark);">Trang web này được xây dựng với ❤️ cho cộng đồng quần vợt Việt Nam 🎾 by Henry Phạm</div>
  <!-- For English pages: -->
  <!-- <div style="font-size: 0.85rem; color: var(--accent-dark);">Built with ❤️ for the Global & Vietnamese Tennis Community 🎾 by Henry Pham</div> -->
</footer>
</body>
</html>
```
* **Strict Rule:** Never close `</body>` without both `md-footer` and `tu-footer`. This is required for visual consistency, copyright compliance, and layout balance across all viewports.

