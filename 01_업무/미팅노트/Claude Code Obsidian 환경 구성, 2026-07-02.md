---
date: 2026-07-02
category: 업무
tags: [업무, Claude-Code, Obsidian, 환경구성]
---

# Claude Code × Obsidian 환경 구성 완료

> 2026-07-02 | a-Shell (iPad) + Claude Code 웹 세션

---

## 설치 완료 항목

| 항목 | 위치 | 상태 |
|------|------|------|
| `kepano/obsidian-skills` | 볼트 `.claude/skills/` | ✅ |
| `obsidian-second-brain` | 볼트 `.claude/skills/` + `.claude/commands/` | ✅ |
| `obsidian-mind` | 볼트 `.claude/agents/` + `brain/` | ✅ |
| `brain/North Star.md` | 볼트 `brain/` | ✅ |
| 슬래시 명령어 5개 | `cdpark1968` repo `.claude/commands/` | ✅ |

---

## 사용 가능한 명령어

- `/obsidian-save` — 대화 내용 볼트 저장
- `/obsidian-daily` — 오늘 일간 노트 생성
- `/om-dump [메모]` — 자유형식 메모 캡처
- `/om-standup` — 아침 업무 브리핑
- `/om-wrap-up` — 하루 마무리 정리

---

## a-Shell 설치 시 배운 것

- `pkg install git` 필요 (설치 시 `y` 입력)
- `$(...)` 문법 미지원 → 변수 저장 불가
- `curl` 없음 → `python3 -c "import urllib.request; ..."` 으로 대체
- `pickFolder` 후 이동 없이 바로 실행해야 볼트 인식

---

## 관련 노트

- [[brain/North Star]]
- [[02_전략/MPS]]
