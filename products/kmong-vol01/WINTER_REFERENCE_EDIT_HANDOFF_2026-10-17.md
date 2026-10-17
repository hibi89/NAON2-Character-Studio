# NAON2 겨울 독립 원화 — 참조 이미지 고정형 편집 인수인계 (2026-10-17)

## 현재 상태
**IMAGE BLOCKED / REFERENCE INPUT READY / NO EXTERNAL TRANSFER.** 단독 겨울 완성 원화 0장. 기존 Full 46 PNG/Wallpaper 19 PNG 구매 RC, 새 ZIP 빌드 소스 및 CI는 그대로 보존. 기존 크몽 ID 840876 수정 없음.

## Stop & Pivot 실제 근거
- 같은 ChatGPT 이미지 생성 도구에 '단독 겨울 일러스트'를 요구했으나, 이번 재시도 결과도 가격/메뉴/프로필이 들어간 **상품 포스터 합성판**으로 출력. 영구 파일 `a_detailed_composite_illustration_poster_product.png`(채팅 로컬). 단독 원화로 채택하지 않음.
- 이전 수동 합성 `WINTER_PRECISION_COMPOSITE_V1_REVIEW_ONLY_2560x1440.png`: 캐릭터와 눈사람/니트/배경의 화풍 불일치로 FAIL. 같은 편집 기법 반복 금지.
- 현 이미지 생성 경로 재시도는 효용 낮으므로 종료. 외부 원형 고정/참조 편집 기능이 있는 **Runway**를 대안으로 검토(별도 계정 연결·크레딧 소모 가능). 연결 추천은 제안했으나 **사용자 설치/연결 및 외부 이미지 전송·유료 결제는 하지 않음**.

## 정확한 레퍼런스 파일
| 역할 | 패키지 파일명 | 출처 | 실제 픽셀 | SHA-256 |
| --- | --- | --- | --- | --- |
| NAON2 외형 기준 | 01_BRAND_GUIDE_REFERENCE_ONLY.png | 기존 승인 `NAON2_PROFILE_GUIDE_LAST_GENERATED_1536x1024.png` / 임시 GitHub Actions refpack artifact 12096579552 | 1536×1024 | `7641e2ea75de3fdaf3167a38a92b17eaeb01a314ab04c39bd51f70fb169004ac` |
| 캐릭터 단독 편집 베이스 | 02_ORIGINAL_NAON2_BASE_1254.png | GitHub `assets/selected/vol01/ChatGPT 이미지 2026년 10월 17일 오후 01_50_04.png` | 1254×1254 | `b67e1e34321664d31ce5e9e9ca1fff5aef190e038ffc6b40919b38411165aaa1` |
| 겨울 무드 **참고만** | 03_WINTER_SCENE_REFERENCE_ONLY.png | 기존 참조 ZIP `WINTER_PANEL_CROP_REFERENCE_ONLY_NOT_SALEABLE.png` | **505×282** | `6b4dac0e553c2d965005d1749bc39b001c5e5a757ad176b4c2e1e917461ded9e` |

작업 공간 로컬 보조 자료: `NAON2_WINTER_REFERENCE_EDIT_READY_20261017.zip`, **4,644,562 bytes** SHA-256 `658e5a7e09f0c1e7c071cae6ab148a7b2702993e25d1bb914f9d29814f58df58` / 구성 위 이미지 3개+한국어 브리프+SHA 매니페스트. 내부 5개 CRC PASS. **이 ZIP은 사용자 채팅 다운로드용 / 외부 서비스 업로드 전용 확정본 아님 / GitHub main 바이너리에는 올리지 않음.**

## 성공 기준
1. 외부/전문 편집 도구를 사용할 경우 **사용자의 명시 승인 후에만** 이미지 전송·유료 크레딧 사용. 연결 완료 전 직접 작업했다고 주장 금지.
2. 결과는 **단독 이미지 한 장**: 텍스트/가격/상품 메뉴/콜라주/프로필/테두리/워터마크 없음. 회갈색과 흰색 치비 나온이 원형 + 보라색 니트 모자·목도리 + 눈사람 + 눈 내리는 밤·가로등.
3. 귀·큰 갈색 눈·흰 털무늬·이빨 위치·꼬리·네 발을 원본과 확대 비교. 고양이 4발 개수 오류, 눈사람과 팔/꼬리 융합 등 불허.
4. 독립 고화질 2048급 PNG(실제 픽셀/네이티브 생성 여부 별도 기록). 저해상도 참고 컷을 단순 확대하여 신규 원화라고 주장 불가.
5. **사용자 최종 시각 승인 전에 구매자 최종 ZIP 빌드/크몽 기존 840876 변경 금지.** 승인 후 GitHub 기존 `winter_release_pipeline.py`으로 두 메뉴 Full 51 PNG, Wallpaper 23 PNG 및 JPG 자동 생성·검증; 이전 원본과 RC 불변 유지.
6. 이미지 원본/최종 파생본 GitHub 적정 위치에 영구 보존된 후에만 임시 `transfer/NAON2_REF_20261017/` 삭제 검토. 기존 원본 데이터 삭제·강제 푸시 금지.

## 다음 '3'
Runway가 실제로 연결돼 있고 사용자 외부 이미지 사용 승인이 있으면 **참조 이미지 편집 → 독립 단일 그림 → 시각 QA**를 시작. 연결/승인이 없다면 *이미 실패한 이미지 생성·로컬 합성 또는 패키징 인프라 테스트를 반복하지 않는다*. 다음으로 할 수 있는 것은 안전한 로컬 편집 소스 준비/별도 전문가 편집 수단 검토이며, 신뢰할 만한 원화 출력을 확보하기 전 출시 완료를 주장하지 않는다.
