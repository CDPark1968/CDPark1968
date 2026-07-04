# Obsidian 로컬 동기화 설정 (git 브릿지)

Obsidian은 iCloud Drive로 볼트를 동기화하고 있고, iCloud Drive와 Obsidian 모두 이 원격 세션에서 접근 가능한 API/MCP가 없다. 대신 **이 git 레포를 로컬 볼트와 파일 시스템 레벨에서 연결**해서, 세션이 커밋·푸시할 때마다 `git pull` 한 번으로 Obsidian에 반영되게 한다.

## 사전 확인
Obsidian 볼트의 실제 경로(맥 기준, iCloud Drive 동기화 볼트인 경우 보통 아래 형태다):
```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<볼트이름>
```
Finder에서 볼트를 iCloud Drive 안에서 우클릭 → "정보 가져오기"로 정확한 경로를 확인한다. 아래 예시의 `<VAULT_PATH>`를 이 경로로 바꿔서 사용한다.

## 설정 (최초 1회)

1. 이 레포를 로컬 아무 위치에 clone한다 (볼트 밖 — 예: `~/dev/CDPark1968`):
   ```bash
   git clone https://github.com/CDPark1968/CDPark1968.git ~/dev/CDPark1968
   cd ~/dev/CDPark1968
   git checkout claude/keyfoundry-ai-agents-vzfyfp
   ```

2. 레포 안의 `obsidian-vault/02_전략/키파운드리` 폴더를 실제 볼트의 `02_전략/키파운드리` 자리에 symlink로 연결한다:
   ```bash
   VAULT_PATH="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/<볼트이름>"
   mkdir -p "$VAULT_PATH/02_전략"
   # 기존에 같은 이름의 실제 폴더가 있으면 먼저 백업/병합할 것
   ln -s ~/dev/CDPark1968/obsidian-vault/02_전략/키파운드리 "$VAULT_PATH/02_전략/키파운드리"
   ```
   symlink 후 Obsidian을 껐다 켜면(또는 볼트 새로고침) `02_전략/키파운드리` 폴더가 그대로 보인다.

## 갱신 (매번)
`/keyfoundry-debate` 세션이 새 요약 노트를 `obsidian-vault/02_전략/키파운드리/`에 커밋·푸시하면, 로컬에서 아래만 실행한다:
```bash
cd ~/dev/CDPark1968 && git pull
```
symlink로 연결돼 있으므로 Obsidian은 파일이 새로 생기거나 바뀐 것을 즉시 인식한다. 필요하면 이 pull을 macOS `launchd`나 cron으로 주기 실행해 자동화할 수 있다(예: 매 15분).

## 참고
- symlink 대신 폴더를 통째로 복사해도 되지만, 그러면 매번 최신 파일로 덮어써야 해서 symlink보다 번거롭다.
- 이 레포 자체를 볼트 안에 직접 clone해도 되지만(예: `<VAULT_PATH>/키파운드리-AI`), 그 경우 `.git`, `.claude` 등 Obsidian이 노트로 인식하지 않아도 되는 파일까지 볼트 트리에 노출된다. 위 symlink 방식이 더 깔끔하다.
- 사용자 로컬 환경에서만 실행 가능한 절차이며, 이 원격 세션은 이 문서를 만드는 것까지만 수행할 수 있다.
