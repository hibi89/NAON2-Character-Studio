# NAON2 · 겨울 파이프라인 v2 실증 결과 (2026-10-17 KST)

## 결과 판정
**파이프라인과 코드 GitHub 반영/CI: 완료. 겨울 신규 독립 원화와 최종 판매 패키지: 미완료.**
사용자 지시 '3'=다음 작업 계속을 수행한 중간 체크포인트. 기존 크몽 840876은 변경하지 않았으며, 제3자 외부 이미지 편집 서비스에 원본을 전송하지 않았다.

## 실제 수정
- 기존 파이프라인은 배경화면 팩에 **겨울 마스터 원화 파일을 제외**하는 버그가 있었다. 사용자 요구에 맞춰 두 buyer ZIP 모두 겨울 독립 원화 PNG 포함으로 수정. 최종 예정 수량: Full 46→**51**, Wallpaper 19→**23**.
- 원본 최소 해상도가 가로·세로 각 2048px로 잘못 고정되어 2560×1440 가로형 원화를 거부하는 버그 수정: 짧은 변 >= 1440px 및 전체 픽셀 >= 2560×1440 기준. **해상도만으로 네이티브 원화·동일 캐릭터임을 증명하지 않음**.
- Wallpaper 상세페이지의 표 8행과 하단 문구 겹침을 피하도록 행 간격 조절.
- `verify_release_gate.py`는 현재 RC 검증 및 `--with-winter --winter-master` 조건에서 목표 51/23 PNG 수량과 겨울 마스터 파일을 각각 실제 검사하도록 개선.

## 검증 (확인/미검증 구분)
- 로컬 `unittest`: **11/11 PASS** (기존 9 + 가로형 2560×1440 원화, Wallpaper 겨울 독립 마스터 포함 검증 추가).
- 현재 RC 구매 ZIP **실제 바이트 SHA와 CRC PASS**:
  - Full `2acd5725434dde4dbd80d35ec7f6fa132eec20da4685425437dc8a6cb24f470a` (137,252,366B), PNG 46.
  - Wallpaper `f435e6729c5892afcf332cbe879e8ca51de2b00c9f0bb63013b9fe6cfad4ad14` (63,296,157B), PNG 19.
- **기존 실물 RC 2개 + 판매 불가로 명시된 인공 단색 테스트 PNG**로 통합 패키징 검증. Full 51장 (테스트 ZIP 137,458,761B), Wallpaper 23장 (63,472,287B) 생성 및 신규 검수기 **PASS**. 상세 JPG 각 5장씩, 총 10장 생성/해상도 검사 **PASS**. 인공 테스트 원화·ZIP·JPG는 임시 격리 폴더 자동 삭제. 실제 새 겨울 원화라고 주장하지 않는다.
- GitHub 본 코드 6파일과 로컬 원본의 Git blob SHA **6/6 일치**, 그중 핵심 파이프라인 blob `0b22f499637730dc3ee861b73529703bb70a243f`, 새 검증기 blob `b70eca7a3263038fe3f399f72608ae2323bb1f15`.
- 원격 CI `NAON2 winter package safety tests`: run **39029592559**, SHA `c728b16555029c3b65fb2cd5dcfad681caeeff91`, **completed/success**. Python 3.11 syntax·Pillow·한국어 폰트·11/11 unittest 및 없는 buyer ZIP 오류 차단 테스트. 이는 판매자 원화 품질 자동 승인이나 GitHub에서 실제 200MB buyer ZIP을 처리한 테스트가 아님.

## GitHub 추적 파일
- `products/kmong-vol01/winter_release_pipeline.py`
- `products/kmong-vol01/verify_release_gate.py`
- `products/kmong-vol01/test_winter_release_pipeline.py`
- `products/kmong-vol01/integration_smoke_actual_rc.py` (로컬 실제 RC에서 선택 실행; 합성 테스트 데이터 자동 삭제)
- `products/kmong-vol01/approval_manifest_TEMPLATE.json` (**false** 값들 그대로 둠, 사용자 승인 사칭 금지)
- `products/kmong-vol01/NAON2_WINTER_PIPELINE_README_2026-10-17.md`
- `.github/workflows/naon2-winter-pipeline-tests.yml`

## 차단 항목과 다음 단계
1. **고화질 신규 독립 겨울 원화 0장**. 기존 image-gen 반복이 홍보 포스터로 흐르고 수동 합성은 스타일 QA 실패. 동일 방식 재시도 금지. 검증 가능한 참조 이미지 보존형 편집/원화 확보 방식으로만 전환. 유료 서비스 및 외부 자료 전송 사전 승인 필요.
2. 완성 원화 시각 QA: 선택 프로필 기준 얼굴·눈·이빨·분홍 귀·복슬한 꼬리·다리 4개·의상·눈사람·배경 스타일. 실제 외형/권리 검증 후 **사용자 승인**.
3. `approval_manifest_TEMPLATE.json`의 거짓 값 임의 변경 없이 승인되면 `winter_release_pipeline.py package`로 두 ZIP 51/23 및 상세 JPG 10장 재빌드. `verify_release_gate.py --with-winter --winter-master`로 기술 QA → 사용자 최종 검수.
4. 그 후 **Codex만** 크몽 기존 840876 심사 상태 확인→수정 가능 여부→정확한 19,900원/9,900원 두 메뉴 편집/재심사. 사용자 승인 전 크몽 수정·철회·등록 금지.
5. GitHub `transfer/NAON2_REF_20261017/` 임시 원본 바이너리는 현재 영구 원화 보존 조건 미충족이므로 **삭제 금지**. 참조 ZIP artifact 12096579552 보존/만료에 주의. Vercel/Production은 이 상품 제작 프로젝트에 **미적용**.

검증 종료 기준: 2026-10-17 KST. CI 실행 성공과 실제 판매 가능한 제품 출시를 구분한다.
