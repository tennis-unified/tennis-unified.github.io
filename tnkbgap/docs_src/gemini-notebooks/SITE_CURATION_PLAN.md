# Tennis Knowledge Gap Intranet — Site Curation Plan

> **Source**: 32 Gemini NotebookLM Vaults (7,000+ grounded sources)
> **Target**: `D:\Github Repos\research-intranet` (MkDocs Material)
> **Live**: `http://localhost:8765/`

---

## Current State

- **Site generator**: MkDocs Material (`mkdocs.yml` + `docs/` → `site/`)
- **Existing nav sections**: Home, Books (133), Reports, Pipeline, Gemini Notebooks (partial), Reference
- **Current Gemini Notebooks nav**: 13 entries (Stroke Biomechanics, Neurological, Footwork, Tactical)
- **Existing docs**: `docs/gemini-notebooks/*.md` (14 files)

## Gap Analysis

| Vault Category | Current Nav Entries | Total Vaults | Missing |
|----------------|---------------------|--------------|---------|
| Elite Tennis Biomechanics | 13 | 20 | **7** |
| Internal Arts & Health | 0 | 3 | **3** |
| Mindset & Philosophy | 0 | 5 | **5** |
| AI & Engineering | 0 | 4 | **4** |
| Artifacts Directory | 1 | 1 | 0 |
| **Total** | **14** | **32** | **19** |

---

## Phase 1: Create Missing Markdown Doc Files

Create 19 new `.md` files in `docs/gemini-notebooks/`:

### 🎾 Elite Tennis — 7 Missing Vaults

| # | Slug | Title | Source Vault |
|---|------|-------|--------------|
| 1 | `the-hidden-engine-footwork.md` | KÌNH LỰC — Footwork Training | `9bf565cd-0228-4570-a071-7cd116993988` |
| 2 | `footwork-neural-control.md` | Động cơ ẩn: Bộ chân & Hệ thần kinh | `28cc5226-17e9-475e-a3c5-484e012075e9` |
| 3 | `tennis-king-equation.md` | Phương Trình Tennis King & Động Lực Học Thần Kinh | `e4cadd0e-322d-44a3-9596-fb7a91e15683` |
| 4 | `tennis-books-library.md` | Tennis Books (133 titles) | `b2646cc6-1dff-422a-b797-403cc7abb319` |
| 5 | `tennis-fundamentals.md` | Tennis Fundamentals | `b05f3704-2ce7-43c7-b4a8-fb7abd0b7ef8` |
| 6 | `tennis-neurological-specialist.md` | Tennis Neurological Specialist Deep Research | `94edafc6-77c0-48b3-86e5-66f48f470f5e` |
| 7 | `ky-nguyen-moi.md` | Kỷ Nguyên Mới Của Kỹ Thuật Quần Vợt Đỉnh Cao | `d84e4fe9-d69b-4c69-9e58-3ba644e52722` |
| 8 | `tennis-research-project.md` | Tennis Research Project | `0f19ffe8-c458-4ab1-8159-14ebaf9d323c` |
| 9 | `tennis-forehand.md` | Tennis Forehand | `807e6956-29f3-4b37-ae96-356a285b72fb` |
| 10 | `tennis-backhand.md` | Tennis Backhand | `0536ae95-0545-450e-b9aa-c3f1ad5f583b` |
| 11 | `tennis-serve-return.md` | Tennis Serve and Return of Serve | `e89c2363-7503-4bab-9bdd-88871dd1e302` |
| 12 | `tennis-volley.md` | Tennis Volley | `f55df0a7-2029-4c56-a96b-e0b5b45cad68` |
| 13 | `tennis-overhead-lob.md` | Tennis Overhead Smash and Lob | `f2561a77-5c84-451d-bf8e-dac9b3d61714` |
| 14 | `giao-trinh-5-nam.md` | Giáo trình Tennis 5 Năm: Tái Thiết Hệ Trục Cơ Sinh Học | `a49486ff-1891-4faf-9afc-dd935cefd409` |
| 15 | `road-to-pro.md` | Road to Pro Tennis | `1d4366f4-ffca-42af-9a9c-2dddde089f97` |
| 16 | `atp-coach-mastery.md` | Kỹ năng & Huấn luyện cùng coach ATP | `c6fe350c-c458-4a50-a2d8-e2350446e68d` |
| 17 | `fault-tolerant-library.md` | Thư viện Kỹ thuật từ Fault Tolerant Tennis | `c2d37981-9d12-4823-b544-4c4111dd2ea6` |
| 18 | `cam-nang-2026.md` | Cẩm Nang Quần Vợt 2026: Kình & Động Lực Học Tai Chi | `da2e6116-6d2e-478b-b117-4c322b1ae71e` |
| 19 | `tennis-specialty.md` | Tennis Specialty | `91360980-b1f4-4ec4-ab32-5efd10797f0d` |

