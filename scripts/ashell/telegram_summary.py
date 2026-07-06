#!/usr/bin/env python3
"""a-Shell(iOS/iPadOS)에서 실행하는 Telegram 안읽은 메시지 요약 스크립트.

Claude Code CLI는 a-Shell(Node.js 미지원)에서 실행할 수 없으므로, 이 스크립트는
Telethon으로 Telegram에 직접 접속하고 Anthropic API를 직접 호출해서 완결된
독립 스크립트로 동작한다.

최초 실행 시 로그인 정보가 없으면 Telethon이 자동으로 전화번호/인증코드를
interactive하게 물어본다 (a-Shell에서 직접 실행할 때만 가능. iOS 단축어로
실행할 때는 이미 로그인이 끝난 상태여야 한다).

사용 전 준비:
1. 이 폴더에 telegram_summary_config.json 파일을 만든다 (config.json.example 참고)
2. `pip install telethon`
3. a-Shell에서 직접 한 번 실행해서 로그인을 끝낸다: `python3 telegram_summary.py`
4. 이후에는 iOS 단축어 자동화로 같은 명령을 실행하면 된다.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

from telethon.sync import TelegramClient

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "telegram_summary_config.json")
SESSION_PATH = os.path.join(HERE, "telegram_summary_session")

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-sonnet-5"
UNREAD_LOOKBACK_HOURS = 24


def load_config():
    if not os.path.exists(CONFIG_PATH):
        sys.exit(
            f"{CONFIG_PATH} 가 없습니다. telegram_summary_config.json.example을 "
            "복사해서 값을 채워주세요."
        )
    with open(CONFIG_PATH) as f:
        return json.load(f)


def collect_unread(client, hours=UNREAD_LOOKBACK_HOURS):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    items = []
    for dialog in client.iter_dialogs():
        if dialog.unread_count <= 0:
            continue
        for m in client.get_messages(dialog.id, limit=dialog.unread_count):
            if not m.date or m.date < cutoff:
                continue
            text = (m.message or "").strip()
            if not text:
                continue
            sender = getattr(m.sender, "first_name", None) or str(m.sender_id)
            items.append(
                {
                    "chat": dialog.name,
                    "sender": sender,
                    "text": text,
                    "is_private": dialog.is_user,
                    "mentioned": bool(m.mentioned),
                }
            )
    return items


def summarize_with_claude(items, api_key):
    if not items:
        return "지난 24시간 동안 안 읽은 메시지가 없습니다."

    lines = []
    for it in items:
        tag = "1:1" if it["is_private"] else ("멘션" if it["mentioned"] else "그룹")
        lines.append(f"[{tag}] {it['chat']} - {it['sender']}: {it['text']}")

    prompt = (
        "다음은 지난 24시간 동안 내 Telegram에 온 안 읽은 메시지 목록이다. "
        "중요도 순으로 정리한 한국어 요약을 만들어줘.\n\n"
        "중요도 기준:\n"
        "- 높음: 1:1 메시지, 나를 멘션/답장한 메시지, 마감·일정·확인 요청 등 "
        "시간에 민감한 내용\n"
        "- 낮음: 그 외 일반 그룹 대화 (건수만 요약)\n\n"
        "각 항목은 대화방 이름, 보낸 사람, 핵심 내용 한 줄로 정리해줘.\n\n"
        "메시지 목록:\n" + "\n".join(lines)
    )

    payload = json.dumps(
        {
            "model": ANTHROPIC_MODEL,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=payload,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.load(resp)
    return "".join(block.get("text", "") for block in result.get("content", []))


def main():
    config = load_config()
    with TelegramClient(SESSION_PATH, config["api_id"], config["api_hash"]) as client:
        items = collect_unread(client)
        summary = summarize_with_claude(items, config["anthropic_api_key"])
        client.send_message("me", summary)
    print("요약을 Saved Messages로 보냈습니다.")


if __name__ == "__main__":
    main()
