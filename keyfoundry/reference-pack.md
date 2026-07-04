# 키파운드리 GSM AI Agent — 3원 참조 팩 (Notion · Google Drive · Obsidian)

모든 GSM Agent와 `/keyfoundry-debate` 세션은 결론을 내리기 전 아래 3개 소스를 우선 참조한다.

## 1. Notion
- [키파운드리](https://app.notion.com/p/2bb8899a479481d59a8de4a223335c40) — 허브 페이지
- [키파운드리 Revenue AI Agent Operating Model](https://app.notion.com/p/3928899a479481f580e4ebef4e9b1a51) — Agent 조직 설계 원문(본 레포의 코드 구현과 1:1 대응)
- [키파운드리 경쟁사 분석 및 전략](https://app.notion.com/p/2ca8899a47948195b027ed7f42697925)
- [GSM Principle 키파운드리](https://app.notion.com/p/3788899a479481c58298e5d9f6ccfb7d) — GSM 10대 원칙
- [PARK CD OS v1.0](https://app.notion.com/p/3928899a479481819e7fe6b6d007a4bd) — 의사결정 프레임(End Market→System→Chip→Process→Fab→Revenue→Profit)

새 산출물은 위 허브 페이지 하위에 생성해 상호 링크가 끊기지 않게 한다.

## 2. Google Drive — 키파운드리 폴더
폴더: https://drive.google.com/drive/folders/1d1HHUsWn-l9FnzPf-J8ePhAN1tfnOIAy

| 파일 | 용도 |
|---|---|
| [KeyFoundry Market Diagnosis 2026.docx](https://drive.google.com/file/d/1q2GUBKBpye9K9tyx-YG1p8CWvfEA9u9P/view) | 2026 AI 서버발 전력반도체 시장 구조 전환 진단 — 수요·공급·가격 근거. Marketing/Tech Marketing Agent 1순위 참조 |
| [하반기 웍샾 아젠다.docx](https://drive.google.com/file/d/1MZ2EnOXD3MIRguGHXt2gN3zZmEMCV1cF/view) | H2 2026 Executive Workshop 스토리라인·아젠다 설계안. Sales Planning/총괄 Agent 회의 안건 구조 참조 |
| [KeyFoundry H2Workshop 2026.docx](https://drive.google.com/file/d/1ATcqN-M6tXtfnxjdC6CcAwwg_KD4B6Ts/view) | 위 아젠다의 실행판 워크숍 덱(하이닉스 미팅 근거, Vcore 본질, 가격 실행) — 보조 참조 |
| SK Keyfoundry GSM 27Co Weekly Heatmap (xlsm, 3종) | 27개사 위클리 트래킹 시트 — Sales Planning/Asia Sales Agent 실적·경쟁 모니터링 |

> 두 핵심 파일(Market Diagnosis, 하반기 웍샾 아젠다)은 요청 시점에 다른 파일명으로 이미 폴더에 존재해 검색으로 재확인했다. 파일 ID 기준으로 링크했으므로 향후 파일명이 다시 바뀌어도 링크는 유지된다.

## 3. Obsidian
Obsidian 볼트는 iCloud Drive로 동기화되며, iCloud Drive·Obsidian 모두 이 원격 세션에서 접근 가능한 API/MCP가 없다(둘 다 공개 커넥터가 없음). 그래서 **git을 동기화 브릿지로 사용**한다 — 이 레포의 `obsidian-vault/` 폴더가 볼트의 실제 위치와 symlink로 연결된다.

- 경로 규칙(레포 쪽): `obsidian-vault/02_전략/키파운드리/`
- 로컬 연결 설정 방법: `obsidian-vault/SETUP.md` 참고(최초 1회 symlink 설정 후, 매번 `git pull`만 하면 Obsidian에 자동 반영)
- `/keyfoundry-debate` 실행마다 `<안건명>-<YYYY-MM-DD>.md` 요약 노트를 레포의 위 경로에 생성·커밋·푸시한다.

## 사용 우선순위
1. Notion에서 기존 결론·원칙과의 정합성 확인
2. Google Drive에서 최신 시장/실행 근거 확인
3. Obsidian 요약본은 근거가 아니라 "빠른 회상용" 최종 요약으로만 사용
