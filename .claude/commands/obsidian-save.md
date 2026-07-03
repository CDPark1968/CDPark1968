# /obsidian-save

현재 대화에서 생성된 보고서나 전략 문서를 Google Drive의 키파운드리 폴더에 Obsidian 호환 마크다운 파일로 저장합니다.

## 실행 지침

1. 사용자가 저장할 내용을 인자로 넘기거나, 인자가 없으면 직전에 생성한 주요 문서/전략을 저장 대상으로 판단합니다.
2. 파일명 규칙: `YYYYMMDD_[제목]_v1.md` (예: `20260703_10대전략제안_v1.md`)
3. Google Drive MCP 도구를 사용해 키파운드리 폴더(ID: 1d1HHUsWn-l9FnzPf-J8ePhAN1tfnOIAy)에 저장합니다.
4. Obsidian 호환 포맷으로 저장:
   - YAML frontmatter 포함 (tags, date, source)
   - 헤딩 계층 (#, ##, ###) 유지
   - 내부 링크 [[]] 스타일 사용 가능
5. 저장 완료 후 파일 ID와 링크를 사용자에게 알립니다.

## 저장 포맷 예시

```
---
tags: [키파운드리, 전략, 마케팅]
date: YYYY-MM-DD
source: Claude AI
---

# 제목

내용...
```

## 주의사항

- 이 환경은 원격 클라우드이므로 로컬 Obsidian vault에 직접 쓸 수 없습니다.
- Google Drive에 저장 후, Obsidian의 "Remotely Save" 플러그인 또는 Google Drive 동기화 앱으로 로컬 vault와 연동하세요.
- 또는 Google Drive에서 파일을 다운로드해 vault에 수동으로 복사하세요.
