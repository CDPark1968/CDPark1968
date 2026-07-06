# Telegram MCP 설정 가이드

이 저장소에는 [mcp-telegram](https://github.com/sparfenyuk/mcp-telegram) 서버를 사용하는
`.mcp.json`이 포함되어 있습니다. 이 서버는 사용자 계정(API ID/Hash) 기반으로 동작하며,
Claude Code가 내 Telegram 대화 목록/메시지를 읽고, 나에게(Saved Messages) 메시지를
보낼 수 있게 해줍니다.

> **주의**: Telegram은 MTProto(원시 TCP)와 HTTPS 도메인 접근이 모두 필요합니다.
> 아웃바운드 네트워크가 화이트리스트로 제한된 환경(예: claude.ai/code의 원격 클라우드
> 세션)에서는 Telegram 서버 접속 자체가 막혀 동작하지 않습니다. **네트워크 제한이 없는
> 로컬 PC에서 설정/실행**하세요.

## 사전 준비물

- [uv](https://docs.astral.sh/uv/) 설치 (`uvx` 명령 포함)
- Claude Code CLI (`claude` 명령) 설치
- https://my.telegram.org/auth 에서 발급받은 `api_id`, `api_hash`

## 1. Telegram API 자격 증명 발급

1. https://my.telegram.org/auth 에 로그인 (본인 전화번호 사용)
2. "API development tools" 클릭 후 새 애플리케이션 생성 (이름은 아무거나)
3. 발급된 `App api_id`와 `App api_hash`를 기록 (api_hash는 재발급이 안 되니 외부 노출 금지)

## 2. 환경 변수 설정

`.mcp.json`은 `TELEGRAM_API_ID`, `TELEGRAM_API_HASH` 두 환경 변수를 참조합니다.
저장소에 값을 커밋하지 않도록, 이 저장소 루트에 `.env.local`을 만들어 채워주세요
(`.env.local`은 `.gitignore`에 등록되어 커밋되지 않습니다).

```bash
cp .env.local.example .env.local
# .env.local을 열어 TELEGRAM_API_ID / TELEGRAM_API_HASH 값을 채운다
set -a && source .env.local && set +a
```

## 3. 최초 1회 로그인 (세션 생성)

```bash
uvx mcp-telegram login
```

API ID / API Hash / 전화번호를 순서대로 물어보고, Telegram으로 전송된 인증 코드를
입력하면 로그인됩니다. 세션 파일은
`~/.local/state/mcp-telegram/mcp_telegram_session` 에 저장되며, 이후 Claude Code가
이 세션을 재사용하므로 다시 로그인할 필요가 없습니다.

## 4. 동작 확인

이 저장소 디렉터리에서 `claude`를 실행하면 `.mcp.json`에 정의된 `telegram` MCP 서버가
자동으로 로드됩니다. `/mcp` 명령으로 서버 연결 상태를 확인하고, "내 안 읽은 메시지
보여줘" 같은 요청으로 테스트해보세요.

## 5. 매일 아침 중요도별 요약 자동화 (macOS, launchd)

`scripts/telegram-daily-summary.sh`가 지난 24시간 안읽은 메시지를 중요도순으로
정리해 Telegram Saved Messages(`entity="me"`)로 보내줍니다.

1. 스크립트에 실행 권한 부여

   ```bash
   chmod +x scripts/telegram-daily-summary.sh
   ```

2. 직접 실행해서 테스트

   ```bash
   ./scripts/telegram-daily-summary.sh
   ```

   Telegram 앱의 "저장한 메시지"에 요약이 도착하면 성공입니다.

3. launchd에 등록해서 매일 아침 8시에 자동 실행되도록 설정

   `~/Library/LaunchAgents/com.cdpark.telegram-summary.plist` 파일을 아래 내용으로
   만들고, `<REPO_PATH>`를 이 저장소의 절대 경로로 바꿔주세요.

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
     <key>Label</key><string>com.cdpark.telegram-summary</string>
     <key>ProgramArguments</key>
     <array>
       <string>/bin/bash</string>
       <string>-lc</string>
       <string>REPO_PATH/scripts/telegram-daily-summary.sh >> /tmp/telegram-summary.log 2>&amp;1</string>
     </array>
     <key>StartCalendarInterval</key>
     <dict>
       <key>Hour</key><integer>8</integer>
       <key>Minute</key><integer>0</integer>
     </dict>
   </dict>
   </plist>
   ```

   (스크립트가 `.env.local`을 직접 읽으므로 plist에는 별도 환경 변수를 넣지 않아도
   됩니다.)

   등록 및 확인:

   ```bash
   launchctl load ~/Library/LaunchAgents/com.cdpark.telegram-summary.plist
   launchctl list | grep telegram-summary
   ```

   해제하려면:

   ```bash
   launchctl unload ~/Library/LaunchAgents/com.cdpark.telegram-summary.plist
   ```

   노트북이 8시에 잠들어 있으면 launchd가 깨어난 직후(또는 다음 실행 시점)에
   실행합니다. 정확히 그 시각에 실행되길 원하면 절전 모드 해제 스케줄을 별도로
   설정하세요.

## 로그아웃 / 세션 삭제

```bash
uvx mcp-telegram logout       # 로그아웃 안내
uvx mcp-telegram clear-session  # 로컬 세션 파일 삭제
```