### 🧘 Internal Arts & Health — 3 Vaults

| # | Slug | Title | Source Vault |
|---|------|-------|--------------|
| 20 | `taichi-qigong.md` | Taichi-ChiGong | `77a7b0bb-32f4-42bc-8485-69a91a2d4e05` |
| 21 | `health-tcm-energy.md` | Health, TCM, Energy Medicine | `d2401afd-0718-4fac-b429-5bca391d27a9` |
| 22 | `tuoi-52-tu-tap.md` | Tuổi 52: Tu Tập Nội Tại | `9a77b59a-d71c-46ad-9bde-18d0eb2ffa9b` |

### 🧠 Mindset & Philosophy — 5 Vaults

| # | Slug | Title | Source Vault |
|---|------|-------|--------------|
| 23 | `minimalism-essentialism.md` | Minimalism and Essentialism | `da8e95a5-5d42-48a2-81e9-6519fd598df1` |
| 24 | `self-help.md` | Self-Help | `bd6e234c-bb06-4105-9b7a-8074efe2066b` |
| 25 | `coaching-deliberate-practice.md` | Coaching and Deliberate Practice | `9abb4b65-5c2a-449b-bc78-fa6f19189def` |
| 26 | `psychology-philosophy.md` | Psychology, Human Science, Philosophy | `3199f045-36d0-4ec8-a18e-4210df3212b1` |
| 27 | `hanh-trinh-thuc-tinh.md` | Hành Trình Thức Tỉnh & Khoa Học Tâm Linh | `74c69e68-4420-4d35-8760-72a0842f7992` |

### 🤖 AI & Engineering — 4 Vaults

| # | Slug | Title | Source Vault |
|---|------|-------|--------------|
| 28 | `hermes-ai-use-cases.md` | Use Cases For Hermes & AIs | `b4591be3-1150-447b-9af1-1ab58f2bc030` |
| 29 | `metacognition-ai.md` | Metacognition in AI | `24003a0c-b51e-4b98-bfe2-043b99bff9b6` |
| 30 | `helpdesk-2026.md` | Helpdesk Tickets 2026 | `90ecb07b-80d8-4792-b080-f00c53fb453a` |
| 31 | `geotech-instruments.md` | Geotechnical Instruments & ADAS | `bf0a18f2-160e-493e-92a1-fbbbd44e15c8` |

---

## Phase 2: Update `mkdocs.yml` Nav

Add the following nav sections under the existing `Gemini Notebooks:` heading:

