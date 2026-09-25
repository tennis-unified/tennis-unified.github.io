# -*- coding: utf-8 -*-
"""
Generator for TennisKB bilingual articles 145-200.

Writes:
  EN: D:\\Github Repos\\tennis-unified\\en\\articles_md\\ART-{NNN}.md
  VI: D:\\Github Repos\\tennis-unified\\vi\\articles\\{VI_SLUG}\\index.md

Deterministic composition from per-article knowledge data (gen145_200_data_*.py)
plus pillar archetype pools (gen145_200_pools_en.py / _vi.py).
"""
import json
import os
import re
import sys
import html
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE = Path(r"D:\Github Repos\tennis-unified")
SCRIPTS = BASE / "scripts"

from gen145_200_pools_en import EN_POOL          # noqa: E402
from gen145_200_pools_vi import VI_POOL          # noqa: E402

DATA = {}
for mod_name in ("gen145_200_data_a", "gen145_200_data_b", "gen145_200_data_c",
                 "gen145_200_data_d", "gen145_200_data_e", "gen145_200_data_f",
                 "gen145_200_data_g", "gen145_200_data_h", "gen145_200_data_i",
                 "gen145_200_data_j"):
    try:
        mod = __import__(mod_name)
        DATA.update(mod.DATA)
    except ImportError as exc:
        print(f"[warn] data module unavailable: {mod_name} ({exc})")

with open(SCRIPTS / "articles_145_200_meta.json", encoding="utf-8") as f:
    META = json.load(f)

with open(SCRIPTS / "articles_200_data.json", encoding="utf-8") as f:
    CAT = json.load(f)

VIDEO_BLOCK = """<div class="video-container" style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; border-radius: 8px; margin: 1.5rem 0;">
  <iframe src="https://www.youtube-nocookie.com/embed/VIDEO_ID_PLACEHOLDER" title="{title}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
</div>"""

VN_DIACRITICS = set(
    "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ"
    "ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐ"
)


# ---------------------------------------------------------------- utilities
def rot(pool, num, k=0):
    return pool[(num + k) % len(pool)]


def first_sentence(text):
    text = re.sub(r"[*_`]", "", text).strip()
    m = re.split(r"(?<=[.!?])\s", text)
    return m[0] if m else text


def shape(data, lang):
    """Normalise steps/errs/drills to the layout each builder consumes.

    lang 0 = EN view, lang 1 = VI view.
    Accepted input layouts:
      pairs:  4 x [name, detail]  -> first two EN, last two VI
      pairs:  2 x [en_name, en_detail, vi_name, vi_detail]
      errs:   2 x [err,cause,cons,fix, err_vi,cause_vi,cons_vi,fix_vi]
      errs:   2 x [err,cause,fix, err_vi,cause_vi,fix_vi]
    """
    def pairs(items):
        if len(items) == 4 and len(items[0]) == 2:
            return items[:2], items[2:]
        if len(items) == 2 and len(items[0]) == 4:
            en = [[items[0][0], items[0][1]], [items[1][0], items[1][1]]]
            vi = [[items[0][2], items[0][3]], [items[1][2], items[1][3]]]
            return en, vi
        raise ValueError("unrecognised pair layout")

    def errs(items):
        en, vi = [], []
        for e in items:
            if len(e) >= 8:
                en.append(list(e[0:4]))
                vi.append(list(e[4:8]))
            elif len(e) == 6:
                en.append([e[0], e[1], "", e[2]])
                vi.append([e[3], e[4], "", e[5]])
            else:
                raise ValueError("unrecognised error layout")
        return en, vi

    en_steps, vi_steps = pairs(data["steps"])
    en_errs, vi_errs = errs(data["errs"])
    en_drills, vi_drills = pairs(data["drills"])
    if lang == 0:
        return en_steps, en_errs, en_drills
    return vi_steps, vi_errs, vi_drills


def wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= width:
            cur += " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def box(title, items, width=74):
    inner = width - 4
    out = ["┌" + "─" * (width - 2) + "┐"]
    for ln in wrap(title, inner):
        out.append("│ " + ln.ljust(inner) + " │")
    out.append("├" + "─" * (width - 2) + "┤")
    for it in items:
        for i, ln in enumerate(wrap(it, inner - 2)):
            prefix = "├─ " if i == 0 else "│  "
            out.append("│ " + (prefix + ln).ljust(inner) + " │")
    out.append("└" + "─" * (width - 2) + "┘")
    return "\n".join(out)


def clean_title(t):
    t = html.unescape(t)
    return t.strip()


def strip_prefix_title(t, num):
    t = clean_title(t)
    return re.sub(r"^\s*Bài\s*viết\s*%d\s*[:：]\s*" % num, "", t, flags=re.IGNORECASE)


def related_numbers(num, pillar_slug):
    """Deterministic cross-reference set: neighbours + pillar kin + foundations."""
    out = []
    for off in (1, -1, 2, -2, 3, -3, 5, -5, 8, -8):
        n = num + off
        if 1 <= n <= 200:
            out.append(n)
    kin = [1, 12, 24, 40, 68, 96, 121, 144, 160, 161, 200]
    for k in kin:
        if k != num and k not in out:
            out.append(k)
    # order: neighbours first then kin, de-duplicated, max 14
    seen, final = set(), []
    for n in out:
        if n not in seen:
            seen.add(n)
            final.append(n)
    return final[:14]


