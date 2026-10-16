# NAON2 Side / Back Test v0.1 — QA failure and next pivot

Date: 2026-10-16. **Neither generated view is a production master.**

## Input anchor and expectations
- Selected frontal direction: `assets/candidates/front-v02/naon2-front-candidate-v02-raw.png` (1254x1254 RGBA, **not yet uploaded to GitHub**)
- Approved concept: `assets/references/naon2-character-sheet-v1.png` (do not modify)
- Target for this test: one independent complete 90-degree side illustration, consistent eyes/ears/fur, body/tail, native high resolution and true alpha transparency, then back view.

## What actually happened
An image-generation call produced a **wide multi-view infographic sheet**, not the requested standalone side master. It included labels claiming "v2 finalized", "2048x2048" and "commercial ready". Those words are part of generated artwork, **not factual validation**.

Source sheet measured **2172x724 RGBA**; alpha values are in the range **207..252**, so the checkerboard was effectively baked into the artwork. Individual rough crops measured:
- Side: **350x332** pixels. Facing left, recognizably similar coloring, but tail **cut off at right panel edge**.
- Back: **323x333** pixels. Tail **cut off at right panel edge**.
- These are not independent layered drawings or native 2K images.

The local QA comparison board shows front v2 vs the extracted side/back, with errors flagged. Artifacts are in conversation download `NAON2-side-back-review-v01.zip`. This GitHub document contains the test report, **not the unapproved binary sheet**.

## Verdict
- Side candidate: **REJECTED as master**; illustration guide only.
- Back candidate: **REJECTED as master**; illustration guide only.
- Frontal v2: unchanged.
- Original A/B images and approved design sheet: unchanged.
- Commercial production, resale rights, licensing, exact pixel fidelity: **not verified**.

## Stop and pivot
Do not request another "turnaround sheet" using the same image generation route. Next viable options:

| Strategy | Pros | Costs/constraints |
| --- | --- | --- |
| A. Single-view source-aware precision edit/outpaint (recommended) | Higher chance of preserving front v2 identity; target one image and protect full tail | Must verify actual image reference use, may require approved external tool and input transfer |
| B. Artist-grade manual redraw with editable layered file | Highest manual control over silhouette and fur transitions | Higher labor, risk of reinterpretation, external cost may apply |

Make a full 90-degree side view with all four canvas edges safe, no text and real transparency. Verify by visual comparison to front v2 **before** making a back view or six commercial themes.

## Blocking prerequisite
Upload the unchanged frontal v2 candidate PNG once to private GitHub at
`assets/candidates/front-v02/naon2-front-candidate-v02-raw.png`.
A workflow already exists in `.github/workflows/naon2-front-v02.yml` to verify the SHA-256 and make padded 2048px display exports on upload. That is a resample, not new native 2K detail.
