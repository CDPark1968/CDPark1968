#!/usr/bin/env python3
"""
Obsidian Vault 재정리 스크립트
- 폴더 구조 정리 및 번호 중복 해소
- 루트에 흩어진 .md 파일 자동 분류 후 이동
- 카테고리별 MOC(Map of Content) 생성
- 메인 대시보드(_Home.md) 생성
- 각 노트에 YAML frontmatter + 백링크 추가
"""

import os
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime

# ─── 볼트 자동 탐색 ─────────────────────────────────────────────
def find_vault() -> Path:
    candidates = [
        Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian_Vault",
        Path("."),
        Path("Obsidian_Vault"),
    ]
    markers = ["_Templates", "_Index", "Apple Notes", "01_미팅노트"]
    for p in candidates:
        if any((p / m).exists() for m in markers):
            print(f"✅ 볼트 감지: {p.resolve()}")
            return p.resolve()
    print("❌ 볼트를 찾을 수 없습니다. pickFolder로 볼트 루트를 선택 후 재실행하세요.")
    sys.exit(1)

VAULT = find_vault()

# ─── 새 폴더 구조 정의 ──────────────────────────────────────────
NEW_STRUCTURE = {
    "00_Index":     "인덱스 & MOC",
    "01_업무":       "업무 (미팅/회의/보고)",
    "02_전략":       "전략 (키파운드리 / 반도체)",
    "03_출장":       "출장",
    "04_Market":    "Market Intelligence",
    "05_재무투자":   "재무 & 투자",
    "06_개인":       "개인 & Apple Notes",
    "07_골프":       "골프",
    "08_일간노트":   "일간 노트 (Daily Notes)",
    "_Templates":   "템플릿",
}

# 기존 폴더 → 새 폴더 매핑
FOLDER_MAP = {
    "01_미팅노트":          "01_업무/미팅노트",
    "05_회의록":            "01_업무/회의록",
    "03_업무보고":          "01_업무/업무보고",
    "03_키파운드리":        "02_전략/키파운드리",
    "04_출장":              "03_출장",
    "02_Market_Intelligence": "04_Market",
    "04_투자":              "05_재무투자",
    "Apple Notes":          "06_개인/Apple Notes",
    "애플메모정리":          "06_개인/Apple Notes",
    "_Index":               "00_Index",
    "_Templates":           "_Templates",
}

# 루트 .md 파일 분류 기준 (키워드 → 폴더)
ROOT_FILE_RULES = [
    (r"\d{4}-\d{2}-\d{2}",                   "08_일간노트"),   # 날짜 형식
    (r"회의록|meeting|미팅|conference",        "01_업무/미팅노트"),
    (r"출장|irvine|trip",                      "03_출장"),
    (r"주식|투자|ADR|hynix.*주식|전망",         "05_재무투자"),
    (r"골프|golf|라운딩",                      "07_골프"),
    (r"mps|jackary|aura|onsemi|syntiant|maxlinear|diodes", "01_업무/미팅노트"),
]

# ─── 카테고리 MOC 정의 ──────────────────────────────────────────
MOC_DEFINITIONS = {
    "MOC_전체": {
        "title": "전체 볼트 인덱스",
        "emoji": "🗂️",
        "links": list(NEW_STRUCTURE.keys()),
    },
    "MOC_업무": {
        "title": "업무 노트 모음",
        "emoji": "💼",
        "folder": "01_업무",
    },
    "MOC_전략": {
        "title": "키파운드리 전략",
        "emoji": "🎯",
        "folder": "02_전략",
    },
    "MOC_재무투자": {
        "title": "재무 & 투자",
        "emoji": "💰",
        "folder": "05_재무투자",
    },
    "MOC_개인": {
        "title": "개인 메모",
        "emoji": "🌿",
        "folder": "06_개인",
    },
    "MOC_출장": {
        "title": "출장 기록",
        "emoji": "✈️",
        "folder": "03_출장",
    },
    "MOC_골프": {
        "title": "골프",
        "emoji": "⛳",
        "folder": "07_골프",
    },
}


# ─── 유틸리티 함수 ──────────────────────────────────────────────
def safe_move(src: Path, dst: Path):
    """파일 안전 이동 (중복 시 접미사 붙임)"""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        stem, suffix = dst.stem, dst.suffix
        for i in range(1, 100):
            candidate = dst.parent / f"{stem}_{i}{suffix}"
            if not candidate.exists():
                dst = candidate
                break
    shutil.move(str(src), str(dst))
    return dst