REASON_EN = [
    "establishes the anatomical constraint that limits how much of this pattern can be loaded in one session",
    "supplies the measurement protocol used to verify the targets in Section 4",
    "documents the failure mode that most often mimics a technical error here",
    "provides the recovery window logic that determines the spacing of these blocks",
    "defines the force-time signature this pattern ultimately depends on",
    "covers the perceptual cue that shortens recognition latency in this situation",
    "details the load progression rule that keeps this adaptation from stalling",
    "explains the score-state context in which this pattern changes value",
]
REASON_VI = [
    "thiết lập ràng buộc giải phẫu giới hạn khối lượng có thể nạp cho mẫu này trong một buổi tập",
    "cung cấp phác đồ đo lường dùng để kiểm chứng các mục tiêu ở Mục 4",
    "ghi nhận kiểu thất bại thường bị nhầm với lỗi kỹ thuật ở đây",
    "đưa ra logic cửa sổ phục hồi quyết định khoảng cách giữa các khối tập này",
    "định nghĩa dấu hiệu lực - thời gian mà mẫu này cuối cùng phụ thuộc vào",
    "trình bày tín hiệu tri giác giúp rút ngắn độ trễ nhận diện trong tình huống này",
    "chi tiết quy tắc tăng tiến tải giúp thích nghi này không bị đình trệ",
    "giải thích bối cảnh trạng thái tỷ số làm thay đổi giá trị của mẫu này",
]


def en_title_of(n):
    return clean_title(CAT["en"][n - 1]["title"])


def vi_title_of(n):
    return strip_prefix_title(CAT["vi"][n - 1]["title"], n)


def cue_en(pillar, topic):
    if pillar == "tactics":
        return (f"**{topic.title()}** = a **decision architecture**, not a preference - scan, classify, "
                f"commit, execute, recover, audit. Declare the target before the ball arrives; never let the "
                f"ball decide for you.")
    return (f"**{topic.title()}** = a **dose-response contract** with recovery in the denominator - train the "
            f"qualities the match actually demands, at a load the tissues can absorb, and verify with markers "
            f"rather than with feelings.")


def cue_vi(pillar, topic):
    if pillar == "tactics":
        return (f"**{topic}** = một **kiến trúc quyết định**, không phải sở thích - quét, phân loại, cam kết, "
                f"thực thi, hồi phục, kiểm toán. Tuyên bố mục tiêu trước khi bóng tới; đừng bao giờ để quả bóng "
                f"quyết định thay bạn.")
    return (f"**{topic}** = một **hợp đồng liều - đáp ứng** với phục hồi ở mẫu số - hãy huấn luyện đúng phẩm chất "
            f"mà trận đấu thực sự đòi hỏi, ở mức tải mà mô có thể hấp thụ, và kiểm chứng bằng chỉ số thay vì "
            f"bằng cảm giác.")


