# NAON2 Character Identity and Delivery QA

All hard-gate criteria must pass before any image is designated an official master or commercial deliverable.

| Test | Requirement | v0.2 Status |
| --- | --- | --- |
| Face | Gamer A face proportions, eye spacing and muzzle remain recognizable | Not validated |
| Fur markings | Gray crown/back and white face/chest contrast remains consistent | Not validated |
| Body | Chibi head-to-body proportions, short limbs, paws | Not validated |
| Ears/tail | Pink inner ears, complete thick curved tail with matching fur | Not validated |
| Artifacts | No duplicate limbs, malformed eyes/objects, unwanted text/logos | Not validated |
| Resolution | Native pixel count and clean edges suitable for delivery | Not validated |
| IP/commercial | AI tool conditions, trademarks/fonts, scope of buyer use | Not validated |
| Approval | User accepts exact final artwork | Not validated |

Original image SHA-256 checks and crop-pixel correctness have passed locally, but those are **not** identity or sales-quality approval.

## 2026-10-16 판정 기록
- `assets/masters/vector-v01/`: **REJECTED** — NAON2 원본과 캐릭터 정체성이 충분히 일치하지 않아 사용자 불합격. 기술 테스트 성공과 무관하게 공식 마스터/판매 이미지로 금지.
- 정면 마스터 승인 조건은 `character/FRONT_MASTER_SPEC_V01.md`를 따른다.
- 다음 검수는 **원본 A·승인 시트 C·신규 정면 시안**을 나란히 놓고 캐릭터 유사성을 우선 확인한다.

## 2026-10-16 · 정면 생성 후보 v1 / v2
- 후보 v2 원본 PNG 1254×1254 RGBA로 생성 성공. 배경 투명화 검사 통과.
- 유사성·이마 흰 털 마스크·눈 비율·꼬리 형태: **최종 디자인 검수 대기**.
- v2 피사체 알파가 왼쪽·아래쪽 캔버스 경계에 닿아 **상품용 안전 여백 검수 불통과**.
- 공식 2K 정면 마스터, 판매용 원화: 아직 아님.
- 상세 `character/FRONT_CANDIDATE_QA_V02.md`.
