# 키파운드리 GSM Revenue AI Agent 조직

키파운드리(SK Keyfoundry) GSM의 매출·수익 전략을 위한 7-Agent 체계. 설계 원문은 Notion [키파운드리 Revenue AI Agent Operating Model](https://app.notion.com/p/3928899a479481f580e4ebef4e9b1a51)이며, 이 레포는 그 설계를 Claude Code에서 실제로 구동 가능한 형태로 구현한다.

## 구성

| Agent | 정의 파일 | 역할 |
|---|---|---|
| 총괄 (Chief of Staff) | `.claude/agents/keyfoundry-chief-of-staff.md` | 의도 파악, 문제 구조화, Agent 지휘, 토론 설계, 통합, 사고 확장, 의사결정 지원 |
| 마케팅 | `.claude/agents/keyfoundry-marketing.md` | 사업계획, 수익성, 신제품, 가격/할당 가이드, 중장기 판매계획, 시장/경쟁 분석 |
| 기술마케팅 | `.claude/agents/keyfoundry-tech-marketing.md` | 경쟁사 tech node/type, 고객 tech trend, 미래 전망, 고객 수요(tech) 분석 |
| 영업기획 | `.claude/agents/keyfoundry-sales-planning.md` | 캐파 반영 mix 최적화, delivery 관리, 실행판매계획, 실적/누적 관리 |
| 미구주영업 | `.claude/agents/keyfoundry-sales-americas-europe.md` | 판매 극대화, 가격 인상/방어, 대응 논리, 고객 분석, talking point, mix 조정 |
| 아시아영업 | `.claude/agents/keyfoundry-sales-asia.md` | 위와 동일 역할을 아시아(한중일대만동남아) 고객 대상으로 수행 |
| 고객기술지원 | `.claude/agents/keyfoundry-customer-tech-support.md` | 이력/사례 기반 inquiry 대응, 불량 대응 논리 개발 |

## 사용법

```
/keyfoundry-debate <안건>
```

예: `/keyfoundry-debate MPS 45K 요청 수용 여부와 가격 조건`

세션은 총괄 Agent 역할로 관련 GSM Agent를 병렬 소집해 제안→반박→중재→합의의 건설적 대립 과정을 거치고, `keyfoundry/output-template.md` 형식의 CEO 보고서를 만든다.

개별 Agent만 단독으로 쓰고 싶으면 Agent 도구로 `subagent_type: keyfoundry-marketing` 등으로 직접 호출한다.

## 참조 체계
3원 참조(Notion·Google Drive·Obsidian) 연결과 우선순위는 `keyfoundry/reference-pack.md`를 따른다.

## 출력 규칙
모든 최종 산출물은 `keyfoundry/output-template.md` 형식을 따르고, 전문은 Notion에, 요약은 `obsidian-vault/02_전략/키파운드리/`에 저장하며, Origin(Codex/Claude Code)과 생성 날짜를 표기한다.

## Obsidian 로컬 연결
Obsidian 볼트(iCloud Drive 동기화)는 이 원격 세션에서 직접 접근할 수 없어, git을 동기화 브릿지로 쓴다. 최초 1회 설정은 `obsidian-vault/SETUP.md`를 따르고, 이후에는 로컬에서 `git pull`만 하면 새 요약 노트가 Obsidian에 자동 반영된다.