# ---------------------------------------------------------------- EN builder
def build_en(num, meta, data):
    pillar = meta["pillar_slug"]
    pool = EN_POOL[pillar]
    topic = data["topic_en"]
    title = clean_title(meta["title_en"])
    subs_u = data["subs"]          # 2 x [title, vi_title, en_body, vi_body]
    steps_u, errs_u, drills_u = shape(data, 0)
    varrow = data["vars"]          # 3 x [en_name, vi_name, value]

    L = []
    A = L.append
    A(f"# Article {num}: {title}")
    A("")
    A(f"> **PRO CUE:** {cue_en(pillar, topic)}")
    A("")
    A(VIDEO_BLOCK.format(title=html.escape(title)))
    A("")

    # ---------------- Section 1
    A("## 1. Executive Summary & Athletic Intent")
    A("")
    A(data["mech_en"])
    A("")
    A(rot(pool["intent"], num, 0))
    A("")
    A(rot(pool["intent"], num, 1))
    A("")
    A(f"This article establishes the complete **{topic.title()} framework**:")
    A("")
    A(f"1. **{subs_u[0][0]}** - {first_sentence(subs_u[0][2])}")
    A(f"2. **{subs_u[1][0]}** - {first_sentence(subs_u[1][2])}")
    A(f"3. **{rot(pool['sub'], num, 0)[0]}** - {first_sentence(rot(pool['sub'], num, 0)[1])}")
    A(f"4. **{rot(pool['sub'], num, 1)[0]}** - {first_sentence(rot(pool['sub'], num, 1)[1])}")
    A(f"5. **Quantified Targets & Dosage Architecture** - the measurable indicators, tolerable weekly dose, "
      f"and the monitoring markers that decide whether the block continues, holds, or deloads.")
    A(f"6. **Error Taxonomy & Diagnostic Logic** - the observable failure patterns, their root causes, and the "
      f"explicit decision tree used to select the correction.")
    A("")
    A("The athletic intent is threefold:")
    A("")
    A(f"- First, convert **{topic}** from an intuitive, mood-dependent behaviour into a **repeatable protocol** "
      f"with declared inputs, measurable outputs, and a defined failure mode.")
    A(f"- Second, make the **limiting factors explicit**. The variables that actually cap performance here are "
      f"{varrow[0][0]}, {varrow[1][0]}, and {varrow[2][0]}; everything else is secondary until those are controlled.")
    A(f"- Third, provide a **complete operational toolkit**: assessment, execution sequencing, dosage, error "
      f"correction, and a printable card that can be used in the next session without further interpretation.")
    A("")
    A("---")
    A("")

    # ---------------- Section 2
    A("## 2. Biomechanical & Neurological Foundation")
    A("")
    A(f"### 2.1 {subs_u[0][0]}")
    A("")
    A(subs_u[0][2])
    A("")
    for i in range(3):
        A(f"- **{varrow[i][0]}** measured at **{varrow[i][2]}** is the operational expression of this principle "
          f"in the current model.")
    A(f"- The interaction between these variables is non-linear: improving one beyond its usable range without "
      f"the others transfers the load to a weaker link rather than raising output.")
    A("")
    A(f"### 2.2 {subs_u[1][0]}")
    A("")
    A(subs_u[1][2])
    A("")
    A(f"- Target range for **{varrow[0][0]}**: {varrow[0][2]} under controlled conditions, degrading by a "
      f"measurable margin under fatigue.")
    A(f"- Target range for **{varrow[1][0]}**: {varrow[1][2]}, verified at least twice per mesocycle.")
    A(f"- Target range for **{varrow[2][0]}**: {varrow[2][2]}, tracked with the same protocol each time.")
    A("")

    for idx, k in enumerate((0, 1, 2), start=3):
        st, body, bullets = rot(pool["sub"], num, k)
        A(f"### 2.{idx} {st}")
        A("")
        A(body)
        A("")
        for b in bullets:
            A(f"- {b}")
        A("")

    A("### 2.6 Quantitative Model & Key Relationships")
    A("")
    A("The governing relationships can be written explicitly, which is what makes the targets auditable rather "
      "than rhetorical:")
    A("")
    A("```")
    A(box(f"QUANTITATIVE MODEL - {topic.upper()}", [
        f"1. {varrow[0][0]} = {varrow[0][2]}  (primary controllable input)",
        f"2. {varrow[1][0]} = {varrow[1][2]}  (secondary transfer variable)",
        f"3. {varrow[2][0]} = {varrow[2][2]}  (verification marker)",
        "4. Output = f(technical quality x available capacity) / fatigue cost",
        "5. Load tolerance is bounded by the slowest-adapting tissue, not the strongest muscle",
    ]))
    A("```")
    A("")
    A("In mathematical form, the three relationships that matter most for this pattern are:")
    A("")
    A(r"- Transfer of force through the system: $F_{out} = \eta \cdot F_{in}$, where $\eta$ is the efficiency "
      r"of the segmental chain and falls sharply when any intermediate segment leaks position.")
    A(r"- Rate of force development: $RFD = \Delta F / \Delta t$, which governs whether the pattern is available "
      r"inside the available time window rather than merely in a laboratory setting.")
    A(r"- Impulse requirement: $J = \int F\,dt = m \cdot \Delta v$, so shortening the time window demands a "
      r"disproportionately larger peak force for the same change in velocity.")
    A(r"- Load-response relationship: $Adaptation = k \cdot \frac{Stimulus}{Fatigue + Recovery\ deficit}$, which "
      r"is why adding stimulus without controlling the denominator fails.")
    A("")
    A("---")
    A("")

    # ---------------- Section 3
    A("## 3. Step-by-Step Technical Execution")
    A("")
    A(f"The following sequence is executed in order. Timing windows assume a competitive tempo; the ordering "
      f"matters more than the absolute values, because each step supplies the input the next one requires.")
    A("")
    A(f"1. **{steps_u[0][0]}** - {steps_u[0][1]}")
    A(f"2. **{steps_u[1][0]}** - {steps_u[1][1]}")
    n = 3
    for k in range(6):
        name, timing, detail = rot(pool["step"], num, k)
        A(f"{n}. **{name}** ({timing}) - {detail}")
        n += 1
    A("")
    A("Checkpoint verification table:")
    A("")
    A("| Checkpoint | Pass | Leak |")
    A("| --- | --- | --- |")
    for k in range(5):
        name, timing, detail = rot(pool["step"], num, k)
        A(f"| {name} | {first_sentence(detail)} | Late or partial execution transfers load to the next segment |")
    A("")
    A("---")
    A("")

    # ---------------- Section 4
    A("## 4. Performance Metrics & Dosage")
    A("")
    A("| Metric | Measurement | Club Target | Elite Target |")
    A("| --- | --- | --- | --- |")
    for i in range(3):
        A(f"| {varrow[i][0]} | Direct measurement, same protocol each time | {varrow[i][2]} | "
          f"{varrow[i][2]} sustained under fatigue |")
    for k in range(7):
        m, meas, club, elite = rot(pool["metric"], num, k)
        A(f"| {m} | {meas} | {club} | {elite} |")
    A("")
    for k in range(2):
        A(rot(pool["dosage"], num, k))
        A("")
    A("Block structure and dose distribution:")
    A("")
    A("| Block | Objective | Dose | Tracking Metric |")
    A("| --- | --- | --- | --- |")
    for k in range(5):
        name, timing, detail = rot(pool["step"], num, k + 2)
        m, meas, club, elite = rot(pool["metric"], num, k)
        A(f"| {name} | {first_sentence(detail)} | 2-3 exposures weekly, 20-40 min | {m} ({club}) |")
    A("")
    A("---")
    A("")

    # ---------------- Section 5
    A("## 5. Errors, Causes & Corrections")
    A("")
    A("| Observable Error | Root Cause | Consequence | Correction Protocol |")
    A("| --- | --- | --- | --- |")
    for e in errs_u:
        A(f"| {e[0]} | {e[1]} | {e[2]} | {e[3]} |")
    for k in range(6):
        e, c, cons, fix = rot(pool["error"], num, k)
        A(f"| {e} | {c} | {cons} | {fix} |")
    A("")
    A(f"Correction priority order: first restore **{varrow[0][0]}** to its target range, then re-verify "
      f"**{varrow[1][0]}**; only then progress the load. Attempting to correct an execution error while the "
      f"underlying capacity is out of range produces temporary fixes that fail under competitive pressure.")
    A("")
    A("---")
    A("")

    # ---------------- Section 6
    A("## 6. Diagnostic Diagram")
    A("")
    A("```")
    A(box(f"DIAGNOSTIC ENTRY - {topic.upper()}", [
        f"INPUT A: {varrow[0][0]} = {varrow[0][2]}",
        f"INPUT B: {varrow[1][0]} = {varrow[1][2]}",
        f"INPUT C: {varrow[2][0]} = {varrow[2][2]}",
    ]))
    A("")
    A("                    |")
    A("        ┌───────────┴────────────┐")
    A(f"        │ {wrap(varrow[0][0] + ' in range?', 24)[0]:<24} │")
    A("        └───┬────────────────┬───┘")
    A("       YES  │                │  NO")
    A("   ┌────────▼────────┐  ┌────▼─────────────┐")
    A("   │ progress load   │  │ hold load,       │")
    A("   │ +5-10% weekly   │  │ correct capacity │")
    A("   └────────┬────────┘  └────┬─────────────┘")
    A("            │                │")
    A("   ┌────────▼────────────────▼─────────┐")
    A("   │  re-test after 7-10 days          │")
    A("   │  compare against Section 4 targets│")
    A("   └───────────────────────────────────┘")
    A("```")
    A("")
    A("Decision rules that follow from the diagram:")
    A("")
    for k in range(4):
        A(f"- {rot(pool['decision'], num, k)}")
    A("")
    A("---")
    A("")

    # ---------------- Section 7
    A("## 7. Video Demonstration")
    A("")
    A("The reference demonstration for this pattern is embedded at the top of the article. Review it "
      "against the checkpoints in Section 3 before progressing load.")
    A("")
    A("Analysis focus while reviewing the footage:")
    A("")
    for k in range(6):
        A(f"- {rot(pool['video'], num, k)}")
    A("")
    A(f"Watch specifically for the moment where **{varrow[0][0]}** departs from {varrow[0][2]} - in almost every "
      f"case the deviation appears before the visible technical defect, not after it.")
    A("")
    A("---")
    A("")

    # ---------------- Section 8
    A("## 8. Cross-Domain Synergy")
    A("")
    A("This pattern does not exist in isolation; the following articles supply the constraints it depends on:")
    A("")
    for i, rn in enumerate(related_numbers(num, pillar)):
        A(f"- **Article {rn:03d} - {en_title_of(rn)}**: {rot(REASON_EN, num + i, 0)}.")
    A("")
    A(f"Read together with these, {topic} becomes a **node in a system** rather than an isolated drill: the "
      f"biomechanical constraint, the perceptual cue, the loading rule, and the score-state value all have to be "
      f"correct simultaneously for the pattern to survive competitive pressure.")
    A("")
    A("---")
    A("")

    # ---------------- Section 9
    A("## 9. Self-Assessment Matrix")
    A("")
    A("| Criterion | Level 1 (Basic) | Level 2 (Transitional) | Level 3 (Functional) | Level 4 (Elite) |")
    A("| --- | --- | --- | --- | --- |")
    for k in range(6):
        crit, l1, l2, l3, l4 = rot(pool["rubric"], num, k)
        A(f"| {crit} | {l1} | {l2} | {l3} | {l4} |")
    A("")
    A("Scoring guide: score each row 1-4, sum across six rows (maximum 24).")
    A("")
    A("- **6-11**: foundation phase. Reduce load, restore the primary variables, and re-test in two weeks.")
    A("- **12-17**: functional phase. Progress load at 5-10% weekly with one deload week in three.")
    A("- **18-21**: competitive phase. Shift emphasis from capacity to execution under fatigue and pressure.")
    A("- **22-24**: maintenance. Hold the dose, audit quarterly, and reinvest time in tactical application.")
    A("")
    A("---")
    A("")

    # ---------------- Section 10
    A("## 10. Printable Practice Card")
    A("")
    A("| Block | Drill | Sets x Reps | Cue | Rest |")
    A("| --- | --- | --- | --- | --- |")
    A(f"| A - Primary | {drills_u[0][0]} | 4 x 8 | {drills_u[0][1]} | 60 s |")
    A(f"| B - Secondary | {drills_u[1][0]} | 3 x 10 | {drills_u[1][1]} | 60 s |")
    for k in range(4):
        blk, dr, sets, cue, rest = rot(pool["drill"], num, k)
        A(f"| {blk} | {dr} | {sets} | {cue} | {rest} |")
    A("")
    A("Progression notes:")
    A("")
    for k in range(3):
        A(f"- {rot(pool['progression'], num, k)}")
    A("")
    A(f"Session-level rule: never leave the session with **{varrow[0][0]}** outside its target range by more "
      f"than one progression step; the pattern you rehearse while out of range is the pattern you will reproduce "
      f"under pressure.")
    A("")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- VI builder
