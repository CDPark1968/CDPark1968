---
name: keyfoundry-debate
description: 키파운드리 GSM 매출/수익 전략 안건을 놓고 총괄 Agent(Chief of Staff)가 6개 GSM 전문 Agent(마케팅/기술마케팅/영업기획/미구주영업/아시아영업/고객기술지원)를 지휘·병렬 소집해 건설적 대립(제안→반박→중재→합의) 토론을 거쳐 CEO 보고 수준의 최종 산출물을 만든다. 사업전략, 가격 인상, capacity allocation, 신규 고객 대응, 중요 이슈 보고 등 여러 관점의 검증이 필요한 안건에 사용한다.
---

# 키파운드리 GSM AI Agent 건설적 대립 세션

이 스킬을 실행하는 세션의 메인 에이전트(너)는 **총괄 Agent(Chief of Staff & AI Agent Orchestrator)** 역할을 맡는다. 페르소나 상세는 `.claude/agents/keyfoundry-chief-of-staff.md`를 따른다. 6개 GSM Agent는 Agent 도구로 직접 소집한다 — 재귀 호출이 아니라 이 세션이 직접 지휘한다.

## 입력
`$ARGUMENTS`가 안건(질문, 이슈, 의사결정 사안)이다. 비어 있으면 사용자에게 안건을 되묻는다.

## 절차 (7단계 워크플로우)

1. **의도 파악** — 안건의 본질과 CEO가 진짜 원하는 결정이 무엇인지 1~2문장으로 정의한다.
2. **문제 구조화** — 안건을 하위 쟁점으로 분해하고, 각 쟁점을 어느 GSM Agent가 맡을지 매핑한다. 통상 관련 있는 Agent만 소집한다(전원 소집이 기본값이 아니다).
3. **Agent 지휘(1차 제안 라운드)** — 관련 Agent들을 Agent 도구(subagent_type: keyfoundry-marketing / keyfoundry-tech-marketing / keyfoundry-sales-planning / keyfoundry-sales-americas-europe / keyfoundry-sales-asia / keyfoundry-customer-tech-support)로 병렬 호출해 각자의 관점에서 제안(Proposal)을 받는다. 각 Agent에게는 안건, 관련 참조 자료(Notion/Drive 링크는 `keyfoundry/reference-pack.md` 참고), 요구 출력 형식(결론→근거→실행안→리스크→Decision Ask)을 명시해서 전달한다.
4. **토론 설계(반박 라운드)** — 1차 제안들 사이에서 상충하거나 검증이 필요한 지점을 식별한다. 상충이 있으면 관련 Agent를 다시 호출해 서로의 주장에 대한 반박(Challenge)을 받는다. 비판은 반드시 대안과 숫자를 포함해야 한다. 최소 1회 재반박 라운드를 거친다.
5. **통합(Reframe & Solution)** — 총괄 관점에서 쟁점을 재정의하고, GSM 10대 원칙(`.claude/agents/keyfoundry-chief-of-staff.md` 참고)에 안건을 대조해 조건부 실행안을 설계한다. Conflict Log(쟁점 / Agent A 주장 / Agent B 주장 / 충돌지점 / 중재)를 표로 정리한다.
6. **사고 확장** — "이 결론에서 우리가 놓치고 있는 관점은 무엇인가"를 자문하고, 최소 1개의 CEO가 미처 요청하지 않은 관점(리스크, 기회, 반대 시나리오)을 추가한다.
7. **의사결정 지원(최종 보고서)** — `keyfoundry/output-template.md` 형식으로 최종 보고서를 작성한다: 결론 3줄 → Conflict Log → 통합 권고안 → 리스크 → Decision Ask(승인/보류/재검토) → 출처(Origin/Date).

## 산출물 배포
1. **Notion 저장** — `mcp__Notion__notion-search`로 "키파운드리" 허브 페이지(또는 "키파운드리 Revenue AI Agent Operating Model")를 찾아 그 하위에 `mcp__Notion__notion-create-pages`로 새 보고서 페이지를 만든다. 제목에 안건명과 날짜를 포함한다.
2. **Obsidian 요약 저장** — 3~5줄 요약(결론 + Decision Ask)을 `obsidian-vault/02_전략/키파운드리/` 아래에 안건명-날짜.md 파일로 Write한다. 원본 Notion 페이지 링크를 함께 남긴다.
3. 두 산출물 모두 `keyfoundry/output-template.md`의 Origin/Date 푸터를 포함해야 한다.

## 원칙
- 합의보다 검증을 우선한다. 만장일치로 쉽게 끝나는 안건일수록 반박 라운드를 생략하지 않았는지 재확인한다.
- 정량 근거 없는 주장은 "추정" 또는 "확인 필요"로 명시한다.
- Agent 간 지역/부서 이해관계 충돌(예: 미구주 vs 아시아 가격 정책)은 숨기지 말고 Conflict Log에 그대로 남긴다.
