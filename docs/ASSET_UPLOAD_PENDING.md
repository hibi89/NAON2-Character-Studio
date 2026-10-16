# PNG 바이너리 업로드 대기

문서와 검증 코드는 GitHub `main`에 등록됐지만, 현재 GitHub 커넥터가 작업 공간의 이미지 파일을 바이너리로 직접 업로드하지 못해 3개 PNG는 아직 원격 저장소에 없습니다.

| 경로 | 원본 크기 |
| --- | ---: |
| `assets/originals/naon2-gamer-original.png` | 96,666 bytes |
| `assets/originals/naon2-astronaut-original.png` | 3,681,149 bytes |
| `assets/references/naon2-character-sheet-v1.png` | 2,237,668 bytes |

이미지는 이 대화에서 제공된 `NAON2-Character-Studio-initial.zip` 안에 변경 없이 보존됐습니다. 이 ZIP을 다운로드해 보관하십시오. GitHub에 파일들을 업로드할 때 임의로 압축하거나 다시 저장하지 마십시오.

업로드 후 `python scripts/verify_assets.py`로 SHA-256·크기·해상도를 비교합니다. 원본별 해시는 `asset-manifest.json`을 참고하십시오.
