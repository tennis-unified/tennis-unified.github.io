---
title: Synthesis log
description: Append-only log of every gap analysis artifact produced.
---

# Synthesis log

Append-only log of every gap analysis artifact produced by the pipeline.
Updated each time a new gap report or web supplement is generated.

---

## Artifact index

| Artifact ID | Kind | Title | Date | Tier | Sources cited |
|-------------|------|-------|------|------|---------------------|
| gap-20260824-001 | whitepaper | Tennis Knowledge Gap Whitepaper | 2026-08-24 | all | 18 books + web |
| gap-20260824-002 | report | Tier 1 — Concrete high-value gaps | 2026-08-24 | T1 | 18 books + Kovacs/Ellenbecker + Paris 2024 |
| gap-20260824-003 | report | Tier 2 — Topic depth gaps | 2026-08-24 | T2 | 10 books + Talent Code web research |
| gap-20260824-004 | report | Tier 3 — Niche and specialty gaps | 2026-08-24 | T3 | 5+ |
| gap-20260824-005 | research | Modern tennis research 2024–2026 | 2026-08-24 | web | ITF, ATP, Wikipedia, peer-reviewed |
| gap-20260824-006 | research | Web-research technical content | 2026-08-24 | web | Cross, Kovacs/Ellenbecker, Coyle |
| gap-20260824-007 | research | Authoritative sources index | 2026-08-24 | web | ITF, ATP, Wikipedia, USPTA |
| gap-20260824-008 | library | Tennis Books Library (inline PDF reader) | 2026-08-24 | library | 34 books |

---

## Whitepaper

### gap-20260824-001 — Tennis Knowledge Gap Whitepaper (extended)

- **Path:** `docs/whitepapers/tennis-knowledge-gap-2026-08-24.md`
- **Confidence:** 0.85
- **Sources cited:** 18 books across 4 tier reports + 3 web-research supplements
- **Summary:** Single headline artifact ranking all 20 gaps and pairing
  each one with the source books that justify adding it to the repo.
  Extended with Kovacs/Ellenbecker 8-stage data and Cross & Lindsey 2013 aerodynamics.

---

## Reports

### gap-20260824-002 — Tier 1, Concrete high-value gaps (extended)

- **Path:** `docs/reports/tier-1-high-value-gaps.md`
- **Confidence:** 0.90
- **Tier:** 1
- **Gaps covered:** 11 (+ Kovacs/Ellenbecker as separate 1b entry)
- **Books cited:** 18
- **Highest-priority extractions:**
  1. Rod Cross double-pendulum (millisecond serve timings) — **extended with TWU model parameters**
  2. Kovacs/Ellenbecker 8-stage serve model — **NEW entry with measured EMG, joint angles, timing**
  3. Mehta aerodynamics (CD = 0.55–0.65, fuzz contribution)
  4. Cross kick-serve (sidespin-dominated, axis tilt)
  5. Marty Smith Future Strokes (Overlapping Dual Forehand, Reverse Serve, Volleyball Serve)

### gap-20260824-003 — Tier 2, Topic depth gaps (extended)

- **Path:** `docs/reports/tier-2-topic-depth-gaps.md`
- **Confidence:** 0.80
- **Tier:** 2
- **Gaps covered:** 8
- **Books cited:** 10
- **Web supplements:** Talent Code three-rule framework + myelin science

### gap-20260824-004 — Tier 3, Niche and specialty

- **Path:** `docs/reports/tier-3-niche-specialty.md`
- **Confidence:** 0.75
- **Tier:** 3
- **Gaps covered:** 5

---

## Web-research supplements

### gap-20260824-005 — Modern tennis research 2024–2026

- **Path:** `docs/research/modern-tennis-2024-2026.md`
- **Confidence:** 0.85 (player stats), 0.90 (rule changes), 0.70 (modern coaching consensus)
- **Sources:** Wikipedia, ITF official, ATP, Olympics.com, The Guardian, Marca, Reuters
- **Summary:** Alcaraz / Sinner / Sabalenka / Swiatek / Gauff profiles; ITF rule changes 2024–2026 (shot clock, Hawk-Eye Live, coaching); Paris 2024 wheelchair tennis full medal table

### gap-20260824-006 — Web-research technical content

- **Path:** `docs/https://tennis-unified.github.io/tnkbgap/research/web-research-summary/`
- **Confidence:** 0.90
- **Sources:** Cross (AJP 2011), Cross & Lindsey (Sports Engineering 2013), Kovacs & Ellenbecker (Sports Health 2011), Coyle (Bantam 2009)
- **Summary:** Cross double pendulum extended data, aerodynamics full source table, Kovacs 8-stage full joint angle/EMG table, Talent Code three-rule + myelin science

### gap-20260824-007 — Authoritative sources index

- **Path:** `docs/research/authoritative-sources.md`
- **Confidence:** 0.95
- **Sources:** ITF, ATP, WTA, USPTA, peer-reviewed journals, tennisplayer.net archive
- **Summary:** Standard tennis court dimensions; ITF Tennis 10s; ATP 2024 rulebook; ITF wheelchair classification; tennis biomechanics paper index

---

## Library

### gap-20260824-008 — Tennis Books Library (inline PDF reader)

- **Path:** `docs/books/index.md` + 34 individual book reader pages
- **Source:** 34 PDFs copied to `site/books/` for inline browser reading
- **Filter:** Domain tags + free-text search; works in all modern browsers
- **Reader:** Native browser PDF viewer via `<iframe>` (no PDF.js dependency)

---

## Skipped (with reasons)

| Source | Reason |
|--------|--------|
| `September-October-Tennis-Industry-Magazine.pdf` | skipped: advertising catalogue, no tennis content |
| `Tennis-Industrial_magazine.pdf` | skipped: advertising catalogue |
| `Tennis-Industry.pdf` | skipped: advertising catalogue |
| `10 Most common mistakes in Tennis Doubles and how to fix them!.mkv` | skipped: video format, not text-extractable |
| `1. Absolute tennis.docx/.pdf/_clean.md/_final_vi.md/_structured.md` (duplicates) | skipped: near-duplicate of `.pdf` canonical |
| `TEC_130_-_THE_SERVE_from_FTPTennis.docx/.epub` (duplicates) | skipped: near-duplicate |
| `Coaching_Tennis_Successfully.docx` etc. (when topic already in repo) | skipped: topic already well-covered |

---

*Trang web này được xây dựng với ❤️ cho cộng đồng quần vợt Việt Nam 🎾 by Henry Phạm*
