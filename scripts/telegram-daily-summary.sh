#!/usr/bin/env bash
# 매일 실행되어 지난 24시간 Telegram 안읽은 메시지를 중요도순으로 요약해서
# Saved Messages(entity="me")로 보내는 스크립트. launchd/cron에서 이 스크립트를 호출한다.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -f .env.local ]; then
  set -a
  source .env.local
  set +a
fi

PROMPT='mcp__telegram__* 도구를 사용해서 다음을 수행해줘:
1. search_dialogs로 최근 대화 목록을 확인한다.
2. 각 대화에서 get_messages(unread=true)로 지난 24시간 안읽은 메시지를 가져온다.
3. 아래 기준으로 중요도를 매겨 정리한다.
   - 높음: 나에게 온 1:1 메시지, 그룹에서 나를 멘션/답장한 메시지, 마감·일정·확인 요청 등 시간에 민감한 내용
   - 낮음: 그 외 일반 그룹 대화 (건수만 요약)
4. 대화방 이름, 보낸 사람, 핵심 내용 한 줄로 정리한 한국어 요약을 작성한다.
5. send_message(entity="me", message=요약)으로 Saved Messages에 전송한다.
메시지를 읽음 처리(mark_as_read)하지는 마.'

claude -p "$PROMPT" \
  --allowed-tools "mcp__telegram__search_dialogs,mcp__telegram__get_messages,mcp__telegram__send_message"
