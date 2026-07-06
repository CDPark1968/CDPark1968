# Telegram 안읽은 메시지 가져오기 - a-Shell(iPad/iPhone) 버전

[a-Shell](https://holzschu.github.io/a-Shell_iOS/)에서 `scripts/ashell/telegram_fetch_unread.py`를
실행하면 지난 24시간 안읽은 Telegram 메시지를 정리해서 화면에 보여주고, 파일로
저장하고, 클립보드에도 복사합니다. **요약/정리는 API 호출 없이, 이 텍스트를
Claude 앱에 붙여넣어서 직접 시키면 됩니다.** (Anthropic API 키 불필요, 별도 과금 없음)

## 1. a-Shell에 저장소 받기 (최초 1회)

a-Shell 앱을 열고:

```bash
git clone https://github.com/CDPark1968/CDPark1968.git
cd CDPark1968
git checkout claude/telegram-mcp-install-nko5p6   # PR이 아직 안 머지됐다면
pip install telethon
```

## 2. 설정 파일 만들기 (최초 1회)

```bash
cd scripts/ashell
cp telegram_fetch_config.json.example telegram_fetch_config.json
```

`telegram_fetch_config.json`을 열어 Telegram `api_id`, `api_hash`를 채워주세요.
(https://my.telegram.org/auth 에서 발급. 이 파일은 `.gitignore`에 포함되어
커밋되지 않습니다.)

## 3. 최초 실행 (로그인 겸 테스트)

```bash
python3 telegram_fetch_unread.py
```

로그인이 안 되어 있으면 전화번호와 인증 코드를 물어봅니다. 입력하면
`telegram_fetch_session` 세션 파일이 저장되어 이후에는 다시 로그인할 필요가
없습니다.

## 4. 평소 사용법 (이거만 반복하면 됨)

1. a-Shell 열고: `python3 ~/CDPark1968/scripts/ashell/telegram_fetch_unread.py`
2. 실행되면 안읽은 메시지 목록이 화면에 뜨고 **클립보드에 자동 복사**됩니다.
   (a-Shell 버전에 `pbcopy`가 없으면 화면 출력이나
   `scripts/ashell/unread_messages.txt` 파일을 대신 사용하세요.)
3. Claude 앱으로 전환해서 붙여넣기 → "중요도 순으로 정리해줘" 같은 요청

## (선택) 한 번에 실행하는 단축어 만들기

매번 a-Shell을 열고 경로를 치는 게 번거로우면, iOS **단축어** 앱에서 위 명령을
실행하는 단축어를 하나 만들어 홈 화면/위젯에 추가해두면 탭 한 번으로 실행할 수
있습니다 (a-Shell 버전에 따라 Shortcuts 연동 동작 이름이 다를 수 있으니, 안 되면
a-Shell 자체 문서를 참고하세요). 자동 스케줄 실행은 이 방식에서는 의미가 없습니다
— 어차피 결과를 Claude 앱에 직접 붙여넣는 수동 단계가 있기 때문입니다.

## 초기화

```bash
rm scripts/ashell/telegram_fetch_session* scripts/ashell/unread_messages.txt
```
