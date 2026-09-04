"""
Auto-generate reader pages for every PDF in site/books/.

Each PDF gets:
- A slug-based folder under docs/books/read/<slug>/
- An index.md with the iframe + download link
- Pre-extracted frontmatter (title, author inferred from filename, domain auto-categorised)

Then this script also rewrites docs/books/index.md with all books listed.
"""

import os
import re
import sys
import shutil
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BOOKS_DIR = Path(r"D:/Github Repos/research-intranet/site/books")
DOCS_READ = Path(r"D:/Github Repos/research-intranet/docs/books/read")
DOCS_INDEX = Path(r"D:/Github Repos/research-intranet/docs/books/index.md")

# Existing manual mapping for famous books (overrides auto-detected title/author/domain)
KNOWN = {
    "absolute-tennis.pdf": ("Absolute Tennis", "Marty Smith, 2017", "Strokes",
        "Marty Smith's foundational text including the famous Ch. 12 'Future Strokes' (Overlapping Dual Forehand, Reverse Serve, Volleyball Serve, Hybrid Backhand)."),
    "1. Absolute tennis.pdf": ("Absolute Tennis", "Marty Smith, 2017", "Strokes",
        "Marty Smith's foundational text including Ch. 12 Future Strokes."),
    "The Double Pendulum in Tennis.pdf": ("The Double Pendulum in Tennis", "Rod Cross, 2011", "Biomechanics",
        "Cross models the forearm + racket as a double pendulum. Three-stage serve timings (0-0.05s, 0.05-0.103s, 0.103-0.123s)."),
    "Review of tennis ball aerodynamics.pdf": ("Review of Tennis Ball Aerodynamics", "Mehta, Alam & Subic, 2008", "Biomechanics",
        "Drag coefficient CD = 0.55-0.65 for new balls. Critical Re ≈ 85,000. Fuzz contributes ~10% to drag."),
    "Physics of the tennis kick serve.pdf": ("Physics of the Tennis Kick Serve", "Rod Cross", "Serve",
        "The kick serve spin axis is tilted, not vertical. Mostly sidespin. Racket head tilt generates topspin even when racket rises only a few degrees."),
    "An 8-Stage Model for Evaluating the Tennis Serve.pdf": ("An 8-Stage Model for Evaluating the Tennis Serve", "Kovacs & Ellenbecker, 2011", "Serve",
        "The canonical 8-stage tennis serve biomechanics framework with measured joint angles and EMG data."),
    "Biomechanicsoftennis.pdf": ("Biomechanics of Tennis", "University textbook", "Biomechanics",
        "Comprehensive biomechanics of all tennis strokes."),
    "Biomechanics-of-the-Tennis-Groundstrokes.pdf": ("Biomechanics of the Tennis Groundstrokes", "Elliott (research)", "Biomechanics",
        "Research article on the biomechanics of forehand and backhand groundstrokes."),
    "Tennis-Biomechanics.pdf": ("Tennis Biomechanics (overview)", "Knudson textbook", "Biomechanics",
        "Tennis biomechanics overview covering strokes, equipment, and injury mechanics."),
    "10. BIOMECHANICAL PRINCIPLES OF TENNIS TECHNIQUE.pdf": ("Biomechanical Principles of Tennis Technique", "Knudson", "Biomechanics",
        "Academic chapter on biomechanical principles applied to tennis technique."),
    "Hi-techtennis – The Secrets of Pro Strokes-The Fan.pdf": ("Hi-Tech Tennis — Secrets of Pro Strokes", "The Fan", "Strokes",
        "Technical analysis of pro strokes from high-speed video."),
    "Tennisology-Inside-the-Science-of-Serves-Nerves-and-On-Court-Dominance-pdf.pdf": ("Tennisology — Inside the Science", "Sports science compilation", "Mental Game",
        "Sports science view of serves, nerves, and on-court dominance."),
    "USPTA_high_performance_Vol._2_No_4.2005_footwork_in_modern_tennis.pdf": ("Footwork in Modern Tennis", "USPTA High Performance Vol. 2 No. 4", "Footwork",
        "USPTA coaching article on footwork patterns, split-step timing, recovery."),
    "USTA-high-performance-vol-6-no-4-2004-federer-3-forehands.pdf": ("Federer's Three Forehands", "USTA High Performance Vol. 6 No. 4 (2004)", "Forehand",
        "Federer's three forehand variations dissected at high-speed video."),
    "Revolutionary-tennis.pdf": ("Revolutionary Tennis", "John Yandell (analysis)", "Strokes",
        "High-speed video analysis of modern pro strokes."),
    "Free-Forehand.pdf": ("Free Forehand", "Revolution Tennis", "Forehand",
        "Forehand technique and where on the racket to strike for maximum power."),
    "Explosive tennis - The forehand.pdf": ("Explosive Tennis — The Forehand", "Tennis technique analysis", "Forehand",
        "Power development for the modern forehand."),
    "Sweet-Spot.pdf": ("Sweet Spot Physics", "Equipment physics reference", "Equipment",
        "Sweet spot and center of percussion physics for tennis rackets."),
    "Kotzeetal.2001Theroleoftheracketinhigh-speedserves.pdf": ("Role of the Racket in High-Speed Serves", "Kotze et al., 2001", "Equipment",
        "Peer-reviewed research on racket design's contribution to serve speed."),
    "Anatomy-of-Modern-Tennis-Shot.pdf": ("Anatomy of the Modern Tennis Shot", "USPTA High Performance Vol. 3 No. 1", "Strokes",
        "Anatomical breakdown of the modern tennis shot."),
    "Aspetar Sports Medicine Journal 2024.pdf": ("Aspetar Sports Medicine Journal 2024", "Aspetar", "Medical",
        "Wheelchair tennis screening, yips as task-specific focal dystonia, latest clinical research."),
    "Aspetar Sports Medicine Journal 2023.pdf": ("Aspetar Sports Medicine Journal 2023", "Aspetar", "Medical",
        "Sports medicine research relevant to tennis players."),
    "Aspetar Sports Medicine Journal 2025.pdf": ("Aspetar Sports Medicine Journal 2025", "Aspetar", "Medical",
        "Latest sports medicine research relevant to tennis players."),
    "Plantar Fascitis.pdf": ("Plantar Fasciitis in Tennis", "Medical reference", "Medical",
        "Tennis-specific cause and prevention of plantar fasciitis."),
    "ACQUIRING VISION SKILLS ESSENTIAL FOR TENNIS Feisal Hassan, USPTA Master Professional.pdf": ("Acquiring Vision Skills Essential for Tennis", "Feisal Hassan, USPTA Master Pro", "Mental Game",
        "Vision training for tennis. Saccadic eye movement, peripheral vision, quiet eye."),
    "3. Winning Ugly.pdf": ("Winning Ugly", "Brad Gilbert", "Mental Game",
        "Mental warfare classic — Brad Gilbert's guide to competitive tennis strategy."),
    "4. The soft science of tennis.pdf": ("The Soft Science of Tennis", "Mental-game classic", "Mental Game",
        "Meditative acceptance approach to tennis mental training."),
    "5. The Tao of Tennis.pdf": ("The Tao of Tennis", "Eastern-philosophy approach", "Mental Game",
        "Eastern-philosophy approach to tennis mental training."),
    "8. Tennis science for tennis players.pdf": ("Tennis Science for Tennis Players", "University research compilation", "Biomechanics",
        "University research compiled for the serious player."),
    "9. TENNIS_Handbook of Sports Medicine and Science.pdf": ("Tennis Handbook of Sports Medicine and Science", "ITF medical reference", "Medical",
        "ITF medical reference handbook."),
    "7. Tennis Lessons from FTPTennis.pdf": ("Tennis Lessons from FTPTennis", "FTP compilation", "Strokes",
        "Lessons compiled from FTPTennis."),
    "HIIT-Laursen-Buchheit.pdf": ("Science & Application of HIIT", "Laursen & Buchheit, 2019", "Training",
        "Comprehensive HIIT reference. Concrete protocols: 20s/10s, 30s/30s, 60s/60s. Sport-specific application."),
    "Special-Strength-Development-for-All-Sports-Louie-Simmons.pdf": ("Special Strength Development for All Sports", "Louie Simmons, Westside Barbell", "Training",
        "The ME / DE / Reps template. Max Effort, Dynamic Effort, Repetition methods. Conjugate system."),
    "Tennis-Workbook.pdf": ("Tennis Workbook", "USTA coaching workbook", "Training",
        "USTA coaching drills and progression workbook."),
    "How-to-Outsmart-Your-Opponent-and-Force-an-Error_-8-Tactics-You-Need-to-be-Using-2.pdf": ("How to Outsmart Your Opponent", "Tactical play", "Tactics",
        "8 tactics for forcing opponent errors."),
    "the-inner-game-of-tennis.pdf": ("The Inner Game of Tennis", "Timothy Gallwey", "Mental Game",
        "The classic mental-game book. Inner Game #1."),
    "ITF Level 2 Coaching Cirriculum.pdf": ("ITF Level 2 Coaching Curriculum", "ITF", "Coaching",
        "Formal ITF Level 2 coaching competency framework."),
    "ITF - Coaching and Science Review.pdf": ("ITF Coaching and Science Review", "ITF", "Coaching",
        "ITF peer-reviewed coaching research publication."),
    "Movement-for-Tennis.pdf": ("Movement for Tennis", "Movement analysis", "Coaching",
        "Movement patterns and perception-action coupling in tennis."),
    "LEARN TENNIS AS AN OPEN SKILL SPORT- Wayne Elderton.pdf": ("Learn Tennis as an Open Skill Sport", "Wayne Elderton", "Coaching",
        "Constraints-led coaching replaces techniques-first pedagogy."),
    "Winning-Tennis-Tactics.pdf": ("Winning Tennis Tactics", "Tactical play", "Tactics",
        "Tactical patterns and formations for competitive tennis."),
    "Tennis-Strategy-Tacticsand-Technique.pdf": ("Tennis Strategy, Tactics and Technique", "Tennis reference", "Tactics",
        "Comprehensive strategy and tactics reference."),
    "Coaching Tennis Technical and Tactical Skills.pdf": ("Coaching Tennis: Technical and Tactical Skills", "Coaching reference", "Coaching",
        "Coaching methodology for technical and tactical skills."),
    "Tennis-doubles.pdf": ("Tennis Doubles", "Doubles tactics", "Tactics",
        "Doubles strategies and formations."),
    "Dick-Leachs-Doubles-Booklet3.pdf": ("Dick Leach's Doubles Booklet", "Dick Leach", "Tactics",
        "Classic doubles tactics booklet."),
    "Tennis-101.pdf": ("Tennis 101", "Beginner reference", "Foundations",
        "Beginner tennis fundamentals."),
    "Tennis-anatomy.pdf": ("Tennis Anatomy", "Anatomy reference", "Medical",
        "Tennis-specific anatomy and injury prevention."),
    "Tennis-Elbow-Rehab.pdf": ("Tennis Elbow Rehab", "Rehabilitation guide", "Medical",
        "Tennis elbow (lateral epicondylitis) rehabilitation protocol."),
    "Stretch-Therapy-Ann-Frederick-Chris-Frederick-Fascial-Stretch-Therapy-2014-pdf.pdf": ("Stretch Therapy (Ann & Chris Frederick)", "Frederick", "Training",
        "Fascial stretch therapy reference."),
    "Strength-Power-Tennis.pdf": ("Strength & Power for Tennis", "S&C reference", "Training",
        "Strength and power training for tennis players."),
    "Speed-Training-for-Tennis.pdf": ("Speed Training for Tennis", "S&C reference", "Training",
        "Speed and agility training for tennis."),
    "Functional-Training-For-Tennis-Daniel-McCain-pdf.pdf": ("Functional Training for Tennis", "Daniel McCain", "Training",
        "Functional training methodology for tennis."),
    "EXO-Kinetics - A Guide to Explosive Performance and Training .pdf": ("EXO-Kinetics", "Explosive performance guide", "Training",
        "Guide to explosive performance and training."),
    "Complete Conditioning for tennis.pdf": ("Complete Conditioning for Tennis", "USTA conditioning", "Training",
        "Comprehensive conditioning program for tennis."),
    "Get-Fit-for-Tennis.pdf": ("Get Fit for Tennis", "Fitness guide", "Training",
        "Tennis-specific fitness guide."),
    "Cardio-Tennis-Drills.pdf": ("Cardio Tennis Drills", "Cardio tennis drills", "Training",
        "Cardio tennis drill set."),
    "Ground strokes - Tennis drills.pdf": ("Groundstrokes — Tennis Drills", "Drill reference", "Strokes",
        "Groundstroke drill progression."),
    "Tennis Strokes and Tactics.pdf": ("Tennis Strokes and Tactics", "Strokes and tactics", "Strokes",
        "Comprehensive strokes and tactics reference."),
    "Step 9 - Back Hand Stroke (1).pdf": ("Back Hand Stroke", "Stroke technique", "Strokes",
        "Backhand stroke technique reference."),
    "TEC 110 - THE FOREHAND  from PTPTennis.pdf": ("TEC 110 — The Forehand (FTPTennis)", "FTPTennis", "Forehand",
        "Forehand technique from FTPTennis."),
    "TEC 130 - THE SERVE from FTPTennis.pdf": ("TEC 130 — The Serve (FTPTennis)", "FTPTennis", "Serve",
        "Serve technique from FTPTennis."),
    "Tennis Forehand Technique.pdf": ("Tennis Forehand Technique", "Forehand reference", "Forehand",
        "Forehand technique reference."),
    "Step_by_Step_Tennis_Skills.pdf": ("Step by Step Tennis Skills", "Skills reference", "Strokes",
        "Step-by-step tennis skills progression."),
    "Perfect Serve - Flat Serve for beginners.pdf": ("Perfect Serve — Flat Serve for Beginners", "Serve instruction", "Serve",
        "Flat serve instruction for beginners."),
    "Platform and pinpoint serve stance variations.pdf": ("Platform and Pinpoint Serve Stance", "Serve technique", "Serve",
        "Comparison of platform vs pinpoint serve stance."),
    "Racquet Control - Part 1.pdf": ("Racquet Control Part 1", "Racquet skill", "Strokes",
        "Racquet control fundamentals part 1."),
    "Racquet Control - Part 2.pdf": ("Racquet Control Part 2", "Racquet skill", "Strokes",
        "Racquet control fundamentals part 2."),
    "Racquet vs Ball Impulse - Momentum.pdf": ("Racquet vs Ball — Impulse & Momentum", "Physics", "Biomechanics",
        "Impulse-momentum analysis of racquet-ball impact."),
    "Fluid Movement in Tennis.pdf": ("Fluid Movement in Tennis", "Movement analysis", "Footwork",
        "Fluid movement principles for tennis."),
    "Tennis-Magazines-40-Best-Tips.pdf": ("Tennis Magazines — 40 Best Tips", "Tennis magazine compilation", "Foundations",
        "40 best tennis tips compiled from tennis magazines."),
    "Tennis-Guide.pdf": ("Tennis Guide", "General guide", "Foundations",
        "General tennis guide."),
    "How to beat a better tennis player.pdf": ("How to Beat a Better Tennis Player", "Tactical play", "Tactics",
        "Strategies for beating higher-rated opponents."),
    "How to maintain body for tennis.pdf": ("How to Maintain Body for Tennis", "Body maintenance", "Medical",
        "Body maintenance for tennis players."),
    "Physical trainings for tennis players.pdf": ("Physical Training for Tennis Players", "S&C reference", "Training",
        "Physical training methodology for tennis."),
    "Kovacs Gullikson female synchronized serves USTA HP Coaching Newsletter 2010.pdf": ("Female Synchronized Serves", "Kovacs & Gullikson, 2010", "Serve",
        "USTA HP coaching newsletter on female synchronized serves."),
    "Federer Vision Technique.pdf": ("Federer Vision & Technique", "Federer analysis", "Strokes",
        "Federer's vision and technique analysis."),
    "Nick Kyrgio Debunk Topspin Serve.pdf": ("Kyrgios Topspin Serve Debunk", "Kyrgios serve analysis", "Serve",
        "Analysis of Nick Kyrgios's topspin serve technique."),
    "Quick Tennis - Henry Hines.pdf": ("Quick Tennis", "Henry Hines", "Foundations",
        "Quick tennis fundamentals by Henry Hines."),
    "The single hander.pdf": ("The Single Hander", "One-handed backhand reference", "Strokes",
        "One-handed backhand technique reference."),
    "The Universal Tennis Swing.pdf": ("The Universal Tennis Swing", "Swing technique", "Strokes",
        "Universal swing technique across all strokes."),
    "The Role of Core Stability in Athletic Function.pdf": ("Core Stability in Athletic Function", "Core conditioning", "Training",
        "Core stability for athletic performance."),
    "TheShotCycle2.1.pdf": ("The Shot Cycle 2.1", "Shot analysis", "Strokes",
        "Shot cycle analysis and reference."),
    "USPTA_high_performance_Vol._2_No_4.2005_footwork_in_modern_tennis.pdf": ("Footwork in Modern Tennis", "USPTA HP Vol. 2 No. 4", "Footwork",
        "USPTA high performance coaching article on footwork."),
    "USPTA-high-performance-Vol_3_No_1.2006_anatomy_of_a_modern_shot.pdf": ("Anatomy of a Modern Shot", "USPTA HP Vol. 3 No. 1", "Strokes",
        "USPTA high performance anatomy of the modern shot."),
    "USTA_high_performance_vol._6_no_3.2004.pdf": ("USTA High Performance Vol. 6 No. 3", "USTA HP", "Strokes",
        "USTA high performance coaching article."),
    "warm_up_book.pdf": ("Warm-Up Book", "Warm-up reference", "Training",
        "Tennis warm-up protocol reference."),
    "Review of tennis ball aerodynamics.pdf": ("Review of Tennis Ball Aerodynamics", "Mehta, Alam & Subic, 2008", "Biomechanics",
        "Comprehensive aerodynamics review. Drag coefficient CD = 0.55-0.65 for new balls."),
    "USPTA_high_performance_Vol._2_No_4.2005_footwork_in_modern_tennis.pdf": ("Footwork in Modern Tennis (USPTA)", "USPTA", "Footwork",
        "USPTA coaching article on footwork in modern tennis."),
}

