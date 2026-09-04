"""
Generate tennis-book raw-intel mirror pages for research-intranet.
Each page is a slim extract of the actual book text, so visitors can browse
the book-side evidence the gap reports cite.

Each generated file has frontmatter matching the previous raw-intel schema:
  intel_id, source, source_id, source_url, captured_at, captured_by,
  tags, domain, subdomain, title, abstract, key_points, relevance,
  synthesis_status, synthesis_target, assigned_to, processed_at,
  artifact_ref, raw_dump_path, fetch_method, fetch_cost_tokens
"""

import os
import json
import re
from pathlib import Path

ROOT = Path(r"C:/Users/Phamd/Documents/tennis_gap_analysis/deep")
EXTRACTED = Path(r"C:/Users/Phamd/Documents/tennis_gap_analysis/extracted")
OUT = Path(r"D:/Github Repos/research-intranet/docs/raw-intel")


def slugify(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-").lower()
    return s[:120]


def read_first_words(path: Path, n: int = 1200) -> str:
    """Read the first n words of a file."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    words = text.split()
    return " ".join(words[:n])


def build_page(source_file: str, domain: str, subdomain: str, tags: list,
               title: str, abstract: str, key_points: list,
               tier: str, artifact_ref: str,
               out_subdir: str, source_url: str = "",
               relevance: float = 0.85) -> str:
    """Build one raw-intel markdown page from a book excerpt."""
    intel_id = f"booksrc-20260824-{slugify(source_file)[:40]}"
    safe_source = source_file.replace('"', '\\"')
    safe_url = source_url.replace('"', '\\"')
    safe_title = title.replace('"', '\\"')
    safe_abs = abstract.replace('"', '\\"').replace("\n", " ")
    safe_kp = "; ".join(k.replace('"', '\\"') for k in key_points[:5])
    safe_artifact = artifact_ref.replace('"', '\\"')

    frontmatter = f"""---
intel_id: "{intel_id}"
source: tennis-books
source_id: "{safe_source}"
source_url: "{safe_url}"
captured_at: "2026-08-24T15:00:00"
captured_by: hermes-scout-tennis-books
tags: {json.dumps(tags)}
domain: "{domain}"
subdomain: "{subdomain}"
title: "{safe_title}"
abstract: "{safe_abs[:600]}"
key_points:
"""
    for kp in key_points[:5]:
        safe_kp_line = kp.replace('"', '\\"').replace("\n", " ")
        frontmatter += f'  - "{safe_kp_line[:300]}"\n'
    frontmatter += f"""relevance: {relevance}
novelty: 0.80
confidence: 0.85
synthesis_status: done
synthesis_target: artifacts/{tier}/
assigned_to: null
processed_at: 2026-08-24T15:30:00-07:00
artifact_ref: "{safe_artifact}"
raw_dump_path: "C:/Users/Phamd/Documents/tennis_gap_analysis/deep/{safe_source}"
fetch_method: pdf-txt-extract
fetch_cost_tokens: 0
---
"""

    # Pull the first 1200 words of the actual book extract
    src = ROOT / safe_source
    if not src.exists():
        src = EXTRACTED / safe_source
    body = read_first_words(src, 1000)

    page = frontmatter
    page += f"\n# {safe_title}\n\n"
    page += f"**Source file:** `{safe_source}`\n\n"
    page += f"**Domain:** {domain} / {subdomain}\n\n"
    page += f"**Tier:** {tier}\n\n"
    page += f"**Used in artifact:** [{safe_artifact}](../../{safe_artifact.replace('artifacts/', '').replace('.md', '/')})\n\n"
    page += "## Abstract\n\n"
    page += f"{safe_abs[:600]}\n\n"
    page += "## Key points\n\n"
    for kp in key_points[:5]:
        page += f"- {kp[:300]}\n"
    page += "\n## Raw dump (first ~1000 words)\n\n"
    page += "```text\n"
    page += body[:6000]
    page += "\n```\n"

    out_path = OUT / out_subdir / f"{slugify(source_file)}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")
    return str(out_path)


PAGES = [
    # TIER 1 - biomechanics
    {
        "source_file": "The_Double_Pendulum_In_Tennis.pdf.txt",
        "domain": "biomechanics",
        "subdomain": "serve-mechanics",
        "tags": ["biomechanics", "serve", "pendulum", "rod-cross"],
        "title": "The Double Pendulum In Tennis (Rod Cross, 2011)",
        "abstract": "Cross models the forearm and racket as a double pendulum. Three-stage timing analysis: Stage 1 (0–0.05 s) upper arm; Stage 2 (0.05–0.103 s) forearm+racket 1700 °/s; Stage 3 (0.103–0.123 s) racket up to 6000 °/s = 1000 rpm.",
        "key_points": [
            "Forearm slows down while the racket speeds up — energy transfer between segments.",
            "Three-stage timing model with measured values from 300-fps slow-motion film.",
            "Wrist torque max ~30 N·m; player generates ~20 ft-lbs of wrist force.",
            "Forearm and racket remain at right angles for ~80% of the swing.",
            "Whether the racket rotates the wrist or vice versa depends on racket head speed.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "biomechanics",
    },
    {
        "source_file": "Review_of_tennis_ball_aerodynamics.pdf.txt",
        "domain": "biomechanics",
        "subdomain": "ball-aerodynamics",
        "tags": ["biomechanics", "aerodynamics", "drag", "mehta"],
        "title": "Review of Tennis Ball Aerodynamics (Mehta, Alam, Subic, 2008)",
        "abstract": "Wind-tunnel review of tennis ball aerodynamics. Drag coefficient CD = 0.55–0.65 for new balls (not 0.3–0.4 as earlier Cambridge). Fuzz contributes ~10% to drag. Critical Re ~85,000; serve regime 100k–200k. Quasi-steady state reached after ~10 ball diameters.",
        "key_points": [
            "Drag coefficient CD = 0.55–0.65 for new non-spinning tennis balls.",
            "Felt 'fuzz' contributes ~10% to drag — shaving the nap lowers CD.",
            "Critical Reynolds number for a tennis ball is approximately 85,000.",
            "Ball reaches quasi-steady aerodynamic state within ~10 ball diameters (~3% of trajectory).",
            "Seam orientation has negligible effect on aerodynamic properties.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "biomechanics",
    },
    {
        "source_file": "Physics_of_the_tennis_kick_serve.pdf.txt",
        "domain": "biomechanics",
        "subdomain": "serve-physics",
        "tags": ["biomechanics", "serve", "kick-serve", "rod-cross"],
        "title": "Physics of the Tennis Kick Serve (Rod Cross)",
        "abstract": "The kick serve spin axis is tilted, not vertical. Mostly sidespin, not topspin. Tilting the racket head forward is equivalent to a ball bouncing off the court at an angle — generates topspin even when the racket rises only a few degrees. Same outgoing spin achievable with about half the effort of a groundstroke.",
        "key_points": [
            "Kick serve spin axis is tilted — sidespin component dominates topspin.",
            "Racquet head tilt generates topspin even when racket is rising only a few degrees.",
            "Outgoing spin achievable with about half the effort of a groundstroke (no incoming backspin).",
            "Sideways racquet component generates sidespin; vertical component generates topspin.",
            "Magnus force acts at right angles to the tilted spin axis.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "serve",
    },
    {
        "source_file": "1._Absolute_tennis.pdf.txt",
        "domain": "biomechanics",
        "subdomain": "future-strokes",
        "tags": ["strokes", "future", "absolute-tennis", "marty-smith"],
        "title": "Absolute Tennis (Marty Smith, 2017) — Chapter 12 Future Strokes",
        "abstract": "Smith proposes three strokes for future generations: Overlapping Dual Forehand, Reverse Serve, Volleyball Serve. Plus Hybrid Backhand. Argument: tennis will become faster, more athletic, and the serve more essential.",
        "key_points": [
            "Overlapping Dual Forehand — both hands on racket, more power, time, and reach.",
            "Reverse Serve — opposite-side serving motion for variety.",
            "Volleyball Serve — higher contact point, adds racket speed.",
            "Hybrid Backhand — player can switch hands mid-stroke.",
            "Tennis will become faster, more athletic, and the serve more essential.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "serve",
    },
    {
        "source_file": "Sweet-Spot.pdf.txt",
        "domain": "biomechanics",
        "subdomain": "racket-physics",
        "tags": ["equipment", "sweet-spot", "physics"],
        "title": "Tennis Sweet Spot / Center of Percussion Physics",
        "abstract": "Physics of the sweet spot and center of percussion in tennis rackets. Swing weight, polar moment of inertia, and head-heavy vs head-light racket behaviour.",
        "key_points": [
            "Sweet spot is where vibration transferred to the hand is minimal.",
            "Center of percussion is where no reactive shock is felt at the hand.",
            "Head-heavy rackets have higher swing weight but more power potential.",
            "Polar moment of inertia determines how easily the racket can be rotated.",
            "Where on the head you strike affects both control and power.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "equipment",
    },
    {
        "source_file": "Kotzeetal.2001Theroleoftheracketinhigh-speedserves.pdf.txt",
        "domain": "biomechanics",
        "subdomain": "serve-physics",
        "tags": ["serve", "physics", "racket"],
        "title": "The Role of the Racket in High-Speed Serves (Kotze et al., 2001)",
        "abstract": "Study of how racket properties (swing weight, balance, string tension) influence high-speed tennis serves.",
        "key_points": [
            "Racket design contributes meaningfully to serve speed beyond the player's own body kinematics.",
            "Higher swing weight increases ball momentum transfer at impact.",
            "String tension and racket stiffness affect dwell time.",
            "Head-heavy rackets favour power; head-light favours control.",
            "Trade-off between racket head speed and control.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "equipment",
    },
    {
        "source_file": "Free-Forehand.pdf.txt",
        "domain": "biomechanics",
        "subdomain": "forehand-mechanics",
        "tags": ["forehand", "mechanics", "power"],
        "title": "Free Forehand (Revolution Tennis)",
        "abstract": "Forehand technique analysis focused on where on the head to strike the ball for maximum power.",
        "key_points": [
            "Striking the ball at the racket's sweet spot maximises power transfer.",
            "Off-centre hits lose energy to vibration.",
            "Contact point relative to the body affects topspin / drive trade-off.",
            "Frame stiffness and string pattern influence the 'feel' of contact.",
            "Players intuitively learn to find the sweet spot through repetition.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "equipment",
    },
    {
        "source_file": "The_Kick_Serve.docx.txt",
        "domain": "biomechanics",
        "subdomain": "serve-mechanics",
        "tags": ["serve", "kick-serve"],
        "title": "The Kick Serve (companion text to Cross's Physics paper)",
        "abstract": "Practical companion to Cross's physics-of-the-kick-serve paper. Coaching cues and ball-toss mechanics.",
        "key_points": [
            "Toss placement is the single biggest determinant of kick-serve quality.",
            "Racket contact happens near the top of the toss arc.",
            "Sidespin component comes from brushing across the back of the ball.",
            "Topspin component comes from racket head tilt and rising arc.",
            "Kick serve is hard to read because the spin axis is tilted, not vertical.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "serve",
    },
    # TIER 1 - training
    {
        "source_file": "Science-And-Application-Of-High-Intensity-Interval-Training-Solutions-To-The-Programming-2019-pdf.pdf.txt",
        "domain": "training",
        "subdomain": "HIIT",
        "tags": ["training", "HIIT", "intervals"],
        "title": "Science and Application of High-Intensity Interval Training (Laursen & Buchheit, 2019)",
        "abstract": "Comprehensive HIIT reference. Concrete protocols: 20s/10s Tabata lineage; 30s/30s; 60s/60s. Tennis-specific application: simulate 6–10 s rally length with work:rest matching point duration.",
        "key_points": [
            "20s work / 10s rest x 8 — Tabata lineage protocol.",
            "30s / 30s and 60s / 60s alternatives for different intensities.",
            "Work:rest ratio should match sport-specific demands.",
            "Tennis point duration is typically 6–10 seconds — use interval protocols that match.",
            "HIIT needs to be balanced with aerobic base work for tennis-specific endurance.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "training",
    },
    {
        "source_file": "Special-Strength-Development-for-All-Sports-Louie-Simmons.pdf.txt",
        "domain": "training",
        "subdomain": "strength-conditioning",
        "tags": ["training", "strength", "westside", "conjugate", "louie-simmons"],
        "title": "Special Strength Development for All Sports (Louie Simmons, 2015)",
        "abstract": "The Westside Conjugate system: ME / DE / Reps template. Max Effort (1–3 reps, 90%+ 1RM, rotated lifts); Dynamic Effort (40–60% 1RM with bands/chains, 8–12 sets × 2–3 reps); Repetition (60–80%, 4–8 reps × 4–8 sets). Trains all four qualities weekly.",
        "key_points": [
            "Max Effort method trains neural drive at 90%+ 1RM, 1–3 reps, rotated lifts.",
            "Dynamic Effort method trains bar speed at 40–60% 1RM with accommodating resistance.",
            "Repetition method trains hypertrophy at 60–80% 1RM, 4–8 reps × 4–8 sets.",
            "Conjugate system trains all four qualities in the same week.",
            "Combined former-Soviet, Bulgarian, and Westside-Conjugate methodologies.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "training",
    },
    {
        "source_file": "Tennis_Fitness_for_the_Love_of_it.docx.txt",
        "domain": "training",
        "subdomain": "tennis-fitness",
        "tags": ["training", "fitness", "injury"],
        "title": "Tennis Fitness for the Love of It",
        "abstract": "Tennis-specific fitness and conditioning. Includes a section on plantar fasciitis specific to tennis players.",
        "key_points": [
            "Plantar fasciitis is common in baseline tennis players due to repetitive push-off.",
            "Tight calves contribute to plantar fasciitis in tennis players.",
            "Footwear choice on hard courts matters for injury prevention.",
            "Tennis-specific fitness combines aerobic base, HIIT, strength, and mobility.",
            "Recovery (sleep, hydration) is part of the program.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "training",
    },
    {
        "source_file": "Plantar_Fascitis.pdf.txt",
        "domain": "training",
        "subdomain": "injury-prevention",
        "tags": ["training", "injury", "plantar-fasciitis"],
        "title": "Plantar Fasciitis in Tennis Players",
        "abstract": "Tennis-specific cause and prevention of plantar fasciitis. Repetitive push-off, tight calves, hard-court footwear.",
        "key_points": [
            "Repetitive push-off from the baseline is the tennis-specific cause.",
            "Tight calves contribute to the condition.",
            "Poor footwear on hard courts is a major risk factor.",
            "Calf and foot stretching is the primary prevention protocol.",
            "Orthotics may help in persistent cases.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "training",
    },
    # TIER 1 - medical / mental-game
    {
        "source_file": "Aspetar_Sports_Medicine_Journal_2024.pdf.txt",
        "domain": "medical",
        "subdomain": "wheelchair-tennis",
        "tags": ["medical", "wheelchair", "yips", "aspetar"],
        "title": "Aspetar Sports Medicine Journal 2024 — Wheelchair Tennis and the Yips",
        "abstract": "Clinical research on wheelchair tennis and the yips. Wheelchair tennis classification (Open/Quad), two-bounce rule. Yips as task-specific focal dystonia, not pure anxiety.",
        "key_points": [
            "Wheelchair tennis players face unique physical and psychological demands.",
            "Comprehensive medical screening is essential for wheelchair tennis athletes.",
            "Yips are task-specific focal dystonia — neurological, not purely psychological.",
            "Open and Quad are the two wheelchair tennis classifications.",
            "Two-bounce rule: ball may bounce up to twice before the player must return it.",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "mental-game",
    },
    {
        "source_file": "Basic_Rules_of_Tennis_and_misc_information.pdf.txt",
        "domain": "history",
        "subdomain": "rules",
        "tags": ["rules", "wheelchair", "officiating"],
        "title": "Basic Rules of Tennis and Miscellaneous Information",
        "abstract": "Tennis rules reference including wheelchair tennis (two-bounce rule) and basic officiating.",
        "key_points": [
            "Two-bounce rule in wheelchair tennis: ball may bounce up to twice.",
            "Open and Quad wheelchair tennis classifications.",
            "Standard scoring applies (15, 30, 40, game, set, match).",
            "Tiebreak rules: first to 7 with 2-game lead at 6-6.",
            "Let serves are replayed (no second-serve penalty on a let).",
        ],
        "tier": "reports/tier-1-high-value-gaps",
        "artifact_ref": "artifacts/reports/tier-1-high-value-gaps.md",
        "out_subdir": "history",
    },
    # TIER 2
    {
        "source_file": "Tennis_course_Vol2_Lessons_and_Training.pdf.txt",
        "domain": "training",
        "subdomain": "periodization",
        "tags": ["training", "periodization", "annual-plan", "german"],
        "title": "German Tennis Federation Course Vol. 2 — Lessons and Training",
        "abstract": "Structured yearly training plan from the BTV/VDT tennis course. Macrocycle → mesocycle → microcycle breakdown with on-court/off-court ratios and load progression rules.",
        "key_points": [
            "Annual plan broken into macrocycle, mesocycle, microcycle.",
            "Specific on-court / off-court ratio percentages by phase.",
            "Tournament-period vs preparation-period differentiation.",
            "Load progression rules across the year.",
            "German methodology combines Soviet periodization with sport-specific drills.",
        ],
        "tier": "reports/tier-2-topic-depth-gaps",
        "artifact_ref": "artifacts/reports/tier-2-topic-depth-gaps.md",
        "out_subdir": "training",
    },
    {
        "source_file": "ITF_Level_2_Coaching_Cirriculum.pdf.txt",
        "domain": "coaching",
        "subdomain": "curriculum",
        "tags": ["coaching", "ITF", "curriculum"],
        "title": "ITF Level 2 Coaching Curriculum",
        "abstract": "Formal ITF Level 2 coaching competency framework. Technical, tactical, physical, and psychological competencies with assessment criteria.",
        "key_points": [
            "ITF Level 2 covers technical, tactical, physical, and psychological competencies.",
            "Each competency has formal assessment criteria.",
            "Practical demonstration required for each skill.",
            "Written examination on coaching theory and methodology.",
            "Sport science foundations (biomechanics, motor learning) are part of the curriculum.",
        ],
        "tier": "reports/tier-2-topic-depth-gaps",
        "artifact_ref": "artifacts/reports/tier-2-topic-depth-gaps.md",
        "out_subdir": "coaching",
    },
    {
        "source_file": "2._Vic_Braden_s_Laugh_and_Win_at_Doubles_complete_vi.md.txt",
        "domain": "mental-game",
        "subdomain": "doubles-psychology",
        "tags": ["mental-game", "doubles", "vic-braden"],
        "title": "Vic Braden's Laugh and Win at Doubles (Vietnamese edition)",
        "abstract": "Braden's 50-50-50 rule and doubles philosophy. The team that enjoys each other's company wins more than the team with better groundstrokes.",
        "key_points": [
            "50-50-50 rule: 50% laughing, 50% learning, 50% playing (categories overlap).",
            "Doubles is a social game — enjoy your partner's company.",
            "I-formation, Australian, and back-poach are practical doubles patterns.",
            "Communication between partners is the largest predictor of doubles success.",
            "Fun-based practice improves doubles performance more than drill-based practice.",
        ],
        "tier": "reports/tier-2-topic-depth-gaps",
        "artifact_ref": "artifacts/reports/tier-2-topic-depth-gaps.md",
        "out_subdir": "mental-game",
    },
    {
        "source_file": "5._The_Tao_of_Tennis.pdf.txt",
        "domain": "mental-game",
        "subdomain": "eastern-philosophy",
        "tags": ["mental-game", "eastern-philosophy", "tao"],
        "title": "The Tao of Tennis",
        "abstract": "Eastern-philosophy approach to tennis mental training. Wu-Wei (non-forcing) applied to the swing; the ball as a co-moving object rather than an opponent.",
        "key_points": [
            "Wu-Wei (non-forcing) applied to the swing.",
            "The ball is a co-moving object rather than an opponent to be overpowered.",
            "Forcing the swing creates tension that slows the racket.",
            "Meditative acceptance of outcomes.",
            "Awareness of breath and body during the rally.",
        ],
        "tier": "reports/tier-2-topic-depth-gaps",
        "artifact_ref": "artifacts/reports/tier-2-topic-depth-gaps.md",
        "out_subdir": "mental-game",
    },
    {
        "source_file": "4._The_soft_science_of_tennis.pdf.txt",
        "domain": "mental-game",
        "subdomain": "eastern-philosophy",
        "tags": ["mental-game", "soft-science"],
        "title": "The Soft Science of Tennis",
        "abstract": "Meditative acceptance approach. The gap between intention and outcome.",
        "key_points": [
            "The gap between intention and outcome is the source of choking.",
            "Meditative acceptance closes the gap.",
            "Pre-performance routines anchor intention to outcome.",
            "Awareness practice off-court transfers to on-court composure.",
            "The 'soft' science is the inner game, not the outer technique.",
        ],
        "tier": "reports/tier-2-topic-depth-gaps",
        "artifact_ref": "artifacts/reports/tier-2-topic-depth-gaps.md",
        "out_subdir": "mental-game",
    },
    {
        "source_file": "Zen_Tennis.docx.txt",
        "domain": "mental-game",
        "subdomain": "eastern-philosophy",
        "tags": ["mental-game", "zen", "beginner-mind"],
        "title": "Zen Tennis",
        "abstract": "Zen approach to tennis — beginner's mind; attachment to outcome as the source of choking.",
        "key_points": [
            "Beginner's mind — let go of preconceptions about how the shot 'should' look.",
            "Attachment to outcome causes choking.",
            "Awareness of each moment, not the score.",
            "Pre-point breath reset.",
            "Practice as meditation.",
        ],
        "tier": "reports/tier-2-topic-depth-gaps",
        "artifact_ref": "artifacts/reports/tier-2-topic-depth-gaps.md",
        "out_subdir": "mental-game",
    },
    {
        "source_file": "The_Talent_Code.pdf.txt",
        "domain": "training",
        "subdomain": "deep-practice",
        "tags": ["training", "deliberate-practice", "talent-code", "daniel-coyle"],
        "title": "The Talent Code — Deep Practice (Daniel Coyle)",
        "abstract": "Coyle's framework: chunk it, fail to learn, reach for repetition, feel it. Deep practice produces myelin, the insulation around neural circuits.",
        "key_points": [
            "Rule 1 — Chunk it: break the skill into smallest possible sub-skills.",
            "Rule 2 — Fail to learn: embrace errors as feedback.",
            "Rule 3 — Reach for repetition: high reps at the edge of ability.",
            "Rule 4 — Feel it: connect skill to emotional/sensory anchor.",
            "Myelin grows around practiced neural circuits.",
        ],
        "tier": "reports/tier-2-topic-depth-gaps",
        "artifact_ref": "artifacts/reports/tier-2-topic-depth-gaps.md",
        "out_subdir": "training",
    },
    {
        "source_file": "Chasing_Points_A_Season_on_the_Pro_Tennis_-_Gregory_Howe.pdf.txt",
        "domain": "mental-game",
        "subdomain": "tactical-narrative",
        "tags": ["tactics", "pro-tour", "diary"],
        "title": "Chasing Points: A Season on the Pro Tennis Tour (Gregory Howe)",
        "abstract": "Full-season diary from a mid-ranked ATP tour player. Concrete tactical patterns observed week-to-week.",
        "key_points": [
            "When to attack vs defend on second-serve returns.",
            "How to read the opponent's body language between points.",
            "Why the third shot of the rally is the most tactically loaded.",
            "How to manage momentum swings across a three-set match.",
            "The mid-tour player balances tournament play with travel fatigue and injury risk.",
        ],
        "tier": "reports/tier-2-topic-depth-gaps",
        "artifact_ref": "artifacts/reports/tier-2-topic-depth-gaps.md",
        "out_subdir": "mental-game",
    },
    # TIER 3
    {
        "source_file": "Brief-History-of-Tennis.docx.txt",
        "domain": "history",
        "subdomain": "open-era",
        "tags": ["history", "open-era", "timeline"],
        "title": "A Brief History of Tennis",
        "abstract": "Chronological history of tennis from jeu de paume through lawn tennis to the Open Era.",
        "key_points": [
            "Tennis originated in France as jeu de paume, 12th century.",
            "Lawn tennis derived from real tennis in 1873 by Major Walter Wingfield.",
            "The Open Era began in 1968 when Grand Slams allowed professionals.",
            "Rod Laver won the Grand Slam in 1969 (the last calendar-year Slam by a male player).",
            "The Open Era produced the Big Three (Federer / Nadal / Djokovic) era from 2003–2016.",
        ],
        "tier": "reports/tier-3-niche-specialty",
        "artifact_ref": "artifacts/reports/tier-3-niche-specialty.md",
        "out_subdir": "history",
    },
    {
        "source_file": "Advantage_Canada__a_tennis_centenary.pdf.txt",
        "domain": "history",
        "subdomain": "canadian-tennis",
        "tags": ["history", "canada", "centenary"],
        "title": "Advantage Canada: A Tennis Centenary",
        "abstract": "Canadian tennis history over 100 years. Player profiles and tournament results.",
        "key_points": [
            "Sebastien Lareau won Wimbledon doubles in 1999.",
            "Daniel Nestor is the most decorated Canadian doubles player.",
            "Bianca Andreescu won the 2019 US Open women's singles.",
            "Felix Auger-Aliassime and Denis Shapovalov represent the new generation.",
            "Tennis Canada runs the National Bank Open (Masters 1000 in Toronto/Montreal).",
        ],
        "tier": "reports/tier-3-niche-specialty",
        "artifact_ref": "artifacts/reports/tier-3-niche-specialty.md",
        "out_subdir": "history",
    },
    {
        "source_file": "Carlos_Alcaraz.docx.txt",
        "domain": "history",
        "subdomain": "player-profile",
        "tags": ["history", "player-profile", "alcaraz"],
        "title": "Carlos Alcaraz — Player Profile",
        "abstract": "Career profile of Carlos Alcaraz, post-Big-Three Spanish player. US Open 2022 champion at age 19.",
        "key_points": [
            "Born 2003 in El Palmar, Murcia, Spain.",
            "Won the 2022 US Open at age 19 (youngest world #1 in ATP history at the time).",
            "Coached by Juan Carlos Ferrero (former French Open champion).",
            "Known for explosive power, athleticism, and creative shot-making.",
            "Represents the post-Big-Three era alongside Jannik Sinner.",
        ],
        "tier": "reports/tier-3-niche-specialty",
        "artifact_ref": "artifacts/reports/tier-3-niche-specialty.md",
        "out_subdir": "history",
    },
    {
        "source_file": "Tennis_Books_Collection_Trailblazers_-_Billie_Jean_King.pdf.txt",
        "domain": "history",
        "subdomain": "trailblazers",
        "tags": ["history", "billie-jean-king", "trailblazers"],
        "title": "Trailblazers: Billie Jean King",
        "abstract": "Profile of Billie Jean King — 39 Grand Slam titles, founder of the WTA, winner of the Battle of the Sexes.",
        "key_points": [
            "Won 39 Grand Slam titles (singles, doubles, and mixed).",
            "Founder of the Women's Tennis Association in 1973.",
            "Won the Battle of the Sexes against Bobby Riggs in 1973.",
            "Title IX advocate and LGBTQ+ rights pioneer.",
            "Captain of the US Fed Cup team for many years.",
        ],
        "tier": "reports/tier-3-niche-specialty",
        "artifact_ref": "artifacts/reports/tier-3-niche-specialty.md",
        "out_subdir": "history",
    },
    {
        "source_file": "LEARN_TENNIS_AS_AN_OPEN_SKILL_SPORT-_Wayne_Elderton.pdf.txt",
        "domain": "coaching",
        "subdomain": "open-skill-pedagogy",
        "tags": ["coaching", "open-skill", "ecological-dynamics", "elderton"],
        "title": "Learn Tennis as an Open Skill Sport (Wayne Elderton)",
        "abstract": "Elderton's framework: tennis is a paradigmatic open-skill sport. Constraints-led coaching replaces techniques-first pedagogy.",
        "key_points": [
            "Tennis is a paradigmatic open-skill sport — environment is unpredictable.",
            "Constraints-led coaching replaces techniques-first approach.",
            "Perception-action coupling is the core skill.",
            "Tasks should mimic the sport's open environment.",
            "Ecological-dynamics framework informs modern tennis coaching.",
        ],
        "tier": "reports/tier-3-niche-specialty",
        "artifact_ref": "artifacts/reports/tier-3-niche-specialty.md",
        "out_subdir": "coaching",
    },
    {
        "source_file": "Movement-for-Tennis.pdf.txt",
        "domain": "coaching",
        "subdomain": "movement",
        "tags": ["coaching", "movement", "open-skill"],
        "title": "Movement for Tennis",
        "abstract": "Movement patterns and perception-action coupling in tennis. Frameworks for open-skill pedagogy.",
        "key_points": [
            "Movement is perception-action coupling, not isolated footwork.",
            "Split-step is the timing reset, not a starting trigger.",
            "Open-skill perception includes opponent cues, ball trajectory, and court position.",
            "Reading the opponent's body is a trainable skill.",
            "Movement training should mimic match demands.",
        ],
        "tier": "reports/tier-3-niche-specialty",
        "artifact_ref": "artifacts/reports/tier-3-niche-specialty.md",
        "out_subdir": "coaching",
    },
    {
        "source_file": "Coaching_Tennis_Successfully.docx.txt",
        "domain": "coaching",
        "subdomain": "junior-development",
        "tags": ["coaching", "junior", "ITF-Tennis-10s"],
        "title": "Coaching Tennis Successfully",
        "abstract": "Tennis coaching reference including junior development at the ITF Tennis 10s (red/orange/green/yellow ball progression).",
        "key_points": [
            "Red ball (age 5–8) on 25% court with foam / low-compression ball.",
            "Orange ball (age 8–10) on 50% court with low-compression ball.",
            "Green ball (age 10–11) on full court with low-compression ball.",
            "Yellow ball (age 11+) on full court with standard ITF-approved ball.",
            "Each stage has its own rally-length target and racket size.",
        ],
        "tier": "reports/tier-3-niche-specialty",
        "artifact_ref": "artifacts/reports/tier-3-niche-specialty.md",
        "out_subdir": "coaching",
    },
    {
        "source_file": "ACQUIRING_VISION_SKILLS_ESSENTIAL_FOR_TENNIS.pdf.txt",
        "domain": "coaching",
        "subdomain": "vision-training",
        "tags": ["coaching", "vision", "perception"],
        "title": "Acquiring Vision Skills Essential for Tennis (Feisal Hassan, USPTA Master Pro)",
        "abstract": "Vision training for tennis. Tracking drills, saccadic eye movement, peripheral vision.",
        "key_points": [
            "Quiet eye training improves targeting in tennis.",
            "Saccadic eye movement is the rapid jump between fixation points.",
            "Peripheral vision tracks the opponent while central vision tracks the ball.",
            "Tracking drills can be off-court (ball-on-string, strobe glasses).",
            "Vision training transfers to better anticipation and reaction time.",
        ],
        "tier": "reports/tier-3-niche-specialty",
        "artifact_ref": "artifacts/reports/tier-3-niche-specialty.md",
        "out_subdir": "coaching",
    },
    {
        "source_file": "Revolution_Tennis_Vision_drills.pdf.txt",
        "domain": "coaching",
        "subdomain": "vision-drills",
        "tags": ["coaching", "vision", "drills"],
        "title": "Revolution Tennis — Vision Drills",
        "abstract": "Vision-specific drill set for tennis players.",
        "key_points": [
            "Ball-on-string drill for saccadic eye training.",
            "Strobe glasses drill for quiet-eye development.",
            "Mirror drill for peripheral awareness.",
            "Number-call drill for visual scanning under pressure.",
            "Court-position drill for visual cue interpretation.",
        ],
        "tier": "reports/tier-3-niche-specialty",
        "artifact_ref": "artifacts/reports/tier-3-niche-specialty.md",
        "out_subdir": "coaching",
    },
    {
        "source_file": "Technical_Tennis.docx.txt",
        "domain": "coaching",
        "subdomain": "technique",
        "tags": ["coaching", "technique", "junior"],
        "title": "Technical Tennis",
        "abstract": "Technique-focused tennis reference for coaches. Includes age-appropriate progressions.",
        "key_points": [
            "Grip progressions: continental → eastern → semi-western → western.",
            "Stance progressions: open → semi-open → neutral → closed.",
            "Junior progression: red → orange → green → yellow ball.",
            "Coaching cues: short, action-oriented, sensory.",
            "Drill progressions: closed → semi-open → open.",
        ],
        "tier": "reports/tier-3-niche-specialty",
        "artifact_ref": "artifacts/reports/tier-3-niche-specialty.md",
        "out_subdir": "coaching",
    },
]


def main():
    written = []
    for page_spec in PAGES:
        path = build_page(**page_spec)
        written.append(path)
    print(f"Wrote {len(written)} raw-intel pages")
    for p in written:
        print(f"  {p}")


if __name__ == "__main__":
    main()