def build_vi(num, meta, data):
    pillar = meta["pillar_slug"]
    pool = VI_POOL[pillar]
    topic = data["topic_vi"]
    vi_title = strip_prefix_title(meta["title_vi"], num)
    subs_u = data["subs"]
    steps_u, errs_u, drills_u = shape(data, 1)
    varrow = data["vars"]

    cat_vi = CAT["vi"][num - 1]
    pillar_slug_vi = cat_vi.get("pillar_slug", pillar)

    L = []
    A = L.append
    A("---")
    A(f'title: "Bài viết {num}: {vi_title}"')
    A(f'description: "TennisKB - Bài viết {num}: {vi_title} | Tennis Future Lab"')
    A('author: "Henry Pham"')
    A("date: 2025-01-15")
    A("lang: vi")
    A(f'pillar: "{pillar_slug_vi}"')
    A(f'pillar_title: "{clean_title(cat_vi.get("pillar_title", ""))}"')
    A(f"article_number: {num}")
    A(f'prev_article: "{meta.get("prev_vi", "")}"')
    A(f'next_article: "{meta.get("next_vi", "")}"')
    A("---")
    A("")
    A(f"# Bài viết {num}: {vi_title}")
    A("")
    A(f"> **CUE CHUYÊN GIA:** {cue_vi(pillar, topic)}")
    A("")
    A(VIDEO_BLOCK.format(title=html.escape(vi_title)))
    A("")

    # ---------------- Mục 1
    A("## 1. Tóm Tắt Điều Hành & Ý Đồ Thể Thao")
    A("")
    A(data["mech_vi"])
    A("")
    A(rot(pool["intent"], num, 0))
    A("")
    A(rot(pool["intent"], num, 1))
    A("")
    A(f"Bài viết này thiết lập **khung {topic} hoàn chỉnh**:")
    A("")
    A(f"1. **{subs_u[0][1]}** - {first_sentence(subs_u[0][3])}")
    A(f"2. **{subs_u[1][1]}** - {first_sentence(subs_u[1][3])}")
    A(f"3. **{rot(pool['sub'], num, 0)[0]}** - {first_sentence(rot(pool['sub'], num, 0)[1])}")
    A(f"4. **{rot(pool['sub'], num, 1)[0]}** - {first_sentence(rot(pool['sub'], num, 1)[1])}")
    A("5. **Kiến Trúc Mục Tiêu Định Lượng & Liều Lượng** - các chỉ số đo lường được, liều lượng tuần có thể "
      "hấp thụ, và các dấu hiệu theo dõi quyết định khối tập tiếp tục, giữ nguyên, hay giảm tải.")
    A("6. **Phân Loại Lỗi & Logic Chẩn Đoán** - các kiểu thất bại quan sát được, nguyên nhân gốc rễ, và cây "
      "quyết định tường minh dùng để chọn giao thức khắc phục.")
    A("")
    A("Ý đồ thể thao gồm ba tầng:")
    A("")
    A(f"- Thứ nhất, chuyển **{topic}** từ một hành vi dựa trên trực giác và cảm xúc thành một **phác đồ lặp "
      f"lại được**, với đầu vào được tuyên bố, đầu ra đo lường được, và kiểu thất bại được định nghĩa.")
    A(f"- Thứ hai, làm cho **các yếu tố giới hạn trở nên tường minh**. Những biến thực sự giới hạn hiệu suất ở "
      f"đây là {varrow[0][1]}, {varrow[1][1]} và {varrow[2][1]}; mọi thứ khác chỉ là thứ yếu cho tới khi ba biến "
      f"này được kiểm soát.")
    A("- Thứ ba, cung cấp **bộ công cụ vận hành đầy đủ**: đánh giá, trình tự thực thi, liều lượng, khắc phục "
      "lỗi, và một thẻ in được dùng ngay trong buổi tập kế tiếp mà không cần diễn giải thêm.")
    A("")
    A("---")
    A("")

    # ---------------- Mục 2
    A("## 2. Nền Tảng Cơ Sinh Học & Thần Kinh Học")
    A("")
    A(f"### 2.1 {subs_u[0][1]}")
    A("")
    A(subs_u[0][3])
    A("")
    for i in range(3):
        A(f"- **{varrow[i][1]}** đo ở mức **{varrow[i][2]}** là biểu hiện vận hành của nguyên lý này trong mô "
          f"hình hiện tại.")
    A("- Tương tác giữa các biến này là phi tuyến: cải thiện một biến vượt khỏi dải sử dụng của nó mà không "
      "kèm các biến còn lại sẽ chuyển tải sang mắt xích yếu hơn thay vì nâng đầu ra.")
    A("")
    A(f"### 2.2 {subs_u[1][1]}")
    A("")
    A(subs_u[1][3])
    A("")
    A(f"- Dải mục tiêu cho **{varrow[0][1]}**: {varrow[0][2]} trong điều kiện kiểm soát, suy giảm một mức đo "
      f"được khi mệt.")
    A(f"- Dải mục tiêu cho **{varrow[1][1]}**: {varrow[1][2]}, kiểm chứng ít nhất hai lần mỗi trung chu kỳ.")
    A(f"- Dải mục tiêu cho **{varrow[2][1]}**: {varrow[2][2]}, theo dõi bằng cùng một phác đồ mỗi lần.")
    A("")

    for idx, k in enumerate((0, 1, 2), start=3):
        st, body, bullets = rot(pool["sub"], num, k)
        A(f"### 2.{idx} {st}")
        A("")
        A(body)
        A("")
        for b in bullets:
            A(f"- {b}")
        A("")

    A("### 2.6 Mô Hình Định Lượng & Các Quan Hệ Then Chốt")
    A("")
    A("Các quan hệ chi phối có thể được viết tường minh, và chính điều đó làm cho các mục tiêu trở nên kiểm "
      "toán được thay vì chỉ mang tính hùng biện:")
    A("")
    A("```")
    A(box(f"MÔ HÌNH ĐỊNH LƯỢNG - {topic.upper()}", [
        f"1. {varrow[0][1]} = {varrow[0][2]}  (đầu vào kiểm soát được chính)",
        f"2. {varrow[1][1]} = {varrow[1][2]}  (biến chuyển giao thứ cấp)",
        f"3. {varrow[2][1]} = {varrow[2][2]}  (dấu hiệu kiểm chứng)",
        "4. Đầu ra = f(chất lượng kỹ thuật x năng lực khả dụng) / chi phí mệt mỏi",
        "5. Ngưỡng chịu tải bị giới hạn bởi mô thích nghi chậm nhất, không phải cơ mạnh nhất",
    ]))
    A("```")
    A("")
    A("Dưới dạng toán học, ba quan hệ quan trọng nhất cho mẫu này là:")
    A("")
    A(r"- Truyền lực qua hệ thống: $F_{out} = \eta \cdot F_{in}$, trong đó $\eta$ là hiệu suất của chuỗi "
      r"phân đoạn và giảm mạnh khi bất kỳ phân đoạn trung gian nào rò rỉ vị thế.")
    A(r"- Tốc độ phát triển lực: $RFD = \Delta F / \Delta t$, quyết định mẫu có khả dụng trong cửa sổ thời gian "
      r"cho phép hay chỉ trong điều kiện phòng thí nghiệm.")
    A(r"- Yêu cầu xung lực: $J = \int F\,dt = m \cdot \Delta v$, nên rút ngắn cửa sổ thời gian đòi hỏi lực đỉnh "
      r"lớn hơn một cách bất tương xứng cho cùng mức thay đổi vận tốc.")
    A(r"- Quan hệ tải - đáp ứng: $Thích\ nghi = k \cdot \frac{Kích\ thích}{Mệt\ mỏi + Thiếu\ hụt\ phục\ hồi}$, đó "
      r"là lý do vì sao thêm kích thích mà không kiểm soát mẫu số sẽ thất bại.")
    A("")
    A("---")
    A("")

    # ---------------- Mục 3
    A("## 3. Trình Tự Thực Thi Kỹ Thuật (Checkpoints)")
    A("")
    A("Trình tự sau được thực hiện theo đúng thứ tự. Các cửa sổ thời gian giả định nhịp độ thi đấu; thứ tự "
      "quan trọng hơn giá trị tuyệt đối, bởi mỗi bước cung cấp đầu vào mà bước kế tiếp cần.")
    A("")
    A(f"1. **{steps_u[0][0]}** - {steps_u[0][1]}")
    A(f"2. **{steps_u[1][0]}** - {steps_u[1][1]}")
    n = 3
    for k in range(6):
        name, timing, detail = rot(pool["step"], num, k)
        A(f"{n}. **{name}** ({timing}) - {detail}")
        n += 1
    A("")
    A("Bảng kiểm chứng điểm kiểm tra:")
    A("")
    A("| Điểm Kiểm Tra | Đạt Chuẩn | Rò Rỉ Động Lực |")
    A("| --- | --- | --- |")
    for k in range(5):
        name, timing, detail = rot(pool["step"], num, k)
        A(f"| {name} | {first_sentence(detail)} | Thực thi muộn hoặc không trọn vẹn sẽ chuyển tải sang phân "
          f"đoạn kế tiếp |")
    A("")
    A("---")
    A("")

    # ---------------- Mục 4
    A("## 4. Chỉ Số Hiệu Suất & Liều Lượng Huấn Luyện")
    A("")
    A("| Chỉ Số | Cách Đo | Mục Tiêu CLB | Mục Tiêu Đẳng Cấp ATP/WTA |")
    A("| --- | --- | --- | --- |")
    for i in range(3):
        A(f"| {varrow[i][1]} | Đo trực tiếp, cùng phác đồ mỗi lần | {varrow[i][2]} | {varrow[i][2]} duy trì "
          f"được khi mệt |")
    for k in range(7):
        m, meas, club, elite = rot(pool["metric"], num, k)
        A(f"| {m} | {meas} | {club} | {elite} |")
    A("")
    for k in range(2):
        A(rot(pool["dosage"], num, k))
        A("")
    A("Cấu trúc khối và phân bổ liều lượng:")
    A("")
    A("| Khối | Mục Tiêu | Liều Lượng | Chỉ Số Theo Dõi |")
    A("| --- | --- | --- | --- |")
    for k in range(5):
        name, timing, detail = rot(pool["step"], num, k + 2)
        m, meas, club, elite = rot(pool["metric"], num, k)
        A(f"| {name} | {first_sentence(detail)} | 2-3 lần mỗi tuần, 20-40 phút | {m} ({club}) |")
    A("")
    A("---")
    A("")

    # ---------------- Mục 5
    A("## 5. Lỗi Thường Gặp, Nguyên Nhân & Giao Thức Khắc Phục")
    A("")
    A("| Lỗi Quan Sát Được | Nguyên Nhân Gốc Rễ | Hậu Quả | Giao Thức Khắc Phục |")
    A("| --- | --- | --- | --- |")
    for e in errs_u:
        A(f"| {e[0]} | {e[1]} | {e[2]} | {e[3]} |")
    for k in range(6):
        e, c, cons, fix = rot(pool["error"], num, k)
        A(f"| {e} | {c} | {cons} | {fix} |")
    A("")
    A(f"Thứ tự ưu tiên khắc phục: trước hết đưa **{varrow[0][1]}** về dải mục tiêu, sau đó kiểm chứng lại "
      f"**{varrow[1][1]}**; chỉ khi đó mới tăng tải. Cố sửa lỗi thực thi trong khi năng lực nền còn ngoài dải sẽ "
      f"tạo ra những chỉnh sửa tạm thời và sụp đổ dưới áp lực thi đấu.")
    A("")
    A("---")
    A("")

    # ---------------- Mục 6
    A("## 6. Sơ Đồ Chẩn Đoán & Ra Quyết Định")
    A("")
    A("```")
    A(box(f"ĐIỂM VÀO CHẨN ĐOÁN - {topic.upper()}", [
        f"ĐẦU VÀO A: {varrow[0][1]} = {varrow[0][2]}",
        f"ĐẦU VÀO B: {varrow[1][1]} = {varrow[1][2]}",
        f"ĐẦU VÀO C: {varrow[2][1]} = {varrow[2][2]}",
    ]))
    A("")
    A("                    |")
    A("        ┌───────────┴────────────┐")
    A(f"        │ {wrap(varrow[0][1] + ' trong dải?', 24)[0]:<24} │")
    A("        └───┬────────────────┬───┘")
    A("       CÓ   │                │  KHÔNG")
    A("   ┌────────▼────────┐  ┌────▼─────────────┐")
    A("   │ tăng tải        │  │ giữ tải,         │")
    A("   │ +5-10% mỗi tuần │  │ sửa năng lực nền │")
    A("   └────────┬────────┘  └────┬─────────────┘")
    A("            │                │")
    A("   ┌────────▼────────────────▼─────────┐")
    A("   │  kiểm tra lại sau 7-10 ngày       │")
    A("   │  so với mục tiêu ở Mục 4          │")
    A("   └───────────────────────────────────┘")
    A("```")
    A("")
    A("Các quy tắc quyết định suy ra từ sơ đồ:")
    A("")
    for k in range(4):
        A(f"- {rot(pool['decision'], num, k)}")
    A("")
    A("---")
    A("")

    # ---------------- Mục 7
    A("## 7. Video Minh Họa & Phân Tích Kỹ Thuật")
    A("")
    A("Video minh họa tham chiếu cho mẫu này được nhúng ở đầu bài viết. Hãy đối chiếu video với các điểm "
      "kiểm tra ở Mục 3 trước khi tăng tải.")
    A("")
    A("Trọng tâm phân tích khi xem lại hình ảnh:")
    A("")
    for k in range(6):
        A(f"- {rot(pool['video'], num, k)}")
    A("")
    A(f"Hãy quan sát riêng khoảnh khắc **{varrow[0][1]}** lệch khỏi mức {varrow[0][2]} - trong gần như mọi "
      f"trường hợp, độ lệch xuất hiện trước khiếm khuyết kỹ thuật nhìn thấy được, chứ không phải sau đó.")
    A("")
    A("---")
    A("")

    # ---------------- Mục 8
    A("## 8. Ứng Dụng Liên Ngành & Phối Hợp Đa Trụ Cột")
    A("")
    A("Mẫu này không tồn tại độc lập; các bài viết sau cung cấp những ràng buộc mà nó phụ thuộc vào:")
    A("")
    for i, rn in enumerate(related_numbers(num, pillar)):
        A(f"- **Bài viết {rn:03d} - {vi_title_of(rn)}**: {rot(REASON_VI, num + i, 0)}.")
    A("")
    A(f"Đọc cùng các bài này, {topic} trở thành một **nút trong hệ thống** thay vì một bài tập tách rời: ràng "
      f"buộc cơ sinh học, tín hiệu tri giác, quy tắc tải và giá trị theo trạng thái tỷ số đều phải đúng đồng "
      f"thời thì mẫu mới tồn tại được dưới áp lực thi đấu.")
    A("")
    A("---")
    A("")

    # ---------------- Mục 9
    A("## 9. Bảng Tự Đánh Giá (Rubric Đa Cấp Độ)")
    A("")
    A("| Tiêu Chí | Mức 1 (Cơ Bản) | Mức 2 (Chuyển Tiếp) | Mức 3 (Chức Năng Hiện Đại) | "
      "Mức 4 (Đẳng Cấp ATP) |")
    A("| --- | --- | --- | --- | --- |")
    for k in range(6):
        crit, l1, l2, l3, l4 = rot(pool["rubric"], num, k)
        A(f"| {crit} | {l1} | {l2} | {l3} | {l4} |")
    A("")
    A("Hướng dẫn chấm điểm: cho điểm mỗi dòng từ 1 đến 4, cộng lại trên sáu dòng (tối đa 24 điểm).")
    A("")
    A("- **6-11**: pha nền tảng. Giảm tải, khôi phục các biến chính, và kiểm tra lại sau hai tuần.")
    A("- **12-17**: pha chức năng. Tăng tải 5-10% mỗi tuần, giữ một tuần giảm tải trong ba tuần.")
    A("- **18-21**: pha thi đấu. Chuyển trọng tâm từ năng lực sang thực thi dưới mệt mỏi và áp lực.")
    A("- **22-24**: duy trì. Giữ nguyên liều, kiểm toán mỗi quý, và tái đầu tư thời gian vào ứng dụng chiến thuật.")
    A("")
    A("---")
    A("")

    # ---------------- Mục 10
    A("## 10. Thẻ Thực Hành In Sổ Tay (Pocket Drill Card)")
    A("")
    A("| Khối | Bài Tập | Số Hiệp x Số Lần | Tín Hiệu | Nghỉ |")
    A("| --- | --- | --- | --- | --- |")
    A(f"| A - Chính | {drills_u[0][0]} | 4 x 8 | {drills_u[0][1]} | 60 giây |")
    A(f"| B - Phụ | {drills_u[1][0]} | 3 x 10 | {drills_u[1][1]} | 60 giây |")
    for k in range(4):
        blk, dr, sets, cue, rest = rot(pool["drill"], num, k)
        A(f"| {blk} | {dr} | {sets} | {cue} | {rest} |")
    A("")
    A("Ghi chú tăng tiến:")
    A("")
    for k in range(3):
        A(f"- {rot(pool['progression'], num, k)}")
    A("")
    A(f"Quy tắc cấp buổi tập: không bao giờ kết thúc buổi tập khi **{varrow[0][1]}** nằm ngoài dải mục tiêu quá "
      f"một bước tăng tiến; mẫu bạn lặp lại khi đang ngoài dải chính là mẫu bạn sẽ tái hiện dưới áp lực.")
    A("")
    return "\n".join(L) + "\n"


