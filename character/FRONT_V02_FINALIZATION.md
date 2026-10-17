# NAON2 Front v2 — Margin-safe candidate export

**Review candidate only, not official character master or commercial product.**

## Decision
User preferred the v2 face direction over the previously rejected flat SVG; proceed without redesigning its head, eyes, forehead blaze, fur texture or tail. Keep all originals and previous versions.

## Export verified locally (2026-10-16)
- Original candidate: 1254×1254 **native** RGBA PNG; expected SHA-256 `fcf6cd58be831bc66ebf72039061fa0d545696ac79f0c3396247eca78b48d059`.
- 1498×1498 padded transparent canvas: source composited at (182, 122); only minor alpha speckles (alpha ≤12) on four **outermost source pixel lines** cleaned.
- 2048×2048 PNG export: Pillow LANCZOS alpha-aware resample; **no novel high-resolution detail**.
- Subject bbox alpha >12: x=295..1752, y=270..1760; safety margin L/T/R/B = **295 / 270 / 295 / 287px**.
- White + dark background JPEG previews and comparison sheet generated.
- Original v2 SHA-256 unchanged; output ZIP integrity checked.

## Source file handling / remote sync — completed 2026-10-17
GitHub source image exists and has been validated at `assets/candidates/front-v02/naon2-front-candidate-v02-raw.png` (1254×1254, 1,511,047 bytes, expected SHA-256 unchanged).
- Upload commit: `ac45833a36d177bf81c7c63fd2b3e113eb3d697f`
- GitHub Actions run: https://github.com/hibi89/NAON2-Character-Studio/actions/runs/38992520700 — **completed/success**.
- Outputs commit: `14f5740dea5535efb7b28ae4df44812c0870f1ac`.
- Outputs and manifest: `assets/candidates/front-v02/outputs/`. This is **review-candidate-NOT-official-master**; upscale does not produce new native details.
The previous chat-delivered ZIP can be retained for archive only; **no manual reupload is needed**.

## Remaining QA
- User visual approval of this exact padded v2.
- True artist-authored high-resolution master or editable-layer source still **not available**.
- Some facial markings and tail differ from the approved first sheet; mark as accepted evolution only if user approves.
- IP ownership/licensing, exact deliverable format, Kmong terms remain unverified.

## Local reproduction
`python -m pip install numpy==2.3.5 Pillow==12.3.0`

`python scripts/finalize_front_v02.py`