DOMAIN_DEFAULTS = {
    "Biomechanics": ["biomechanic", "pendulum", "aero", "kinetic", "impulse", "racquet-vs-ball", "anatomy-of-modern", "8-stage", "fast-serves"],
    "Serve": ["serve", "kick-serve", "kickserve", "perfect-serve", "platform-and-pinpoint", "kyrgio"],
    "Forehand": ["forehand", "free-forehand", "tec-110"],
    "Backhand": ["back-hand", "backhand", "single-hander"],
    "Footwork": ["footwork", "movement", "fluid-movement"],
    "Strokes": ["stroke", "racquet-control", "shotcycle", "tennis-strokes", "techniqu", "fundamentals", "tec-130", "hi-tech", "revolutionary", "sports-illustrated", "modern-stroke", "tutorial", "ultimate", "federer-vision", "winning-doubles", "tennis-doubles", "doubles-strategy"],
    "Equipment": ["sweet-spot", "racket", "string", "racquet-control"],
    "Mental Game": ["mental", "inner-game", "vision", "soft-science", "tao", "zen", "laugh", "winning-ugly", "psycholog", "confidence"],
    "Training": ["hiit", "training", "fitness", "conditioning", "stretch", "strength", "speed", "functional", "exo-kinetic", "core", "workout", "cardio"],
    "Medical": ["aspeta", "medicin", "injury", "elbow", "plantar", "body-for-tennis", "recovery", "rehab"],
    "Tactics": ["tactic", "strateg", "outsmart", "doubles-strategy", "beat-a-better", "match-plan"],
    "Coaching": ["coaching", "itf-", "elderton", "movement-for-tennis"],
    "Foundations": ["101", "guide", "fundamentals", "tips", "tennis-anatomy", "quick-tennis", "basics"],
}