# ---------------------------------------------------------------- main
def main():
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    en_written, vi_written, skipped = 0, 0, []
    for num in range(145, 201):
        key = str(num)
        if only and key not in only:
            continue
        if key not in DATA:
            skipped.append(key)
            continue
        meta = META[key]
        data = DATA[key]
        en_md = build_en(num, meta, data)
        vi_md = build_vi(num, meta, data)

        en_path = BASE / "en" / "articles_md" / f"ART-{num:03d}.md"
        en_path.write_text(en_md, encoding="utf-8", newline="\n")
        en_written += 1

        vi_dir = BASE / "vi" / "articles" / meta["slug_vi"]
        vi_dir.mkdir(parents=True, exist_ok=True)
        (vi_dir / "index.md").write_text(vi_md, encoding="utf-8", newline="\n")
        vi_written += 1

        en_vn = sum(1 for c in en_md if c in VN_DIACRITICS)
        print(f"{num:03d} EN {len(en_md.encode('utf-8')):6d} B | VI {len(vi_md.encode('utf-8')):6d} B "
              f"| VI diacritics {sum(1 for c in vi_md if c in VN_DIACRITICS):5d} | EN vn-leak {en_vn}")

    print(f"\nWritten: EN {en_written}, VI {vi_written}")
    if skipped:
        print(f"Missing data for: {', '.join(skipped)}")


if __name__ == "__main__":
    main()
