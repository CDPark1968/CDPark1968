# Telegram 요약 - a-Shell(iPhone/iPad) 버전

[a-Shell](https://holzschu.github.io/a-Shell_iOS/)은 iOS/iPadOS 터미널 앱으로,
Node.js를 지원하지 않아 Claude Code CLI(`claude` 명령)를 그 안에서 실행할 수
없습니다. 대신 `scripts/ashell/telegram_summary.py`가 Telethon으로 Telegram에
직접 접속하고, Anthropic API를 직접 호출해 요약까지 끝내는 독립 스크립트입니다.
Claude.ai 구독과는 별개로 **Anthropic API 사용량 기반 과금**이 발생합니다.

## 0. 준비물

- Telegram `api_id` / `api_hash` (https://my.telegram.org/auth 에서 발급, 이미 있다면 재사용)
- Anthropic API 키 (https://console.anthropic.com → API Keys → Create Key)
  - Claude.ai 로그인 계정과 같은 계정으로 콘솔에 로그인 후 발급하면 됩니다.
  - 발급한 키(`sk-ant-...`)는 외부에 노출하지 마세요.

## 1. a-Shell에 저장소 받기

a-Shell 앱을 열고:

```bash
git clone https://github.com/CDPark1968/CDPark1968.git
cd CDPark1968
git checkout claude/telegram-mcp-install-nko5p6   # PR이 아직 안 머지됐다면
```

## 2. 의존성 설치

```bash
pip install telethon
```

(a-Shell의 pip은 순수 Python 패키지 위주로 지원됩니다. telethon은 순수 Python으로도
동작하니 설치가 안 되는 하위 패키지가 있어도 대부분 무시하고 진행해도 됩니다.)

## 3. 설정 파일 만들기

```bash
cd scripts/ashell
cp telegram_summary_config.json.example telegram_summary_config.json
```

`telegram_summary_config.json`을 열어 `api_id`, `api_hash`, `anthropic_api_key`
값을 채워주세요. 이 파일은 `.gitignore`에 포함되어 커밋되지 않습니다.

## 4. 최초 실행 (로그인 겸 테스트)

```bash
python3 telegram_summary.py
```

로그인이 안 되어 있으면 전화번호와 인증 코드를 물어봅니다. 입력하면
`telegram_summary_session` 세션 파일이 같은 폴더에 생성되고, 이후에는 다시
로그인할 필요가 없습니다. 성공하면 Telegram "저장한 메시지"에 요약이 도착합니다.

## 5. 매일 아침 자동 실행 (iOS 단축어)

iOS는 앱이 꺼진 상태에서 자체적으로 백그라운드 스케줄을 실행할 수 없으므로,
iOS의 **단축어(Shortcuts) 앱 → 개인 자동화**로 a-Shell 명령을 매일 정해진
시간에 실행시킵니다.

1. 단축어 앱 → **자동화** 탭 → **+** → **개인 자동화 생성**
2. **시간대** 선택 → 매일 오전 8시로 설정
3. **즉시 실행**을 켜서(확인 없이 실행) 알림 없이 바로 실행되게 설정
4. 동작 추가에서 **a-Shell**을 검색해 명령 실행 동작을 추가
   (a-Shell 버전에 따라 동작 이름이 다를 수 있습니다. a-Shell 안에서 `help shortcuts`
   또는 앱 내 도움말을 참고해 정확한 동작 이름/사용법을 확인하세요.)
5. 명령으로 아래를 입력 (경로는 실제 clone 위치에 맞게 조정)

   ```
   python3 ~/CDPark1968/scripts/ashell/telegram_summary.py
   ```

6. 저장 후 폰이 켜져 있고 잠금 해제된 시간대에 잘 동작하는지 며칠 확인해보세요.
   (iOS 자동화는 기기 상태에 따라 정확히 그 시각에 실행되지 않을 수 있습니다.)

> a-Shell의 Shortcuts 연동 세부 동작은 앱 업데이트에 따라 바뀔 수 있어 이 문서에서
> 100% 보장은 못 드립니다. 안 되면 a-Shell 자체 문서(GitHub Wiki)를 확인하거나,
> 대안으로 매일 아침 앱을 직접 열어 `python3 ~/CDPark1968/scripts/ashell/telegram_summary.py`
> 를 수동 실행하는 방법도 있습니다.

## 로그아웃 / 초기화

```bash
rm scripts/ashell/telegram_summary_session*
```
