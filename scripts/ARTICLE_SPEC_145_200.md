# TENNISKB ARTICLE GENERATION SPEC — ARTICLES 145–200

You are writing ONE bilingual article pair (English + Vietnamese) for the TennisKB 200-Article Knowledge Base, deployed at tennis-unified.github.io.

## OUTPUT FILES (write BOTH, exact paths)
- EN: `D:\Github Repos\tennis-unified\en\articles_md\ART-{NUM:03d}.md`
- VI: `D:\Github Repos\tennis-unified\vi\articles\{VI_SLUG}\index.md`

Create the directory if missing. Pure UTF-8. LF newlines.

## REQUIRED STRUCTURE (both languages, 10 numbered sections exactly)

EN headers:
1. `## 1. Executive Summary & Athletic Intent`
2. `## 2. Biomechanical & Neurological Foundation` (use `### 2.1`, `### 2.2` … 5–7 subsections; include formulas in LaTeX `$...$` and code-block ASCII tables/diagrams)
3. `## 3. Step-by-Step Technical Execution` (numbered steps with timing windows)
4. `## 4. Performance Metrics & Dosage` (markdown table: Metric | Measurement | Club Target | Elite Target)
5. `## 5. Errors, Causes & Corrections` (markdown table: Observable Error | Root Cause | Consequence | Correction Protocol; 7–9 rows)
6. `## 6. Diagnostic Diagram` (ASCII art inside a fenced code block)
7. `## 7. Video Demonstration` (see VIDEO BLOCK below)
8. `## 8. Cross-Domain Synergy` (bullet list citing 10–15 related articles by number, e.g. "Article 081")
9. `## 9. Self-Assessment Matrix` (checkbox rubric table + scoring guide)
10. `## 10. Printable Practice Card` (drill card table: Block | Drill | Sets×Reps | Cue | Rest)

VI headers (MUST be exactly these, fully accented):
1. `## 1. Tóm Tắt Điều Hành & Ý Đồ Thể Thao`
2. `## 2. Nền Tảng Cơ Sinh Học & Thần Kinh Học`
3. `## 3. Trình Tự Thực Thi Kỹ Thuật (Checkpoints)`
4. `## 4. Chỉ Số Hiệu Suất & Liều Lượng Huấn Luyện`
5. `## 5. Lỗi Thường Gặp, Nguyên Nhân & Giao Thức Khắc Phục` (table columns: Lỗi Quan Sát Được | Nguyên Nhân Gốc Rễ | Hậu Quả | Giao Thức Khắc Phục)
6. `## 6. Sơ Đồ Chẩn Đoán & Ra Quyết Định`
7. `## 7. Video Minh Họa & Phân Tích Kỹ Thuật`
8. `## 8. Ứng Dụng Liên Ngành & Phối Hợp Đa Trụ Cột`
9. `## 9. Bảng Tự Đánh Giá (Rubric Đa Cấp Độ)`
10. `## 10. Thẻ Thực Hành In Sổ Tay (Pocket Drill Card)`

## VIETNAMESE RULES (HARD CONSTRAINTS)
- EVERY Vietnamese word must carry full, correct diacritics (UTF-8 NFC). Absolutely NO unaccented Vietnamese (no "Du Lieu", "Thong Ke", "Chien Thuat", etc.).
- ZERO English headers or sentences in the VI file. Proper nouns, technical English, and formulas may appear in parentheses after the Vietnamese term, e.g. `Chuỗi Động Lực Học (Kinetic Chain)`, `Tốc Độ Đầu Xoay (Rate of Force Development)`.
- Table headers, badges, section titles: Vietnamese only (English optional in parentheses).

## OPENING FORMAT
EN starts:
```
# Article {NUM}: {EN_TITLE}

> **PRO CUE:** {one punchy, expert coaching cue sentence}

## 1. Executive Summary & Athletic Intent
```
VI starts:
```
---
title: "Bài viết {NUM}: {VI_TITLE}"
description: "TennisKB — Bài viết {NUM}: {VI_TITLE} | Tennis Future Lab"
author: "Henry Pham"
date: 2025-01-15
lang: vi
pillar: "{PILLAR_SLUG}"
pillar_title: "{PILLAR_TITLE_VI}"
article_number: {NUM}
prev_article: "{PREV_VI_SLUG}"
next_article: "{NEXT_VI_SLUG}"
---

# Bài viết {NUM}: {VI_TITLE}

> **CUE CHUYÊN GIA:** {Vietnamese expert cue}

## 1. Tóm Tắt Điều Hành & Ý Đồ Thể Thao
```
(The frontmatter is REQUIRED on the VI file only.)

## VIDEO BLOCK (place right after the PRO CUE / CUE CHUYÊN GIA paragraph, before Section 1)
```html
<div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 8px; margin: 1.5rem 0;">
  <iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID_PLACEHOLDER" title="{article title}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>
```
(Leave the literal string VIDEO_ID_PLACEHOLDER. The deploy pipeline substitutes the real video.)

## QUALITY BAR
Match the depth of Article 001 (Ground Reaction Forces) and Article 144 (Equipment Optimization) in `D:\Github Repos\tennis-unified\en\articles_md\ART-144.md`:
- EN file: ≥ 22,000 bytes (~4,000–5,500 words)
- VI file: ≥ 22,000 bytes, faithful full translation (not summary) of the EN content
- Specific numbers everywhere (ms, °, cm, kg·cm², km/h, %, nmol/L, W/kg)
- LaTeX formulas (`$F_z$`, `$\tau = r \times F$`, `$\Delta v = J/m$`, …) rendered via MathJax
- ASCII diagnostic diagrams inside fenced code blocks
- Reference real research (e.g., Kovacs & Ellenbecker, Fleisig et al., Vickers, Fitts & Posner) where appropriate
- Cross-references cite article numbers that exist (001–200)

## WHEN DONE
Report exactly: `{ "num": {NUM}, "en_bytes": <size>, "vi_bytes": <size>, "status": "done" }`
