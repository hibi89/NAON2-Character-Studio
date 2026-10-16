# NAON2 Source Asset Verification — 2026-10-16

## Scope
Authenticated GitHub tree inspection + independent local calculation of the Git object blob digest over the original three files. The Git SHA-1 blob digest includes `blob {file-size}\\0` prefix before file bytes.

| GitHub file | Size (bytes) | Git blob SHA-1 (GitHub and local both match) |
| --- | ---: | --- |
| `assets/originals/naon2-gamer-original.png` | 96,666 | `5a6bcdc0281aa393d2aa1b30a24852744b879cdc` |
| `assets/originals/naon2-astronaut-original.png` | 3,681,149 | `5e0de00d733d09ee49033cba3779943fce123160` |
| `assets/references/naon2-character-sheet-v1.png` | 2,237,668 | `9623d4774187d222d8fa95fa3917d3f847285f8c` |

Remote `main` HEAD at inspection: `470f9fb59606a0ae94320b65ecda075f6669ba27`.
Source SHA-256 and pixel dimensions are recorded in root `asset-manifest.json`.

**Outcome:** 3/3 remote Git blob SHA-1 digests exactly matched independent computation from the original local files. This verifies byte-for-byte identity at upload. This does **not** establish layered editability, model consistency or commercial usage rights.
