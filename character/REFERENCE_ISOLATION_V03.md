# NAON2 transparent isolation v0.3 — verification and use

## Actual artifacts
- `assets/derivatives/reference-isolates-v03/naon2-front-reference-v03.png`: 214 × 213 native pixels, transparent RGBA
- `assets/derivatives/reference-isolates-v03/naon2-three-quarter-reference-v03.png`: 185 × 216 native pixels, transparent RGBA
- `assets/derivatives/reference-isolates-v03/naon2-back-reference-v03.png`: 213 × 215 native pixels, transparent RGBA
- `assets/derivatives/reference-isolates-v03/naon2-three-view-preview-v03.png`: contact sheet (enlarged presentation only)
- `assets/derivatives/reference-isolates-v03/reference-v03-manifest.json`: byte sizes and SHA-256 of native transparent PNGs

## Verified provenance
Source: user-approved `assets/references/naon2-character-sheet-v1.png`.
The source was not modified. The script uses fixed source rectangles + OpenCV GrabCut, single connected silhouette, hole filling and feathered alpha edge. This is an **extraction**, not a redraw and not a new high-resolution original.

## QA
- Local source SHA-256/size verification: PASS 3/3 source images.
- Each separate subject is fully inside its crop, contains transparent outside pixels and opaque inside pixels: PASS 3/3.
- OpenCV silhouettes preserve all paws, ears and tails visible in approved sheet: visually checked.
- GitHub Actions: `success`, run `38909850479`.
- GitHub remote `main`: generated PNGs committed `b2ffd9381e75c9fa1134b60a8dc84f9920f89ad0`.
- Remote file blob SHA compared to local generated file blob SHA: PASS 3/3 exact-byte match.

## Limits
- The "side" in the approved flattened sheet is a **three-quarter perspective**, not full 90° side.
- The display board enlarges images using interpolation but adds no native detail.
- GrabCut removes/reconstructs the border alpha and may discard some original edge pixels.
- Not layered art, not standalone 2K original masters, not commercial delivery artwork.
- Separate reference-aware redraw/manual illustration is needed before final official master approval.

## Reproduce
`python -m pip install -r requirements-reference.txt`

`python scripts/verify_assets.py`

`python scripts/isolate_model_references.py`

Workflow: `.github/workflows/naon2-reference-cutouts.yml`.
