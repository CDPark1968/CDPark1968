# Obsidian 로컬 동기화 설정 (git 브릿지)

Obsidian 볼트는 로컬 경로 `~/Documents/Obsidian/키파운드리`에 있다. 이 경로와 Obsidian 앱 모두 이 원격 세션에서 접근 가능한 API/MCP가 없으므로, **이 git 레포를 로컬 볼트와 파일 시스템 레벨에서 연결**해서 세션이 커밋·푸시할 때마다 `git pull` 한 번으로 Obsidian에 반영되게 한다.

볼트 자체가 이미 "키파운드리"이므로, 레포의 `obsidian-vault/02_전략/키파운드리` 폴더를 볼트 루트의 `02_전략`으로 symlink한다(폴더명 중복을 피하기 위해 한 단계 아래에 연결).

## 설정 (최초 1회, 터미널에서 그대로 실행)

1. 이 레포를 로컬 아무 위치에 clone한다 (볼트 밖 — 예: `~/dev/CDPark1968`):
   ```bash
   git clone https://github.com/CDPark1968/CDPark1968.git ~/dev/CDPark1968
   cd ~/dev/CDPark1968
   git checkout claude/keyfoundry-ai-agents-vzfyfp
   ```

2. 레포 안의 `obsidian-vault/02_전략/키파운드리` 폴더를 실제 볼트의 `02_전략` 자리에 symlink로 연결한다:
   ```bash
   VAULT_PATH="$HOME/Documents/Obsidian/키파운드리"
   # 볼트 안에 이미 02_전략 폴더(실제 폴더)가 있다면 먼저 이름을 바꾸거나 내용을 백업할 것
   ln -s ~/dev/CDPark1968/obsidian-vault/02_전략/키파운드리 "$VAULT_PATH/02_전략"
   ```
   symlink 후 Obsidian을 껐다 켜면(또는 볼트 새로고침) 볼트 루트에 `02_전략` 폴더가 그대로 보인다.

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
