# Telegram MCP 설정 가이드

이 저장소에는 [mcp-telegram](https://github.com/sparfenyuk/mcp-telegram) 서버를 사용하는
`.mcp.json`이 포함되어 있습니다. 이 서버는 사용자 계정(API ID/Hash) 기반으로 동작하며,
Claude Code가 내 Telegram 대화 목록과 메시지를 읽을 수 있게 해줍니다. (현재는 읽기 전용)

## 사전 준비물

- [uv](https://docs.astral.sh/uv/) 설치 (`uvx` 명령 포함)
- https://my.telegram.org/auth 에서 발급받은 `api_id`, `api_hash`

## 1. Telegram API 자격 증명 발급

1. https://my.telegram.org/auth 에 로그인 (본인 전화번호 사용)
2. "API development tools" 클릭 후 새 애플리케이션 생성
3. 발급된 `App api_id`와 `App api_hash`를 기록 (api_hash는 외부에 노출하지 말 것)

## 2. 환경 변수 설정

`.mcp.json`은 아래 두 환경 변수를 참조합니다. 저장소에 값을 커밋하지 않도록
로컬 셸 환경(예: `~/.zshrc`, `~/.bashrc`)이나 실행 환경의 secret 설정에 값을 넣어주세요.

```bash
export TELEGRAM_API_ID="<발급받은 api_id>"
export TELEGRAM_API_HASH="<발급받은 api_hash>"
```

## 3. 최초 1회 로그인 (세션 생성)

서버가 사용할 Telegram 세션을 만들기 위해 최초 1회 로그인이 필요합니다.

```bash
uvx mcp-telegram sign-in --api-id "$TELEGRAM_API_ID" --api-hash "$TELEGRAM_API_HASH" --phone-number "<본인 전화번호, 예: +821012345678>"
```

Telegram으로 전송된 인증 코드를 입력하면 세션 파일이
`~/.local/state/mcp-telegram/mcp_telegram_session` 에 저장됩니다.
이후에는 Claude Code가 이 세션을 재사용하므로 다시 로그인할 필요가 없습니다.

## 4. 동작 확인

Claude Code를 이 저장소에서 실행하면 `.mcp.json`에 정의된 `telegram` MCP 서버가
자동으로 로드됩니다. `/mcp` 명령으로 서버 연결 상태를 확인할 수 있습니다.

## 로그아웃

```bash
uvx mcp-telegram logout
```
