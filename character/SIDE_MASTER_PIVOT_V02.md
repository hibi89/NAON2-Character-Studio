# NAON2 / 90° 측면 마스터 — 제작 전환 규격 v0.2
작성: 2026-10-17 / 상태: 작업 경로 변경, 신규 마스터 미완료

## 입력 원본 (우선순위)
1. **Identity / main**: `assets/candidates/front-v02/naon2-front-candidate-v02-raw.png` — 사용자 선호 정면 v2, 1254×1254 RGBA. **GitHub 업로드 완료(2026-10-17), 정면 후보 상태**. 대화에서 파일은 제공했으며 SHA-256: `fcf6cd58be831bc66ebf72039061fa0d545696ac79f0c3396247eca78b48d059`.
2. **Source primary**: `assets/originals/naon2-gamer-original.png` — 최초 게이머 이미지, 얼굴/표정/그림체 기준.
3. **Source secondary**: `assets/references/naon2-character-sheet-v1.png` — 사용자가 승인한 도감 시트의 털색/체형 및 꼬리.
4. **Style auxiliary**: `assets/originals/naon2-astronaut-original.png` — 다른 각도에서 같은 캐릭터인지 비교용.

사용자 원본과 정면 v2를 섞어서 다른 캐릭터로 재설계하지 말 것. 이전 벡터 v0.1은 REJECTED; 이미지 생성 콜라주/잘린 측면은 참고용으로도 최소화.

## Stop-and-Pivot: 2026-10-17 검수
### 시도 1
기존 가로형 캐릭터 시트에서 OpenCV GrabCut으로 측면 단일 이미지를 분리.
- 결과: 흰 주둥이/가슴/앞발이 배경으로 제거돼 원형 손상.
- 해당 결과를 공식 원화로 채택하지 않음.

### 시도 2 (마스크 수정)
흰 털·발·꼬리에 수동 전경 마스크를 넣어 재분리.
- 결과: 흰색 털 보존은 개선됐지만 측면 꼬리의 오른쪽과 하단 발이 **원본 패널 경계에서 이미 잘려 있음**.
- 캔버스에 여백을 추가하거나 배경을 투명하게 해도 잘린 픽셀을 복구할 수 없음.
- 동일한 분리 재시도 중지. 실제 판매용 마스터로 지정 금지.

## 정식 측면 마스터 요구
- **단독 이미지 1장**: 정확한 옆모습(90° profile), 화면에서 왼쪽을 향함.
- 머리부터 발바닥까지 보이는 전신; 둥근 큰 눈 한쪽, 작은 분홍색 코와 하얀 입주변.
- 귀 내부 분홍빛, 회갈색/흰색 기본 털 마스크, 따뜻한 입체적 털 질감.
- **꼬리가 뿌리부터 끝까지 완전히 보일 것.** 4변 안전 여백 각 최소 10% 목표.
- 옷/게임패드/헬멧/글자/도표/패널/추가 고양이/레이블/로고 없음.
- 실제 이미지 형식, native resolution, alpha 포함 여부를 파일에서 검증. 체크무늬를 그린 RGB는 투명 배경 아님.
- 이전 정면 v2와의 얼굴·털 분포·꼬리 동일성 검수. 사용자의 디자인 승인 전 공식 상품 사용 금지.

## 검증 가능한 외부 대안
| 방법 | 속도/비용 | 장점 | 조건 |
| --- | --- | --- | --- |
| A. **참조 이미지 기반 단일 컷 편집/생성** — Runway(연결 시) / Gemini | 1~2회 테스트, 크레딧 또는 요금제에 따름 | 동일 캐릭터 참조에 직접 맞출 가능성 | 외부 계정/원본 업로드에 사용자 동의 필요; 성공 보장 아님 |
| B. Adobe Photoshop Reference image + Generative Fill | 편집 시간과 플랜에 따름 | 영역 부분 수정/수동 보정 통제 | 외부 툴/요금제 필요 |
| C. 레이어 원화 수작업 | 상대적으로 느리고 비용 높음 | 원형·꼬리·패턴 직접 통제, 편집 가능 | 디자이너 수준의 수정 필요 |

**다음 추천:** A안으로 **측면 한 장만** 시도한다. 조잡한 콜라주나 잘린 꼬리가 나오면 다시 동일 프롬프트 반복하지 말고 B/C로 전환한다.

### 사용 가능한 작업 지시(외부 이미지 편집기)
```text
Use the supplied NAON2 front v2 as the PRIMARY identity reference. Other supplied images are secondary reference only.
Create exactly ONE standalone full-body, true 90-degree left-facing SIDE PROFILE of the very same NAON2 kitten.
Preserve character identity: round gray-brown head, large glossy warm-brown eye, short pink nose, white muzzle and fluffy white chest, pink inner ear, compact chibi proportions, short white paws, giant plush curved tail with warm brown highlight.
Preserve soft dimensional illustrated fur and original palette. Full head, ears, all four paws and the ENTIRE tail must fit safely inside the canvas with >10% margin on every edge.
Plain empty white or truly transparent backdrop. No text, title, chart, panels, multiple views, reference sheet, clothing, props, typography or additional characters.
Do not redesign the original cat; do not change its eye style or facial mask. Return ONE isolated image file, not a marketing collage. If the tool cannot preserve identity or tail, do not claim completion.
```

## 현재 소유·저장 상태
- GitHub `main`: 기존 원본·승인 시트 및 QA 보고서 보존.
- 프런트 v2 raw PNG: **GitHub 원본 업로드 완료(커밋 `ac45833`)**, 자동 보정 run `38992520700` 성공(출력 커밋 `14f5740`).
- 실패한 GrabCut 출력: 로컬 검사 파일. 사용 승인 전 외부 전송·GitHub 원화 승격 금지.
- 새 측면 마스터: **미제작**, 상업화 미승인.
- 외부 서비스 연결/원본 업로드/결제 전 **사용자 동의** 필요.