```yaml
  - Gemini Notebooks:
      - "Notebooks Hub": gemini-notebooks/index.md
      - "32 Vaults Artifacts Directory": gemini-notebooks/gemini-artifacts-vault-directory.md
      - "Tennis Studio Notes": gemini-notebooks/tennis-studio-notes-collection.md
      - "Elite Stroke Biomechanics & Kinetics":
          # ... existing 5 entries ...
          - "Footwork Training (Kình Lực)": gemini-notebooks/the-hidden-engine-footwork.md
          - "Neural Control & Footwork": gemini-notebooks/footwork-neural-control.md
          - "Tennis King Equation": gemini-notebooks/tennis-king-equation.md
          - "Tennis Books Library": gemini-notebooks/tennis-books-library.md
          - "Tennis Research Project": gemini-notebooks/tennis-research-project.md
          - "Tennis Forehand": gemini-notebooks/tennis-forehand.md
          - "Tennis Backhand": gemini-notebooks/tennis-backhand.md
          - "Serve & Return": gemini-notebooks/tennis-serve-return.md
          - "Volley Mastery": gemini-notebooks/tennis-volley.md
          - "Overhead & Lob": gemini-notebooks/tennis-overhead-lob.md
          - "5-Year Curriculum": gemini-notebooks/giao-trinh-5-nam.md
          - "Road to Pro": gemini-notebooks/road-to-pro.md
          - "ATP Coach Mastery": gemini-notebooks/atp-coach-mastery.md
          - "Fault-Tolerant Library": gemini-notebooks/fault-tolerant-library.md
          - "Cam Nay 2026 (Kình + Taichi)": gemini-notebooks/cam-nang-2026.md
          - "Tennis Specialty": gemini-notebooks/tennis-specialty.md
      - "Internal Arts, Health & TCM":
          - "Taichi-ChiGong Vault": gemini-notebooks/taichi-qigong.md
          - "TCM & Energy Medicine": gemini-notebooks/health-tcm-energy.md
          - "Tuổi 52: Tu Tập Nội Tại": gemini-notebooks/tuoi-52-tu-tap.md
      - "Mindset, Philosophy & Finance":
          - "Minimalism & Essentialism": gemini-notebooks/minimalism-essentialism.md
          - "Self-Help & Atomic Habits": gemini-notebooks/self-help.md
          - "Deliberate Practice": gemini-notebooks/coaching-deliberate-practice.md
          - "Psychology & Philosophy": gemini-notebooks/psychology-philosophy.md
          - "Thức Tỉnh & Tâm Linh": gemini-notebooks/hanh-trinh-thuc-tinh.md
      - "AI & Engineering":
          - "Hermes AI Use Cases": gemini-notebooks/hermes-ai-use-cases.md
          - "Metacognition in AI": gemini-notebooks/metacognition-ai.md
          - "Helpdesk 2026": gemini-notebooks/helpdesk-2026.md
          - "Geotech Instruments": gemini-notebooks/geotech-instruments.md
```

---

## Phase 3: Doc Content Template

Each new `.md` file follows this structure:

```markdown
# [Vault Title]

> **Vault ID**: `[cloud-id]` · **Sources**: [N] · **NotebookLM**: [Open ↗](https://notebooklm.google.com/notebook/[id])

## Research Scope

[2-3 sentences describing the vault's research focus from the table above]

## Key Themes

- Theme 1
- Theme 2
- Theme 3

## Grounded Insights

[3-5 bullet points synthesizing the most important findings from the vault]

## Studio Artifacts

| Artifact | Access |
|----------|--------|
| Audio Overview | [🔊 Play in Studio](https://notebooklm.google.com/notebook/[id]) |
| Video Overview | [🎬 Play in Studio](https://notebooklm.google.com/notebook/[id]) |
| Mind Map | [📖 Open Studio](https://notebooklm.google.com/notebook/[id]) |
| Slide Deck | [📖 Open Studio](https://notebooklm.google.com/notebook/[id]) |

## Connections to Tennis Knowledge Gap

- Connection 1
- Connection 2

## External References

- [Source 1](url)
- [Source 2](url)
```

---

## Phase 4: Deployment

1. Create all 19 missing `.md` files in `docs/gemini-notebooks/`
2. Update `mkdocs.yml` nav with new sections
3. Run `mkdocs build` from `D:\Github Repos\research-intranet\`
4. Verify at `http://localhost:8765/`
5. Deploy via `gh-pages` to GitHub Pages

---

## Deliverables Checklist

- [ ] 19 new markdown doc files created
- [ ] `mkdocs.yml` nav updated with all 32 vaults
- [ ] All existing docs verified (no broken links)
- [ ] `mkdocs build` succeeds with 0 errors
- [ ] Site verified at localhost:8765
- [ ] Deployed to GitHub Pages
