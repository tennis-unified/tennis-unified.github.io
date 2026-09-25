#!/usr/bin/env python3
"""
Deployment Verification Script for Tennis Unified Knowledge Base
Run after mkdocs build to verify all 10 new Vietnamese articles are deployed correctly.
"""

import os
import sys
from pathlib import Path

BASE = Path(r"D:\Github Repos\tennis-unified")

# The 42 Vietnamese articles with markdown (034-080)
NEW_VI_ARTICLES = [
    "VI-tenniskb-kinetic-transfer-from-quad-drive-to-pelvic-acceleration",
    "VI-tenniskb-torque-vector-generation-in-open-vs-closed-stances",
    "VI-tenniskb-gravitational-acceleration-utilization-in-drop-feeds",
    "VI-tenniskb-passive-ligamentous-locking-vs-active-muscle-tension",
    "VI-tenniskb-rotational-inertia-adjustment-during-mid-swing-tracking",
    "VI-tenniskb-kinetic-chain-peak-power-phase-alignment",
    "VI-tenniskb-biomechanical-efficiency-audits-for-stroke-longevity",
    "VI-tenniskb-quiet-eye-qe-fixing-visual-anchors-before-impact",
    "VI-tenniskb-vestibular-ocular-reflex-vor-and-head-stabilization",
    "VI-tenniskb-proprioceptive-feedback-loops-in-high-velocity-tracking",
    "VI-tenniskb-amygdala-hijack-mitigation-under-match-pressure",
    "VI-tenniskb-subconscious-motor-program-recruitment-self-1-vs-self-2",
    "VI-tenniskb-spatial-awareness-and-anticipatory-visual-cues",
    "VI-tenniskb-pre-point-routines-and-sympathetic-modulation",
    "VI-tenniskb-neuro-priming-protocols-for-explosive-first-step-readiness",
    "VI-tenniskb-sensory-gating-and-background-noise-suppression",
    "VI-tenniskb-temporal-perception-and-slower-ball-tracking-in-flow-states",
    "VI-tenniskb-neural-myelination-through-high-density-precision-repetitions",
    "VI-tenniskb-peripheral-vision-expansion-in-court-coverage",
    "VI-tenniskb-cognitive-load-reduction-through-automated-tactical-heuristics",
    "VI-tenniskb-neuro-muscular-fatigue-cues-and-impact-on-timing",
    "VI-tenniskb-saccadic-eye-movement-vs-smooth-pursuit-in-ball-tracking",
    "VI-tenniskb-de-escalation-protocols-for-choking-and-motor-inhibitions",
    "VI-tenniskb-visual-anchor-shifts-from-ball-seams-to-opponent-hip-cues",
    "VI-tenniskb-proprioceptive-joint-position-sense-under-high-lactate",
    "VI-tenniskb-mental-imagery-and-cerebellar-motor-schema-simulation",
    "VI-tenniskb-focal-attention-vs-global-spatial-awareness-in-rallying",
    "VI-tenniskb-micro-recovery-interventions-between-points-25-second-audit",
    "VI-tenniskb-affordance-perception-reading-ball-trajectories-instantly",
    "VI-tenniskb-sensory-deprivation-and-visual-goggle-training-methods",
    "VI-tenniskb-neural-drive-optimization-during-serve-acceleration",
    "VI-tenniskb-inter-hemispheric-brain-synchronization-in-bilateral-movements",
    "VI-tenniskb-reaction-time-priming-via-auditory-tennis-cues",
    "VI-tenniskb-stress-resilience-and-cortisol-buffering-during-tiebreakers",
    "VI-tenniskb-somatosensory-feedback-and-racket-face-angle-awareness",
    "VI-tenniskb-conscious-override-elimination-in-reaction-volleys",
    "VI-tenniskb-neuro-visual-tracking-under-stadium-lighting-variations",
    "VI-tenniskb-cognitive-flexibility-in-mid-point-strategy-pivots",
    "VI-tenniskb-executive-function-maintenance-into-5th-set-conditions",
    "VI-tenniskb-neuromuscular-junction-efficiency-and-acetylcholine-dynamics",
    "VI-tenniskb-subconscious-micro-adjustments-in-unpredictable-bounces",
    "VI-tenniskb-neuro-athletic-profiling-for-individualized-coaching-design",
]

# Truncated slugs that should NOT exist (slug collision bug)
TRUNCATED_SLUGS = [
    "VI-tenniskb-brain-derived-neurotrophic-factor-bdnf-and-motor-skill-acqui",
    "VI-tenniskb-cognitive-load-reduction-through-automated-tactical-heuristi",
    "VI-tenniskb-heart-rate-variability-hrv-and-autonomic-nervous-state-regul",
    "VI-tenniskb-inter-hemispheric-brain-synchronization-in-bilateral-movemen",
    "VI-tenniskb-neural-myelination-through-high-density-precision-repetition",
    "EN-tenniskb-brain-derived-neurotrophic-factor-bdnf-and-motor-skill-acqui",
    "EN-tenniskb-cognitive-load-reduction-through-automated-tactical-heuristi",
    "EN-tenniskb-heart-rate-variability-hrv-and-autonomic-nervous-state-regul",
    "EN-tenniskb-inter-hemispheric-brain-synchronization-in-bilateral-movemen",
    "EN-tenniskb-neural-myelination-through-high-density-precision-repetition",
]

