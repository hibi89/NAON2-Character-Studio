# NAON2 vector art redraw v0.1 — REVIEW DRAFT

## Why this approach
Three attempts using the generic image generation workflow returned marketing collages instead of a standalone 3-view master. Rather than retry, the cat was **independently hand-constructed as editable SVG paths** based on the approved original concept art.

## Asset set
- Front, true side (90°) and back **three separate SVG vector artworks**
- 2048×2048 PNG, transparent background for each SVG
- Generator source: `scripts/build_vector_masters.py`
- Quality gate script: `scripts/verify_vector_masters.py`
- Output: `assets/masters/vector-v01/`

## Design invariants
- Gray brown head and back, white lower cheeks / bib / paws, pink ears and nose
- Oversized glossy warm-brown eyes on front, single eye on side
- Short and stout sitting chibi cat with **one** curled fluffy tail and warmer brown tail tip
- No clothing, props, background objects or text

## Important limitations
- **NOT** pixel-identical to gamer/astronaut original or the approved flattened sheet
- Render treatment is cleaner/flatter SVG art, unlike the soft rendered source image
- Vector rendering at 2K produces clean shapes at 2K but **does not make the old 208px image contain new photorealistic detail**
- No claim that design similarity or intellectual property usage has been finally approved
- These files are draft masters. Do not mark as `official` or `for sale` until user approves exact appearance and license review is complete

## Local/CI validation
`python scripts/build_vector_masters.py`, then `python scripts/verify_vector_masters.py`

Both editable vector source and exports are versioned, and the original images are never overwritten.
