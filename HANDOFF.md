# NAON2-Character-Studio — HANDOFF.md
2026-10-17 최신 복원/검수 / RELEASE HOLD (출시 승인 전)

> 정식 인수인계는 [NEXT_CHAT_HANDOFF.md](NEXT_CHAT_HANDOFF.md)를 먼저 읽고, 그 다음 본 파일 → STATUS.md → AGENTS.md → products/kmong-vol01/*.md → 실제 코드를 비교한다. 본 파일은 2026-10-17 15시대 KST 검수 결과를 간결하게 요약하며 이전의 12장 합성 러프 계획보다 우선한다.

## 1. 목표 / 확정 요구 / 기술
NAON2 WORLD Vol.01, 사용자가 고른 고양이 일러스트 15장의 기성 디지털 컬렉션을 크몽 기존 편집 ID **840876**에 등록. 판매가 **5,900원**, 향후 7,900원 변경은 내부 계획(기존 할인 이력 없음). 다온이·맞춤 제작 제외, 원본 그림/배치/표지 1+상세 5는 사용자 승인 완료. Python/Pillow/zipfile, GitHub Actions/크몽 사용.

## 2. 실제 완료 / 결정
- 본 세션 기준 GitHub 최초 main `7af71e742857c9365adec79d4ad3ff8c1ac9eb2c` 검증, Actions run **39006112541** artifact ID **12090534562** 다운로드/내용 직접 확인.
- Artifact sha256 `9d9221c4e81b4eaa38e9cb547032a3798c9e6759b1cfc9d8547f3ee8137b9a6b` / 65,895,535 bytes / 외부 12멤버/ZIP 검사 PASS.
- 원본 15/15 PNG 실제 decode 및 SHA256 + Git blob + bytes 검사 PASS. 구성 13×1254×1254, 1×208×208, 1×379×384. 이미지 바이트 재인코딩, AI 재생성, 업스케일, 홍보 이미지 배치 수정 없음.
- 과거 구매자 후보 ZIP `d4e0554622a9a74a0cf47009028bbdc1ea51ec883c86aa1fb606b27e266f3847` 30,650,596 bytes에서 구매자 안내의 '정식 판매 전 확인해야 할 조건' 발견, 납품 금지.
- 새로운 **깨끗한 구매자 ZIP** `NAON2_WORLD_VOL01_15PNG_BUYER.zip` **30,651,697 bytes**, SHA256 `e35e7292718ea8728e5d2498eb4e7187675201919a7c2272817dcb0c773c3f2f`. 15 PNG 원본 동일 + 정리된 한국어 안내 1, 불필요한 내부자료 0. ZIP CRC PASS / 15 해시 PASS.
- 새 판매자 등록 키트 `NAON2_WORLD_VOL01_REGISTRATION_KIT_RELEASE_HOLD.zip`, **33,621,748 bytes**, SHA256 `dd2f97609a9d57241e001663ed19b3973b2dc7b57e985fdc9781c31ec2a7a095`. buyer ZIP + 이전 승인 JPG 6개 그대로 + 판매자 전용 등록문안/QA/권리 게이트.
- GitHub 텍스트 소스 `products/kmong-vol01/BUYER_GUIDE_KR.txt` 추가; `LISTING_COPY.md` 신규 문구 정리; `build_selected15.py`의 구매자 초안 안내문 하드코딩을 외부 한국어 안내 원본 참조로 변경(원본 15 PNG/홍보 JPG 생성 코드 구조 유지). 빌드 최신 수정 관련 커밋 **900589955b9d5d5aaa22026649261d1785174aa4** (이후 문서 변경 커밋은 main 최신 확인).

## 3. 테스트와 검증
다운로드 artifact 외부 zip: 12/12 확인, CRC PASS. 내부 구 구매자 ZIP 16/16, 구 판매자 ZIP 10/10 CRC PASS. 원본 해시 15/15/픽셀 디코딩 15/15. 새 buyer ZIP 16/16·SHA 15/15 PASS. 새 seller kit 내부 buyer 동일·JPG 6/6 재사용·CRC PASS. 홍보 JPG 크기 대표 652×488, 상세 1200×1900 3개/1200×1800 1개/1200×1690 1개. **최신 GitHub Actions 재빌드 결과는 별도 실확인 전 미검증.** UI 변경/상품 심사 제출 미시행.

## 4. 상태
원본 및 패키지: 완료(로컬 검증). 구매자용 이용 안내: 정리 완료(조건부 라이선스). 개별 작품 생성 출처/입력 자산 권리: **미완료**. 크몽 카테고리 적합성/실수령액: 미확정. 기존 편집 ID 840876 실제 화면은 확인, 상품 등록/제출/승인/판매: **미실시/미검증**, 중복 생성 금지. **최종 판매 상태 = RELEASE HOLD.**

## 5. 근거 / 차단 사유 / 재시도
- 최초 buyer ZIP 안내 내용에 예비 문구 → 별도 새 구매자 ZIP으로 교체, 원본 15장 무변경.
- ChatGPT/OpenAI 일반 약관은 적법한 입력 기반 출력 사용과 판매를 허용하나, 제3자/입력물 권리·독점 저작권 보증은 아님. 11개 'ChatGPT 이미지...' 파일명만으로 생성 소스/당시 약관 검증 불가. 나머지 `image(20260928-233741).png`, `나온이3.PNG`, `냥이.png`, `황금빛 기차 여행의 고양이 친구.png` 네 원본의 생성 이력·기준 시트 사용 권리도 확인 필요.
- 브라우저 연결 계정의 크몽 기존 편집 페이지 실제 확인: 화면상 이전 제목 '나온이 디지털 배경화면 12종', 카테고리 `자료·템플릿 > 취미 자료 > 기타`, 설명/대표/상세/금액/ZIP 빈 상태. Browser는 읽기 전용이므로 제출이나 저장은 수행하지 않음.
- 기존 생성된 원본/홍보 JPG 교체나 다시 그리는 접근 중단. 권리 검증 없이 출시 주장 금지.

## 6. 원격 저장소 / 버전 / 경로
- `https://github.com/hibi89/NAON2-Character-Studio`, branch `main`, 최초 확인 SHA `7af71e742857c9365adec79d4ad3ff8c1ac9eb2c`.
- 원본 `assets/selected/vol01/` 15 PNG / 빌드 `products/kmong-vol01/build_selected15.py`, Actions `.github/workflows/naon2-vol01-selected15.yml`.
- GitHub 원본 바이너리 불변, 로컬 ZIP은 다운로드 산출물이며 GitHub에 대용량 ZIP/JPG 신규 커밋하지 않음.
- 핵심 `NEXT_CHAT_HANDOFF.md`, `HANDOFF.md`, `STATUS.md`, `AGENTS.md`, `products/kmong-vol01/BUYER_GUIDE_KR.txt`, `LISTING_COPY.md`.

## 7. Production / 실행 환경
- Vercel 서비스 배포 **미적용** (디지털 아트 상품). 크몽 편집: `https://kmong.com/my-gigs/edit/840876?rootCategoryId=20&subCategoryId=2005&thirdCategoryId=200502`.
- 로컬 재빌드: 프로젝트 루트에서 Python Pillow 설치 후 `python products/kmong-vol01/build_selected15.py`.
- Actions 기존 성공 run 39006112541. 변경된 guide ref 코드 기준 새 Actions 성공 여부는 별도 확인해야 함.
- 기존 크몽 제출·판매 URL 없음.

## 8. 원본/백업/보안
- 원본 기준: GitHub `assets/selected/vol01/`의 15개 blob 및 SHA. git commit history로 코드/문서 복구.
- 수정 전 기존 buyer/seller 후보 ZIP과 artifact가 증거로 남아 있음. 원본 파일 경로·파일명·이미지 바이트/대표·상세 이미지 절대 바꾸지 않음.
- 인증 쿠키, 크몽 계정, 토큰은 문서화/커밋/ZIP 포함 금지.

## 9. 다음 순서 / 승인 항목 / 완료기준
1) 각 PNG 생성 도구/입력 자료 및 권리/상표 문제의 증빙 확인(특히 4개 파일).
2) 크몽 자료·템플릿 카테고리의 이 유형 허용 여부, 5,900원 기준 수수료/수익금 계산기 실확인. 필요시 크몽 공식 고객센터 문의.
3) 최신 Actions 자동 재빌드 성공·구매자 안내 동일성 확인. 로컬 ZIP 15장 해시와 맞는지 검사.
4) 모든 RELEASE HOLD 해소 후 기존 840876에서 **15종 제목/5,900원/승인 이미지 6개/완성 buyer ZIP**으로 입력·제출. 신규 상품 생성 금지. 권리/보안 변경, 유료 결제·외부 업로드는 사용자 승인 범위 확인.
5) 실제 화면에서 '미제출 / 심사 대기 / 승인 / 판매 중' 구분하고 고유 상품 URL/증거/남은 문제 보고.

## 10. 갱신·검증 기준
2026-10-17 KST, 본 채팅에서 artifact 바이너리 다운로드·압축·해시 직접 검증, 연결 브라우저에서 기존 크몽 840876 편집 페이지 텍스트 확인. 사후 GitHub 최신 커밋은 `main` 재확인, 최신 Actions 런/심사 상태는 미확인 사항으로 표시.


### 2026-10-17 크몽 공식 운영정책 추가 확인
- 공식 노하우·콘텐츠 등록 가이드 (https://kmong.com/support/expert-center/posts/755): **자료·템플릿 최소 판매 금액 5,000원**, 5,900원 충족. 자료·템플릿은 ZIP 제출 지원, **파일당 200MB**.
- 카테고리 예시 (https://kmong.com/support/expert-center/posts/757): `취미 자료 > 기타`에는 도안·시안·컬러링북 등 예시가 있고, 예시에 없는 콘텐츠도 **기타로 등록하여 크몽이 검토/허용 여부 안내**하는 방식. 따라서 NAON2 단순 감상용 PNG 15장 상품을 이 카테고리로 **심사 제안할 근거는 있으나 실제 승인 확정 아님**.
- 수익금 (https://kmong.com/support/expert-center/posts/705): 서비스 이용료·결제 수수료/결제망 이용료·부가세 차감, 카테고리별 차이. 계정 '수익금 확인하기' 버튼을 실제 작동해 보지 못해 **5,900원 정확한 정산금 미확정**.
- 할인 (https://kmong.com/support/expert-center/posts/755): 할인 비교금액·적용기간의 증거가 필요하므로 7,900원 기존 판매가 취소선, 7,900→5,900 할인율 표기 금지. 단일 5,900원 등록 권고.
