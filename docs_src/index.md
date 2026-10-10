---
title: Tennis Knowledge Gap Intranet
description: Pipeline that compares the Tennis-Unified intranet against the Tennis Books library and surfaces what is missing — with web-sourced modern context.
---

# Tennis Knowledge Gap Intranet

**One-time comparative sweep + continuously maintained reference.** Hermes scout extracted the Tennis Books library (476 books) and indexed every topic heading in [the Tennis-Unified intranet](https://tennis-unified.github.io/) (1,950 articles). Antigravity ran a 92-concept diff and surfaced **20 confirmed gaps** — topics the books cover deeply that the intranet either omits or touches only superficially. Modern web research (2024–2026 sources) supplements the book-side evidence.

This intranet mirrors that sweep so you can browse, cite, and revisit the findings without rerunning the analysis.

!!! note "Pipeline state — 2026-08-24"
    **1,950** repo articles scanned · **476** books indexed · **92** concepts searched · **20** gaps found · **30+** books readable in browser · **8** modern-web supplements

## 🌐 Tennis Unified Ecosystem & Main Library Links

This research and gap analysis portal directly connects with the **[Tennis Unified Library](https://tennis-unified.github.io/)** (1,300+ articles, 880+ videos, 38 world-class coaches).

<div class="grid cards" markdown>

- ### 🏛️ [Tennis Unified Library (Main Site)](https://tennis-unified.github.io/)

    ---

    The primary unified knowledge base featuring 17 comprehensive sections, 38 coach collections, and stroke video archives.

    [Explore Main Library →](https://tennis-unified.github.io/)

- ### 📖 [The Master Book: The Unified Court](book/index.md)

    ---

    Our 16-chapter master treatise on Newtonian physics, biotensegrity (*Chan Si Jin*), 8-stage serve, and stroke mechanics.

    [Read The Master Book →](book/index.md)

- ### 🎥 [Coach Video Library (38 Coaches)](https://tennis-unified.github.io/coach-video-library/)

    ---

    Video archives from world-class coaches (Fuorivia, Fedorov, Macci, Yandell, Bollettieri, Lansdorp, Mouratoglou).

    [Watch Coach Library →](https://tennis-unified.github.io/coach-video-library/)

- ### ⚡ [Stroke Analysis & Fundamentals](https://tennis-unified.github.io/stroke-analysis/)

    ---

    Over 490+ deep articles covering pro forehands, backhands, serves, volleys, footwork, and tactical development.

    [View Stroke Breakdowns →](https://tennis-unified.github.io/stroke-analysis/)

</div>

---

## Quick navigation

| I want to… | Where to go |
|------------|-------------|
| Explore the Main Knowledge Base | [Tennis Unified Main Site](https://tennis-unified.github.io/) · [Knowledge Intranet](https://tennis-unified.github.io/) |
| Read The Master Book (16 Chapters) | [The Unified Court Overview](book/index.md) · [Bản Tiếng Việt](vi/book/) |
| Read the headline gap analysis | [Tennis Knowledge Gap Whitepaper](whitepapers/tennis-knowledge-gap-2026-08-24.md) |
| Get a structured per-tier gap list | [Tier 1 — high-value gaps](reports/tier-1-high-value-gaps.md) · [Tier 2 — topic depth](reports/tier-2-topic-depth-gaps.md) · [Tier 3 — niche](reports/tier-3-niche-specialty.md) |
| Read a tennis book in the browser | [Tennis Books Library](books/) — 34 titles, PDF inline reader |
| Browse the source book extracts | [Raw tennis-book intel](raw-intel/index.md) |
| See modern (2024–2026) web context | [Modern tennis research 2024–2026](research/modern-tennis-2024-2026.md) |
| Check what's still pending | [Synthesis log](synthesis-log.md) |

---

## Latest synthesis

The main deliverable is the [Tennis Knowledge Gap whitepaper](whitepapers/tennis-knowledge-gap-2026-08-24.md), which ranks the 20 gaps into three tiers and pairs each one with the source books that justify including it in the repo.

Supporting reports:

- [Tier 1 — concrete high-value gaps](reports/tier-1-high-value-gaps.md) — Rod Cross double pendulum, Mehta aerodynamics, kick serve physics, Marty Smith Future Strokes, plantar fasciitis, HIIT protocols, Westside Conjugate, the yips as focal dystonia, wheelchair tennis
- [Tier 2 — topic depth gaps](reports/tier-2-topic-depth-gaps.md) — German Tennis Federation annual plan, ITF Level 2 curriculum, Vic Braden 50-50-50, Oscar Wegner "simplify the stroke", Tao/Zen/Soft Science mental traditions, Daniel Coyle deep-practice rules, Chasing Points diary, Greg Rusedski 240 km/h serve
- [Tier 3 — niche / specialty](reports/tier-3-niche-specialty.md) — real tennis, rough/smooth, ITF Tennis 10s ball progression, open-skill sport pedagogy (Wayne Elderton), Open Era timeline

---

## Tennis Books Library (read in browser)

Browse **34 curated tennis books** with the inline PDF reader — no separate reader needed.

[Open the Books Library →](books/)

Highlights:

- **Biomechanics** — Rod Cross double pendulum, Mehta aerodynamics, Kovacs/Ellenbecker 8-stage serve, biomechanics of tennis groundstrokes
- **Serve** — 8-stage serve model, physics of the kick serve, anatomy of the modern tennis shot
- **Equipment** — Sweet Spot physics, Kotze racket-in-serves research
- **Strokes** — Absolute Tennis (Marty Smith Future Strokes), Hi-Tech Tennis, USPTA footwork, USTA Federer forehands
- **Mental game** — Winning Ugly (Brad Gilbert), Vic Braden 50-50-50, Tao of Tennis, Soft Science of Tennis, Vision Skills
- **Training** — HIIT (Laursen & Buchheit), Westside Conjugate (Louie Simmons), Tennis Workbook
- **Medical** — Aspetar Journals 2023/2024/2025 (wheelchair tennis, yips), plantar fasciitis, sports medicine handbook

---

## Modern tennis research 2024–2026 (web supplements)

Supplement the book-side evidence with current web research:

- [Modern tennis research 2024–2026](research/modern-tennis-2024-2026.md) — Alcaraz/Sinner/Sabalenka profiles, ITF rules changes, Hawk-Eye Live rollout, modern coaching consensus
- [Web-sourced technical content](https://tennis-unified.github.io/tnkbgap/research/web-research-summary/) — Rod Cross extended research, Kovacs/Ellenbecker 8-stage, kinetic chain data
- [Authoritative sources index](research/authoritative-sources.md) — tennisplayer.net archive, Wikipedia tennis, ITF coaching references

---

## Browse the pipeline

- [Digest queue](digest.md) — full Tennis Books inventory grouped by gap-analysis status
- [Synthesis log](synthesis-log.md) — append-only log of completed artifacts
- [Raw tennis-book intel](raw-intel/index.md) — every captured source file, viewable as-is with extracted text

---

## How the pipeline works

```
┌────────────────────┐
│ 1. Hermes scout    │  walks D:/New Tennis Knowledge/Tennis Books/
│                    │  extracts TOC + first 5 pages of each book
└──────────┬─────────┘
           ▼
┌────────────────────┐
│ 2. Topic inventory │  walks [the Tennis-Unified intranet](https://tennis-unified.github.io/) at `D:/New Tennis Knowledge/Tennis Knowledge/Tennis-Unified/TP-Archive-Site/` │
│                    │  builds 10,945-line heading index
└──────────┬─────────┘
           ▼
┌────────────────────┐
│ 3. Antigravity     │  92-concept diff → 20 gaps with book citations
│    synthesis       │  sorted into Tier 1 / Tier 2 / Tier 3
└──────────┬─────────┘
           ▼
┌────────────────────┐
│ 4. Web supplement  │  2024–2026 authoritative sources cross-reference
│                    │  (Wikipedia, ITF, ATP, sports journals, YouTube)
└──────────┬─────────┘
           ▼
┌────────────────────┐
│ 5. This intranet   │  mirrors books, raw intel, gap reports, web context
└────────────────────┘
```

---

## Conventions

- **Raw intel** is the book-side evidence. Each entry carries the source filename, the topic it was extracted under, and a short passage.
- **Gap reports** are the deliverables. Every gap cites back to the raw-intel entries that justify it.
- **Web supplements** add 2024–2026 authoritative context (rules changes, player stats, modern coaching consensus).
- **Skipped** books are recorded with a reason (off-topic, vendor magazine, schedule handout) so the analysis is reproducible.

---

*Trang web này được xây dựng với ❤️ cho cộng đồng quần vợt Việt Nam 🎾 by Henry Phạm*
