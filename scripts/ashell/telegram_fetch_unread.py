#!/usr/bin/env python3
"""a-Shell(iPad/iPhone)에서 실행: Telegram 안읽은 메시지를 모아 정리된 텍스트로
출력하고 iOS 클립보드에 복사한다. 요약/정리는 이 텍스트를 Claude 앱에 붙여넣어서
직접 시킨다 (이 스크립트는 API 호출을 하지 않는다).

최초 실행 시 로그인 정보가 없으면 Telethon이 전화번호/인증코드를 물어본다.
이후에는 세션이 저장되어 다시 로그인할 필요가 없다.

사용 전 준비:
1. telegram_fetch_config.json 을 만든다 (telegram_fetch_config.json.example 참고)
2. `pip install telethon`
3. a-Shell에서 실행: `python3 telegram_fetch_unread.py`
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

from telethon.sync import TelegramClient

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "telegram_fetch_config.json")
SESSION_PATH = os.path.join(HERE, "telegram_fetch_session")
OUTPUT_PATH = os.path.join(HERE, "unread_messages.txt")

UNREAD_LOOKBACK_HOURS = 24


def load_config():
    if not os.path.exists(CONFIG_PATH):
        sys.exit(
            f"{CONFIG_PATH} 가 없습니다. telegram_fetch_config.json.example을 "
            "복사해서 api_id / api_hash 값을 채워주세요."
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
            tag = "1:1" if dialog.is_user else ("멘션" if m.mentioned else "그룹")
            items.append(f"[{tag}] {dialog.name} - {sender}: {text}")
    return items


def copy_to_clipboard(text):
    try:
        subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def main():
    config = load_config()
    client = TelegramClient(SESSION_PATH, config["api_id"], config["api_hash"])
    # a-Shell's terminal doesn't support getpass's masked-input prompt, so the
    # 2FA password (if the account has one) must come from config instead of
    # being typed interactively.
    client.start(password=config.get("password"))
    try:
        items = collect_unread(client)
    finally:
        client.disconnect()

    if items:
        body = "지난 24시간 동안 안 읽은 Telegram 메시지:\n\n" + "\n".join(items)
    else:
        body = "지난 24시간 동안 안 읽은 Telegram 메시지가 없습니다."

    with open(OUTPUT_PATH, "w") as f:
        f.write(body)

    print(body)
    print(f"\n---\n{OUTPUT_PATH} 에 저장했습니다.")

    if copy_to_clipboard(body):
        print("클립보드에도 복사했습니다. Claude 앱에 붙여넣어서 요약을 시켜보세요.")
    else:
        print(
            "이 a-Shell 버전엔 pbcopy가 없어 클립보드 복사는 건너뛰었습니다. "
            f"위 내용을 직접 선택해 복사하거나 {OUTPUT_PATH} 파일을 Claude 앱에 "
            "공유하세요."
        )


if __name__ == "__main__":
    main()