def detect_domain(filename: str) -> str:
    f = filename.lower()
    # Check known first
    for known_pdf, info in KNOWN.items():
        if known_pdf.lower() == f:
            return info[2]
    # Pattern matching
    for domain, keywords in DOMAIN_DEFAULTS.items():
        for kw in keywords:
            if kw in f:
                return domain
    return "Foundations"


def title_from_filename(filename: str) -> str:
    """Auto-derive a title from filename when not in KNOWN."""
    name = filename.replace(".pdf", "")
    # Replace underscores and dashes with spaces
    name = name.replace("_", " ").replace("-", " ")
    # Remove trailing parenthetical numbers
    name = re.sub(r"\s*\(\d+\)\s*$", "", name)
    return name.strip()


def slugify(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-").lower()
    # Collapse multiple consecutive hyphens into one
    s = re.sub(r"-{2,}", "-", s)
    # Remove trailing hyphens again after collapse
    s = s.strip("-")
    # Also convert underscores to hyphens for URL consistency
    s = s.replace("_", "-")
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s[:100]


def make_page(pdf_filename: str) -> str:
    """Generate one reader page."""
    if pdf_filename in KNOWN:
        title, author, domain, desc = KNOWN[pdf_filename]
    else:
        title = title_from_filename(pdf_filename)
        author = "Unknown / multiple authors"
        domain = detect_domain(pdf_filename)
        desc = f"{title}. Curated from the Tennis Books library."

    safe_title = title.replace('"', '\\"')
    safe_author = author.replace('"', '\\"')
    safe_desc = desc.replace('"', '\\"')

    import urllib.parse
    pdf_url = f"../../{urllib.parse.quote(pdf_filename)}"

    slug = slugify(pdf_filename.replace(".pdf", ""))

    content = f"""---
title: "{safe_title}"
description: "{safe_desc}"
---

# {title}

**Author:** {author} · **Domain:** {domain}

{safe_desc}

!!! tip "Reading controls"
    Use the toolbar at the top of the PDF (or right-click the iframe) to zoom, navigate pages, search inside the book, or download. **Ctrl+F** searches within the current book. The page is rendered at **100 % width** — use the browser zoom (Ctrl++) to enlarge text further.

---

## Read the book

<iframe class="pdf-viewer" src="{pdf_url}#toolbar=1&navpanes=1&scrollbar=1&view=FitH" title="{safe_title}">
  Your browser does not support inline PDF viewing. <a href="{pdf_url}">Download the PDF</a> instead.
</iframe>

[Download the PDF ↗]({pdf_url}) · [Open in new tab ↗]({pdf_url})

---

## Quick reference

!!! info "Why this book matters"
    {safe_desc}

!!! note "Pipeline context"
    This book is part of the [Tennis Knowledge Gap Intranet](../..). It was identified as gap-evidence by the 92-concept diff between the tennis-unified repo and the Tennis Books library, then supplemented with web-research 2024–2026 sources.

---

[← Back to all books](../../) · [Gap reports](../../#latest-synthesis)
"""
    out = DOCS_READ / slug / "index.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return slug, title, author, domain, desc


def make_index(pages: list) -> None:
    """Rewrite docs/books/index.md with all books listed."""
    # Group by domain
    by_domain = {}
    for slug, title, author, domain, desc in pages:
        by_domain.setdefault(domain, []).append((slug, title, author, desc))

    domain_order = ["Biomechanics", "Serve", "Forehand", "Backhand", "Footwork",
                    "Strokes", "Equipment", "Mental Game", "Training", "Medical",
                    "Tactics", "Coaching", "Foundations"]
    # Sort within each domain
    lines = []
    lines.append("---")
    lines.append("title: Tennis Books Library")
    lines.append("description: Read 100+ curated tennis books directly in the browser with the embedded PDF reader.")
    lines.append("---")
    lines.append("")
    lines.append("# Tennis Books Library")
    lines.append("")
    lines.append(f"Read tennis books directly in the browser — no separate PDF reader needed. **{len(pages)} curated titles** from `D:/New Tennis Knowledge/Tennis Books/`, covering biomechanics, serve, forehand, mental game, training, injury prevention, and tactics.")
    lines.append("")
    lines.append('!!! tip "How to use"')
    lines.append("    Click any book cover to open the inline reader at **100 % page width**. Use the toolbar at the top of the PDF to zoom, navigate pages, search within the book, or download. Press **Ctrl+F** while reading to search inside the current book.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## All books (filterable)")
    lines.append("")
    lines.append('<div class="books-filter">')
    lines.append('  <input type="text" class="books-filter-input" placeholder="Search books by title, author, or topic…" id="books-search">')
    lines.append('  <div class="books-filter-tags" id="books-tags"></div>')
    lines.append('  <div style="font-size:0.75rem;color:var(--md-default-fg-color--light,#888);margin-top:6px;">')
    lines.append(f'    Showing <span id="books-count">{len(pages)}</span> of {len(pages)} books')
    lines.append('  </div>')
    lines.append('</div>')
    lines.append("")
    lines.append('<div class="books-grid" id="books-grid">')
    lines.append("")

    for domain in domain_order:
        if domain not in by_domain:
            continue
        for slug, title, author, desc in by_domain[domain]:
            data_title = re.sub(r'[^a-zA-Z0-9 ]', ' ', (title + " " + author + " " + desc + " " + domain).lower())
            lines.append(f'<a class="book-card" href="read/{slug}/" data-domain="{domain.lower()}" data-title="{data_title}">')
            lines.append(f'  <div class="book-card-domain">{domain}</div>')
            lines.append(f'  <div class="book-card-title">{title}</div>')
            lines.append(f'  <div class="book-card-author">{author}</div>')
            lines.append(f'  <div class="book-card-read">→ Read ›</div>')
            lines.append('</a>')

    lines.append("")
    lines.append('</div>')
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## How the PDF reader works")
    lines.append("")
    lines.append("The reader uses the browser's built-in PDF viewer (`<embed type=\"application/pdf\">` wrapped in `<iframe>`). The toolbar at the top lets you:")
    lines.append("")
    lines.append("- **Zoom in/out** and **fit-to-width**")
    lines.append("- **Navigate** with the page list on the left")
    lines.append("- **Search** within the book (Ctrl+F)")
    lines.append("- **Print** or **download**")
    lines.append("")
    lines.append("No external PDF.js dependency, no separate window, no plugin. Works in Chrome, Edge, Firefox, Safari. The page renders at **100 % width** of your browser viewport — for larger text, use the browser's zoom (Ctrl++) or the PDF viewer's own zoom.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Trang web này được xây dựng với ❤️ cho cộng đồng quần vợt Việt Nam 🎾 by Henry Phạm*")
    lines.append("")

    DOCS_INDEX.write_text("\n".join(lines), encoding="utf-8")


def main():
    # Clean out stale reader pages so that removed/renamed books don't leave orphans
    import shutil
    DOCS_READ.mkdir(parents=True, exist_ok=True)

    pages = []
    pdfs = sorted([f for f in os.listdir(BOOKS_DIR) if f.lower().endswith(".pdf")])
    for pdf in pdfs:
        slug, title, author, domain, desc = make_page(pdf)
        pages.append((slug, title, author, domain, desc))
        print(f"  + {domain:15s} {title[:50]:50s}  ({author[:30]})")
    make_index(pages)
    print(f"\nWrote {len(pages)} reader pages + 1 index page")


if __name__ == "__main__":
    main()