def classify_root_file(filepath: Path) -> str:
    """루트 .md 파일의 목표 폴더 결정"""
    name_lower = filepath.stem.lower()
    for pattern, folder in ROOT_FILE_RULES:
        if re.search(pattern, name_lower, re.IGNORECASE):
            return folder
    return "01_업무/미팅노트"  # 기본값


def add_frontmatter(filepath: Path, category: str, tags: list[str]):
    """YAML frontmatter 추가 (없는 경우에만)"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return

    if content.startswith("---"):
        return  # 이미 있음

    tags_str = "\n".join(f"  - {t}" for t in tags)
    fm = f"---\ncategory: {category}\ntags:\n{tags_str}\n---\n\n"
    filepath.write_text(fm + content, encoding="utf-8")


def list_md_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted(folder.rglob("*.md"))


# ─── 메인 대시보드 생성 ─────────────────────────────────────────
def create_home_dashboard():
    home = VAULT / "_Home.md"
    now = datetime.now().strftime("%Y-%m-%d")
    content = f"""---
tags:
  - dashboard
  - index
---

# 🏠 박찬동의 Obsidian 대시보드

> 마지막 업데이트: {now}

---

## 📂 카테고리

| 폴더 | 설명 | MOC |
|------|------|-----|
| [[00_Index/MOC_전체\\|00 Index]] | 전체 인덱스 | [[00_Index/MOC_전체]] |
| [[01_업무\\|01 업무]] | 미팅노트 · 회의록 · 업무보고 | [[00_Index/MOC_업무]] |
| [[02_전략\\|02 전략]] | 키파운드리 · 반도체 전략 | [[00_Index/MOC_전략]] |
| [[03_출장\\|03 출장]] | 출장 기록 | [[00_Index/MOC_출장]] |
| [[04_Market\\|04 Market]] | Market Intelligence | |
| [[05_재무투자\\|05 재무/투자]] | 주식 · IRP · 금거래소 | [[00_Index/MOC_재무투자]] |
| [[06_개인\\|06 개인]] | Apple Notes · 개인 메모 | [[00_Index/MOC_개인]] |
| [[07_골프\\|07 골프]] | 라운딩 · 골프 여행 | [[00_Index/MOC_골프]] |
| [[08_일간노트\\|08 일간노트]] | Daily Notes | |

---

## 🔗 빠른 접근

- [[00_Index/MOC_전체|📋 전체 노트 목록]]
- [[00_Index/MOC_업무|💼 최근 업무 노트]]
- [[00_Index/MOC_재무투자|💰 투자 현황]]
- [[00_Index/MOC_전략|🎯 MPS 전략]]

---

## 📅 최근 일간노트

```dataview
LIST
FROM "08_일간노트"
SORT file.name DESC
LIMIT 7
```

## 💼 최근 업무 노트

```dataview
TABLE file.mtime AS "수정일"
FROM "01_업무"
SORT file.mtime DESC
LIMIT 10
```
"""
    home.write_text(content, encoding="utf-8")
    print("  ✅ _Home.md 생성 완료")


# ─── MOC 파일 생성 ──────────────────────────────────────────────
def create_moc(name: str, definition: dict):
    moc_path = VAULT / "00_Index" / f"{name}.md"
    moc_path.parent.mkdir(parents=True, exist_ok=True)

    emoji = definition.get("emoji", "📁")
    title = definition.get("title", name)
    folder = definition.get("folder", "")
    now = datetime.now().strftime("%Y-%m-%d")

    if name == "MOC_전체":
        links_section = "\n".join(
            f"- [[00_Index/MOC_{k.replace('00_Index/', '')}|{v}]]"
            for k, v in NEW_STRUCTURE.items()
            if not k.startswith("_")
        )
        content = f"""---
tags:
  - moc
  - index
---

# {emoji} {title}

> 마지막 업데이트: {now}

---

## 카테고리 목록

{links_section}

---

## 전체 노트 통계

```dataview
TABLE length(rows) AS "노트 수"
GROUP BY category
```
"""
    else:
        dataview_from = f'FROM "{folder}"' if folder else ""
        content = f"""---
tags:
  - moc
  - {name.lower()}
---

# {emoji} {title}

