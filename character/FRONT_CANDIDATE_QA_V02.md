# NAON2 Front Candidate QA v0.2 — Not Official

Date: 2026-10-16
Status: **CANDIDATE ONLY / NOT A MASTER / NOT FOR SALE**

## Source-of-truth
- Original gamer A: `assets/originals/naon2-gamer-original.png` (208×208)
- Approved sheet C: `assets/references/naon2-character-sheet-v1.png`
- Extracted reference: `assets/derivatives/reference-isolates-v03/naon2-front-reference-v03.png` (214×213)
- Rejected SVG vector v0.1: do not reuse for master or derivatives.

## Generated candidates (not yet uploaded to GitHub)
| Candidate | Native px | Color/alpha | SHA-256 |
| --- | --- | --- | --- |
| `naon2-front-candidate-v01-raw.png` | 1254×1254 | RGBA | `b09db17f8c1df3a6e4195fbd35ca8dfd069d7d30b4034acf1db6c805b5945df8` |
| `naon2-front-candidate-v02-raw.png` | 1254×1254 | RGBA | `fcf6cd58be831bc66ebf72039061fa0d545696ac79f0c3396247eca78b48d059` |

Local deliverable: `NAON2-front-master-QA-v01.zip`, including both byte-for-byte unchanged candidate PNGs, side-by-side comparison PNG, `QUALITY_REVIEW.md` and `QA-manifest.json`. Zip integrity passed. The archive is **not part of GitHub yet**; keep the download separately.

## Actual QA verdict
| Gate | Outcome |
| --- | --- |
| Files readable and source original untouched | PASS |
| 1254×1254 RGBA + transparency | PASS |
| Native 2K (2048×2048) production target | FAIL — candidate is 1254×1254 |
| Complete safety margin around subject | FAIL — latest alpha touches left and bottom edges (5 and 8 pixels) |
| Edges / halo | REVIEW — colored fringe around fur requires quality pass on light and dark backgrounds |
| Face and fur-mask resemblance | REVIEW — larger white forehead blaze, differences in eye proportions and tail |
| User identity/design final approval | **PENDING** — positive reaction recorded but no acceptance as official final master |
| Commercial-ready master | NOT YET |

## Recommendation
Preserve the v2 raw candidate unchanged. Ask the user to compare identity to the gamer original and approved sheet. If accepted as the preferred facial *direction*, make targeted correction to forehead marking, composition/safe margins and edge quality. Do not state that padding, upscaling or PNG alpha extraction is an actual 2K native redraw. Only after visual approval and technical QA should `official` promotion or subsequent themes proceed.

Do not conflate the initial user's acceptance of the character sheet with final approval of this new independently generated v2 artwork.
