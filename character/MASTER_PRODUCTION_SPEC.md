# NAON2 Single-Character Master — Production Spec v0.3

## Objective
Create three **independent, high-resolution, complete-body** NAON2 cat illustrations: `front`, `side`, and `back`. The approved character must remain recognizable as the same cat. These are masters for later themed derivatives, not a poster, infographic or promotional collage.

## Reference order
1. `assets/originals/naon2-gamer-original.png`: primary eye/muzzle/head identity reference
2. `assets/originals/naon2-astronaut-original.png`: secondary tail/body/alternate perspective
3. `assets/references/naon2-character-sheet-v1.png`: user-approved design style; **flattened** raster, not a set of separate editable masters

## Hard identity invariants
- Gray crown/back, white lower face/bib/chest; keep the distinct facial boundary and markings.
- Very large round dark eyes with warm brown irises, small rosy-pink nose, soft rounded muzzle.
- Triangular ears, pink inner ears; large rounded head, tiny chibi body, short paws.
- Thick, fluffy curled tail; same base fur pattern across all angles.
- Keep warm expressive stylization; no new stripes/spots, no change of breed, no anthropomorphic human proportions.

## Required outputs
- Output **one view at a time**, not combined character charts.
- Front: full body, neutral expression, both eyes visible, both ears and tail fully inside the frame.
- Side: full body true 90-degree profile, muzzle/nose clearly in profile, tail fully visible; maintain same fur mask.
- Back: full body facing away, ears and complete curled tail visible, paw/body proportions match front/side.
- No hoodie, astronaut suit, headset, eyeglasses, backpack, props, environmental scenery or text.
- Consistent camera distance and white/off-white background for clean comparison.
- Recommended native target: at least 2048px on longest side **if supported natively by selected generation/editing tool**. Do not treat upscaling as native detail.
- Save PNG with versioned names `naon2-master-front-v01.png`, etc. Preserve exact generation settings and source rights.

## Quality gates
`character/QUALITY_GATE.md` defines pass/fail criteria. Require side-by-side inspection with A/B/C; reject non-NAON2 cats, incomplete body, cut-off limbs/tail, extra features, low-resolution defects, and character drift.

## Implementation options and stop-pivot
| Option | Speed | Cost | Character fidelity | Constraint |
| --- | --- | --- | --- | --- |
| A. Image reference-aware single-image editing workflow | Medium | Tool-dependent | Higher chance of close consistency | Specific tool must be verified, may require external upload and approval |
| B. Manually recreated layered master based on approved references | Slower | Typically higher | Highest control and editability | Needs artist-grade source editing and more labor |

**Recommendation:** Test A first only after confirming reference-image input is actually used. If two materially different attempts do not produce standalone single-view artwork, stop and pivot to B. Prior image generation in this chat produced marketing collages twice despite requesting master turnarounds; those are NOT valid master candidates.

### Review status (2026-10-16)
- Master 3-view: Not produced
- User-approved master: Not yet
- Commercial-ready derivatives: Not yet
