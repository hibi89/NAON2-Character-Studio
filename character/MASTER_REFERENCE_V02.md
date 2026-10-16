# NAON2 Master Reference v0.2 — comparison only

## Source of truth
- Gamer original (A): primary face and overall identity anchor
- Astronaut original (B): action and variation reference
- Approved concept sheet (C): user-approved visual guide, **flattened** rather than editable independent artwork

## Work completed, 2026-10-16
The approved 1536 × 1024 sheet was cropped into 3 viewpoints (front, side, back) and 5 expressions (neutral, smile, surprised, curious, wink). A comparison board was generated locally.

Crops preserve their original pixels and have reproducible source coordinates in `scripts/extract_reference_crops.py`.

## Hard limits
- Some tails or neighboring figures may overlap crop boundaries because the source sheet is flattened.
- Enlarging a preview does not restore resolution or create a high-resolution independent drawing.
- The image's generated HEX labels are not confirmed color standards.
- None of the cropped outputs is an official master image or approved sales deliverable.

## Reproducibility
- `python scripts/verify_assets.py` checks the three original/reference PNGs
- `python scripts/extract_reference_crops.py` creates the exact reference regions from the approved sheet
- The v0.2 comparison board and raw crops are in the user-downloadable project ZIP; GitHub binary image uploads are still pending

## Path to official v1.0 master
1. Produce independent full-body front, side and back illustrations, without clothing, equipment or background scene.
2. Preserve face shape, eye spacing, muzzle, gray/white fur mask, pink ears and full curved tail across all 3 views.
3. Obtain a clean editable source where possible (separate layers preferred), not a collage crop.
4. Confirm real output resolution, artifact-free anatomy, commercial usage rights and user visual approval.
5. Record approved asset checksums, then derive themed art.

## Stop-and-pivot result
Two image-generation attempts returned **6-theme promotional collages** rather than requested independent turnaround drawings. No further identical attempt; collages retained only as unapproved drafts. A reference-aware editor or source-layer workflow should be evaluated for the true master.
