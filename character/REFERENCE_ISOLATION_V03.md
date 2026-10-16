# NAON2 isolated model references v0.3

## Result
Three **standalone transparent PNG references** were extracted from the already approved character sheet, not synthesized:
- `naon2-front-reference-v03.png`: front, 214 × 213 px
- `naon2-three-quarter-reference-v03.png`: three-quarter view, 185 × 216 px
- `naon2-back-reference-v03.png`: back, 213 × 215 px

The reference board is a layout of enlarged copies; it does not increase native detail. Source PNG is not multilayer. The "side" in the approved sheet is actually a 3/4 perspective, **not a true 90-degree profile**.

## Method and validation
- Uses original image in `assets/references/naon2-character-sheet-v1.png`.
- Verifies its SHA-256 against `asset-manifest.json` before processing.
- OpenCV GrabCut subject masks + largest-object contour fill + alpha smoothing.
- Each output checks silhouette size and verifies its alpha mask does not hit the image edges.
- Processing can remove individual boundary pixels. This is not a pixel-for-pixel exact reproduction at the edges.
- Quality inspection: head, ears, paws and tail visible in all 3 cutouts.

## Status
**Reference preparation complete, true standalone high-resolution official master NOT complete.**
Do not market these 185-214px crops as original high-resolution art or layered source.

## Reproduction
Run `python -m pip install -r requirements-reference.txt`, then
`python scripts/verify_assets.py` and
`python scripts/isolate_model_references.py`.

A GitHub Actions workflow may generate and commit these binary derivatives. If actions are blocked by permissions, treat that as a distinct deployment status; use the provided ZIP as the local verified asset.
