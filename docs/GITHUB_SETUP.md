# GitHub 연동 및 바이너리 업로드 현황

- 저장소: `hibi89/NAON2-Character-Studio`
- Branch: `main`; Visibility: `private`
- 기존 프로젝트로부터 분리된 전용 저장소
- 텍스트 문서: ChatGPT GitHub 커넥터를 통해 커밋
- PNG 이미지 3개: 현재 GitHub 커넥터와 작업 공간 사이의 바이너리 전달 경로가 없어 업로드 대기

## 이미지 업로드 대안 (강제 push 금지)
1. [프로젝트 초기 ZIP] 압축을 풀어 원본 이미지 파일 3개를 확인합니다.
2. GitHub `assets/originals/`, `assets/references/` 폴더 경로로 원본 PNG를 그대로 업로드합니다.
3. `python scripts/verify_assets.py` 실행 후 `asset-manifest.json`의 SHA-256과 픽셀 크기가 일치하는지 검증합니다.
4. GitHub 파일 존재 여부, 커밋 SHA, Author/Committer 확인.

원본은 재인코딩하거나 임의 변경하지 않습니다.