# GitHub 저장소 상태

- 저장소: `hibi89/NAON2-Character-Studio`
- 브랜치: `main` · 공개 범위: `private`
- 원본 PNG 2개 + 승인된 표준화 PNG 1개: **GitHub 등록 완료**
- 업로드 원본과 로컬 파일의 Git blob SHA: **3/3 일치**
- 문서와 캐릭터 기획·크몽 상품 설계: `main`에 커밋 완료
- 이미지 비교 기록: `docs/ASSET_VERIFICATION_2026-10-16.md`

## 검증 방법
GitHub의 git tree에 기록된 blob SHA는 이미지 파일의 실제 바이트를 기반으로 생성된 Git SHA-1입니다.
로컬 계산: `SHA1("blob " + byte_length + "\\0" + bytes)`. 단순 파일 SHA-1과는 다른 값입니다.

기존 `asset-manifest.json`의 SHA-256과 픽셀 해상도 확인 스크립트는 별도로 보존합니다. 앞으로 새로운 캐릭터 마스터/파생 원화를 추가할 때는 원본을 덮어쓰지 않습니다.
