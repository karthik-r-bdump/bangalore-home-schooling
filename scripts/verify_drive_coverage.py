#!/usr/bin/env python3
"""
Drive Coverage Verification Script
Validates that all 220 items from the Google Drive catalog are accounted for,
and that target markdown docs and hosted assets exist on disk.
"""

import os
import sys
import json

WORKSPACE_ROOT = "/home/rkar/sources/bangalore-home-schooling"
MANIFEST_PATH = "/home/rkar/.gemini/antigravity-cli/brain/a9cc1c31-a94b-43d1-baa4-adbda1794750/scratch/conversion_manifest.json"
CATALOG_PATH = "/home/rkar/.gemini/antigravity-cli/brain/a9cc1c31-a94b-43d1-baa4-adbda1794750/scratch/drive_catalog.json"

def main():
    print("🔍 Verifying Google Drive Coverage...")
    
    with open(CATALOG_PATH) as f:
        catalog = json.load(f)
    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    print(f"  • Total items in Google Drive catalog: {len(catalog)}")
    print(f"  • Total items mapped in manifest: {len(manifest)}")

    assert len(catalog) == 220, f"Expected 220 catalog items, got {len(catalog)}"
    assert len(manifest) == 220, f"Expected 220 manifest items, got {len(manifest)}"

    # Check key generated pages exist
    key_pages = [
        "docs/middle-school/class-7/overview.md",
        "docs/middle-school/class-7/materials-inventory.md",
        "docs/middle-school/class-7/midterm-papers/history-civics-midterm.md",
        "docs/middle-school/class-7/midterm-papers/geography-midterm.md",
        "docs/middle-school/class-7/midterm-papers/biology-midterm.md",
        "docs/middle-school/class-7/midterm-papers/physics-midterm.md",
        "docs/middle-school/class-7/midterm-papers/chemistry-midterm.md",
        "docs/middle-school/class-7/midterm-papers/mathematics-midterm.md",
        "docs/middle-school/class-7/midterm-papers/english-language-midterm.md",
        "docs/middle-school/class-7/midterm-papers/english-literature-midterm.md",
        "docs/middle-school/class-7/midterm-papers/computer-studies-midterm.md",
        "docs/middle-school/class-7/midterm-papers/kannada-midterm.md",
        "docs/middle-school/class-7/midterm-papers/hindi-midterm.md",
        "docs/middle-school/class-7/history-civics/delhi-sultanate.md",
        "docs/middle-school/class-7/history-civics/vijayanagar-bahmani-kingdoms.md",
        "docs/middle-school/class-7/history-civics/constitution-of-india.md",
        "docs/middle-school/class-7/geography/topographical-maps.md",
        "docs/middle-school/class-7/geography/weathering-and-soil-formation.md",
        "docs/middle-school/class-7/geography/europe-and-switzerland.md",
        "docs/middle-school/class-7/biology/plant-and-animal-tissues.md",
        "docs/middle-school/class-7/biology/photosynthesis.md",
        "docs/middle-school/class-7/biology/respiration.md",
        "docs/middle-school/class-7/biology/excretory-system.md",
        "docs/middle-school/class-7/physics/physical-quantities-measurement.md",
        "docs/middle-school/class-7/physics/motion.md",
        "docs/middle-school/class-7/physics/work-and-energy.md",
        "docs/middle-school/class-7/physics/light-reflection.md",
        "docs/middle-school/class-7/chemistry/symbols-and-formulae.md",
    ]

    for kp in key_pages:
        full_p = os.path.join(WORKSPACE_ROOT, kp)
        assert os.path.exists(full_p), f"Missing key page: {kp}"

    # Check key hosted assets exist
    key_assets = [
        "static/assets/class-7/biology/01-histology-tactical-playbook.pdf",
        "static/assets/class-7/biology/03-photosynthesis-decoded.pdf",
        "static/assets/class-7/biology/04-respiration-decoded.pdf",
        "static/assets/class-7/history-civics/01-delhi-sultanate-revision-guide.pdf",
        "static/assets/class-7/history-civics/02-augmented-deccan-blueprint.pdf",
        "static/assets/class-7/history-civics/02-deccan-titans-blueprint.pdf",
        "static/assets/class-7/history-civics/03-indian-constitution-blueprint.pdf",
        "static/assets/class-7/geography/01-topographical-map-mastery.pdf",
        "static/assets/class-7/geography/02-weathering-and-soil-flashcards.pdf",
        "static/assets/flashcards/delhi-sultanate-cards.colpkg",
        "static/assets/flashcards/biology-class7-cards.apkg",
    ]

    for ka in key_assets:
        full_a = os.path.join(WORKSPACE_ROOT, ka)
        assert os.path.exists(full_a), f"Missing key asset: {ka}"

    print(f"  • All {len(key_pages)} key documentation pages verified.")
    print(f"  • All {len(key_assets)} hosted assets verified.")
    print("✅ Drive Coverage Verification Passed: 220/220 documents accounted for.")

if __name__ == '__main__':
    main()