def check_source_markdown():
    """Verify source .md files exist in vi/articles/"""
    print("=" * 60)
    print("CHECKING SOURCE MARKDOWN FILES (vi/articles/)")
    print("=" * 60)
    all_ok = True
    for slug in NEW_VI_ARTICLES:
        md_path = BASE / "vi" / "articles" / slug / "index.md"
        if md_path.exists():
            size = md_path.stat().st_size
            print(f"  OK {slug} ({size:,} bytes)")
        else:
            print(f"  MISSING {slug}")
            all_ok = False
    return all_ok

def check_built_html(site_dir="site"):
    """Verify built HTML files exist in site/ directory"""
    print("\n" + "=" * 60)
    print(f"CHECKING BUILT HTML FILES ({site_dir}/)")
    print("=" * 60)
    site_path = BASE / site_dir
    if not site_path.exists():
        print(f"  WARNING Build directory '{site_dir}' not found. Run 'mkdocs build' first.")
        return False
    
    all_ok = True
    for slug in NEW_VI_ARTICLES:
        html_path = site_path / "vi" / "articles" / slug / "index.html"
        if html_path.exists():
            size = html_path.stat().st_size
            print(f"  OK {slug} ({size:,} bytes)")
        else:
            print(f"  NOT BUILT {slug}")
            all_ok = False
    return all_ok

def check_truncated_slugs():
    """Verify truncated slug directories have been removed"""
    print("\n" + "=" * 60)
    print("CHECKING FOR TRUNCATED SLUGS (should NOT exist)")
    print("=" * 60)
    all_ok = True
    for lang in ["vi", "en"]:
        articles_dir = BASE / lang / "articles"
        if not articles_dir.exists():
            continue
        for slug in TRUNCATED_SLUGS:
            if slug.startswith(lang[:2]):
                slug_path = articles_dir / slug
                if slug_path.exists():
                    print(f"  STILL EXISTS {lang}/{slug} (DELETE IT)")
                    all_ok = False
                else:
                    print(f"  REMOVED {lang}/{slug}")
    return all_ok

def check_navigation_links():
    """Verify prev/next navigation in a sample article"""
    print("\n" + "=" * 60)
    print("CHECKING NAVIGATION LINKS (sample: article 034)")
    print("=" * 60)
    md_path = BASE / "vi" / "articles" / "VI-tenniskb-kinetic-transfer-from-quad-drive-to-pelvic-acceleration" / "index.md"
    if md_path.exists():
        content = md_path.read_text(encoding="utf-8")
        # Check frontmatter
        if 'prev_article: "VI-tenniskb-passive-ligamentous-locking-vs-active-muscle-tension"' in content:
            print("  OK prev_article correctly set to article 037")
        else:
            print("  FAIL prev_article missing or incorrect")
        
        if 'next_article: "VI-tenniskb-torque-vector-generation-in-open-vs-closed-stances"' in content:
            print("  OK next_article correctly set to article 035")
        else:
            print("  FAIL next_article missing or incorrect")
        
        # Check pillar
        if 'pillar: "co-sinh-hoc"' in content:
            print("  OK pillar correctly set to co-sinh-hoc")
        else:
            print("  FAIL pillar missing or incorrect")
        
        # Check article number
        if 'article_number: 34' in content:
            print("  OK article_number correctly set to 34")
        else:
            print("  FAIL article_number missing or incorrect")
        return True
    return False

def check_mathjax_content():
    """Verify LaTeX math content is preserved"""
    print("\n" + "=" * 60)
    print("CHECKING MATHJAX/LATEX CONTENT PRESERVATION")
    print("=" * 60)
    all_ok = True
    test_patterns = ["F<sub>z</sub>", "F<sub>x</sub>", "F<sub>y</sub>", "η =", "α = τ/I", "≤30 ms"]
    
    for slug in NEW_VI_ARTICLES[:3]:  # Check first 3 as sample
        md_path = BASE / "vi" / "articles" / slug / "index.md"
        if md_path.exists():
            content = md_path.read_text(encoding="utf-8")
            found = sum(1 for p in test_patterns if p in content)
            print(f"  {slug}: {found}/{len(test_patterns)} math patterns found")
            if found == 0:
                all_ok = False
    return all_ok

def main():
    print("\n" + "=" * 60)
    print("TENNIS UNIFIED KB -- DEPLOYMENT VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Source Markdown Files", check_source_markdown),
        ("Built HTML Files", lambda: check_built_html("site")),
        ("Truncated Slugs Removed", check_truncated_slugs),
        ("Navigation Links", check_navigation_links),
        ("MathJax Content", check_mathjax_content),
    ]
    
    results = []
    for name, check_fn in checks:
        try:
            result = check_fn()
            results.append((name, result))
        except Exception as e:
            print(f"  ERROR in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    all_passed = all(r[1] for r in results)
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {status} -- {name}")
    
    if all_passed:
        print("\nALL CHECKS PASSED -- Deployment ready!")
        return 0
    else:
        print("\nSOME CHECKS FAILED -- Review before deploying")
        return 1

if __name__ == "__main__":
    sys.exit(main())