# NAON2 겨울 원화 완성 이후 자동 패키징 키트 (2026-10-17)

**상태: 기술 구현 검수 통과, 겨울 독립 원화 미확보로 실제 판매본 생성은 차단.**

- 기존 GitHub `main` 출발 커밋: `c666f193383b57b51d6bd615e081a95b10d41c28`.
- 기존 Full RC ZIP: `2acd5725434dde4dbd80d35ec7f6fa132eec20da4685425437dc8a6cb24f470a` (137,252,366B).
- 기존 Wallpaper RC ZIP: `f435e6729c5892afcf332cbe879e8ca51de2b00c9f0bb63013b9fe6cfad4ad14` (63,296,157B).
- 공통 프로필 PNG SHA256: `7641e2ea75de3fdaf3167a38a92b17eaeb01a314ab04c39bd51f70fb169004ac`.
- 원본 바이너리 및 등록된 크몽 840876은 변경하지 않음.

## 구현 비교

| 설계 | 장점 | 단점/비용 | 결정 |
|---|---|---|---|
| **기존 검증 ZIP을 읽어 새로운 겨울 테마만 추가** | 기존 구매자 파일 내용/원본 SHA 유지, 속도/비용/QA 최소화 | 새 겨울 원화 별도 필요, ZIP은 재압축 | 채택 |
| 13개 원화+모든 배경화면을 새로 재렌더링 | 디자인 일괄 변경 가능 | 높은 비용, 기존 데이터 왜곡 위험, 모든 QC 재수행 | 거절 |

## 필요한 실제 작업

1. 사용자 선택 프로필과 같은 캐릭터의 **신규 독립 겨울 원화** PNG (가로·세로 각각 2048px 이상, 유료 외부 도구 없이 생성 가능하면 우선)를 확보한다. 스크린샷·업스케일 이미지·홍보 합성판 사용 금지. 네 발, 꼬리, 눈, 이빨, 얼굴을 사람이 확인한다.
2. `python winter_release_pipeline.py inspect --master NAON2_WINTER_ORIGINAL.png --out winter_preview/`로 원화 규격 및 PC/모바일 화면비 미리보기를 만든다. 이 단계에는 승인서가 필요 없다.
3. 사용자가 실제 원화 및 권리·상품 사용 조건을 확인 후 `approval_manifest_TEMPLATE.json`의 **거짓 플래그**를 사실이 확인된 항목만 `true`로 바꾸고 `winter_master_sha256` 및 출처·사용권 근거를 작성한다. 임의로 승인서를 생성하지 않는다.
4. `python winter_release_pipeline.py package --master NAON2_WINTER_ORIGINAL.png --approval APPROVED.json --full NAON2_FULL_COLLECTION_19900_BUYER_REVIEW_RC.zip --wallpaper NAON2_WALLPAPER_PACK_9900_BUYER_REVIEW_RC.zip --out deliverables/`
5. 기존 검증 파일을 수정하지 않고 **새 검수 ZIP** 2개(Full PNG 51개, Wallpaper PNG 22개), 크몽 메인 652×488 JPG 포함 **새 상세 5장씩**, 신규 겨울 테마 썸네일, 변경 후 ZIP CRC/제품 안내가 생성된다.
6. 사용자가 최종 ZIP과 상세페이지를 한번에 검수·승인한 후 Codex에게만 기존 크몽 840876의 **두 메뉴 19,900원/9,900원** 편집·재심사 제출을 위임한다. 사용 권한·권리·가격·크몽 실제 메뉴 구조 충돌 시 재승인 요청.

## 품질 게이트

- 원화 PNG가 2048×2048 미만이거나 투명한 불완전 장면이면 거부한다. 원본 생성 해상도인지, 눈/치아/발 수가 실제 정확한지는 자동 검사로 **입증 불가능**해 수동 품질 플래그가 필요하다.
- 허용된 JSON 체크리스트가 모두 사실상 승인되지 않으면 `package`는 아무것도 제작하지 않고 종료한다.
- 원본 RC ZIP 2개 SHA 및 두 ZIP 공통 프로필 SHA가 일치하지 않으면 거부한다.
- 같은 경로 파일을 덮어쓰지 않고 새로운 결과만 생성하며 200MB 이상 납품 ZIP은 거부한다.
- 화면비 맞춤 파생은 네이티브 2K/4K 신규 원화라고 표시하지 않는다.
- 생성 성공은 **검수용 후보**일 뿐, 자동 크몽 등록/제출을 하지 않는다.

## 실제 검증 내용
- 2026-10-17 로컬 Python 3.11 + Pillow: **unittest 9/9 PASS**. ZIP 검사·비정상 승인·저해상도·투명도·파일 규격/상세 JPEG 렌더 및 경로 오염 방어 테스트 포함.
- 실제 Full/Wallpaper 두 ZIP의 SHA256/CRC PASS (원본 읽기만 수행).
- 실제 신규 독립 겨울 원화: **0장**, 상품 최종 파일: **0장**. 성과를 혼동하지 않는다.
- GitHub CI: 기존 검수기 run 39026198826 성공. **본 신규 파이프라인의 원격 CI는 별도 검증 전까지 미검증**.