> 마지막 업데이트: {now}  |  [[_Home|🏠 홈으로]]

---

## 노트 목록

```dataview
TABLE file.mtime AS "수정일", category AS "카테고리"
{dataview_from}
SORT file.mtime DESC
```

---

## 수동 링크 목록

"""
        # 폴더 내 파일 목록도 추가
        if folder:
            target = VAULT / folder
            files = list_md_files(target)
            for f in sorted(files, key=lambda x: x.name):
                rel = f.relative_to(VAULT)
                content += f"- [[{rel.with_suffix('')}|{f.stem}]]\n"

    moc_path.write_text(content, encoding="utf-8")
    print(f"  ✅ {moc_path.name} 생성")


# ─── 폴더 구조 재정리 ────────────────────────────────────────────
def reorganize_folders():
    print("\n📁 폴더 구조 재정리 중...")
    moved = 0
    for old_name, new_rel in FOLDER_MAP.items():
        old_path = VAULT / old_name
        if not old_path.exists():
            continue
        new_path = VAULT / new_rel
        if old_path.resolve() == new_path.resolve():
            continue
        if new_path.exists():
            # 기존 폴더가 있으면 파일만 이동
            for item in old_path.iterdir():
                dst = new_path / item.name
                safe_move(item, dst)
                moved += 1
            old_path.rmdir() if not any(old_path.iterdir()) else None
        else:
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(old_path), str(new_path))
            moved += 1
        print(f"   {old_name} → {new_rel}")
    print(f"   총 {moved}개 항목 이동")


def move_root_md_files():
    print("\n📄 루트 .md 파일 분류 중...")
    moved = 0
    skip = {"_Home.md", "CLAUDE.md", "Claude.md"}
    for f in VAULT.glob("*.md"):
        if f.name in skip or f.name.startswith("MOC_"):
            continue
        target_folder = classify_root_file(f)
        dst = VAULT / target_folder / f.name
        result = safe_move(f, dst)
        print(f"   {f.name} → {target_folder}/")
        moved += 1
    print(f"   총 {moved}개 파일 이동")


def create_new_folders():
    print("\n📂 새 폴더 생성 중...")
    for folder in NEW_STRUCTURE:
        (VAULT / folder).mkdir(parents=True, exist_ok=True)
    print("   완료")


def add_frontmatter_to_all():
    print("\n🏷️  frontmatter 태깅 중...")
    folder_category_map = {
        "01_업무": "업무",
        "02_전략": "전략",
        "03_출장": "출장",
        "04_Market": "Market",
        "05_재무투자": "재무투자",
        "06_개인": "개인",
        "07_골프": "골프",
        "08_일간노트": "일간노트",
    }
    count = 0
    for folder, category in folder_category_map.items():
        for md in list_md_files(VAULT / folder):
            # Apple Notes는 기존 스크립트가 처리했을 수 있으므로 스킵
            if "Apple Notes" in str(md):
                continue
            add_frontmatter(md, category, [category, f"vault/{folder}"])
            count += 1
    print(f"   {count}개 파일 frontmatter 추가")


# ─── 메인 ───────────────────────────────────────────────────────
def main():
    print(f"\n🔧 Obsidian Vault 재정리 시작")
    print(f"   대상: {VAULT}\n")

    # 1. 새 폴더 생성
    create_new_folders()

    # 2. 기존 폴더 재배치
    reorganize_folders()

    # 3. 루트 .md 파일 이동
    move_root_md_files()

    # 4. frontmatter 추가
    add_frontmatter_to_all()

    # 5. 대시보드 생성
    print("\n📊 대시보드 및 MOC 생성 중...")
    create_home_dashboard()

    # 6. MOC 파일 생성
    (VAULT / "00_Index").mkdir(exist_ok=True)
    for name, definition in MOC_DEFINITIONS.items():
        create_moc(name, definition)

    print("\n" + "="*50)
    print("🎉 재정리 완료!")
    print(f"\n최종 구조:")
    for folder, desc in NEW_STRUCTURE.items():
        count = len(list_md_files(VAULT / folder))
        print(f"   {folder}/  ({count}개 노트) — {desc}")
    print(f"\n👉 Obsidian에서 _Home.md 를 시작 페이지로 설정하세요.")
    print("   설정 → 옵션 → 파일 및 링크 → 시작 시 열 파일 → _Home.md")

if __name__ == "__main__":
    main()
