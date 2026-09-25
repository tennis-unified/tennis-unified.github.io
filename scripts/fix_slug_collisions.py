#!/usr/bin/env python3
"""
Fix Slug Collision Bug — Remove truncated directory duplicates
Run this BEFORE deploying to clean up the 64-char filesystem limit remnants.
"""

import os
import shutil
from pathlib import Path

BASE = Path(r"D:\Github Repos\tennis-unified")

# Truncated slugs that should be REMOVED (keep the full versions)
TRUNCATED_TO_REMOVE = {
    "vi": [
        "VI-tenniskb-brain-derived-neurotrophic-factor-bdnf-and-motor-skill-acqui",
        "VI-tenniskb-cognitive-load-reduction-through-automated-tactical-heuristi",
        "VI-tenniskb-heart-rate-variability-hrv-and-autonomic-nervous-state-regul",
        "VI-tenniskb-inter-hemispheric-brain-synchronization-in-bilateral-movemen",
        "VI-tenniskb-neural-myelination-through-high-density-precision-repetition",
    ],
    "en": [
        "EN-tenniskb-brain-derived-neurotrophic-factor-bdnf-and-motor-skill-acqui",
        "EN-tenniskb-cognitive-load-reduction-through-automated-tactical-heuristi",
        "EN-tenniskb-heart-rate-variability-hrv-and-autonomic-nervous-state-regul",
        "EN-tenniskb-inter-hemispheric-brain-synchronization-in-bilateral-movemen",
        "EN-tenniskb-neural-myelination-through-high-density-precision-repetition",
    ]
}

# Full slugs that should be KEPT
FULL_SLUGS = {
    "vi": [
        "VI-tenniskb-brain-derived-neurotrophic-factor-bdnf-and-motor-skill-acquisition",
        "VI-tenniskb-cognitive-load-reduction-through-automated-tactical-heuristics",
        "VI-tenniskb-heart-rate-variability-hrv-and-autonomic-nervous-state-regulation",
        "VI-tenniskb-inter-hemispheric-brain-synchronization-in-bilateral-movements",
        "VI-tenniskb-neural-myelination-through-high-density-precision-repetitions",
    ],
    "en": [
        "EN-tenniskb-brain-derived-neurotrophic-factor-bdnf-and-motor-skill-acquisition",
        "EN-tenniskb-cognitive-load-reduction-through-automated-tactical-heuristics",
        "EN-tenniskb-heart-rate-variability-hrv-and-autonomic-nervous-state-regulation",
        "EN-tenniskb-inter-hemispheric-brain-synchronization-in-bilateral-movements",
        "EN-tenniskb-neural-myelination-through-high-density-precision-repetitions",
    ]
}

def main():
    print("=" * 60)
    print("FIXING SLUG COLLISION BUG")
    print("=" * 60)
    
    total_removed = 0
    total_kept = 0
    
    for lang in ["vi", "en"]:
        articles_dir = BASE / lang / "articles"
        if not articles_dir.exists():
            print(f"\n⚠️  {lang}/articles not found")
            continue
        
        print(f"\n--- {lang.upper()} ---")
        
        # Remove truncated
        for slug in TRUNCATED_TO_REMOVE[lang]:
            slug_path = articles_dir / slug
            if slug_path.exists():
                print(f"  REMOVING truncated: {slug}")
                try:
                    shutil.rmtree(slug_path)
                    total_removed += 1
                except Exception as e:
                    print(f"     ERROR: {e}")
            else:
                print(f"  Already absent: {slug}")
        
        # Verify full slugs exist
        for slug in FULL_SLUGS[lang]:
            slug_path = articles_dir / slug
            if slug_path.exists():
                print(f"  Full slug present: {slug}")
                total_kept += 1
            else:
                print(f"  Full slug MISSING: {slug}")
    
    print("\n" + "=" * 60)
    print(f"SUMMARY: {total_removed} truncated dirs removed, {total_kept} full dirs verified")
    print("=" * 60)
    
    if total_removed > 0:
        print("\nCleanup complete. Now rebuild mkdocs and verify index.html links.")
    else:
        print("\nNo truncated dirs found -- already clean.")

if __name__ == "__main__":
    main()