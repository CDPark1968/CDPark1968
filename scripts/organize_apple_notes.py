#!/usr/bin/env python3
"""
Obsidian Apple Notes 카테고리 연결 스크립트
- 애플메모정리 폴더의 노트들을 카테고리로 분류
- 각 노트에 YAML frontmatter (tags, category) 추가
- 카테고리별 MOC(Map of Content) 인덱스 파일 생성
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime

# ─── 설정 ────────────────────────────────────────────────────────
VAULT_PATH = Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian_Vault"
NOTES_FOLDER = "애플메모정리"
MOC_FOLDER = "00_MOC"  # MOC 파일 저장 폴더

# ─── 카테고리별 키워드 (제목 + 내용 검색) ──────────────────────
CATEGORY_KEYWORDS = {
    "AI": [
        "ai", "인공지능", "chatgpt", "gpt", "claude", "머신러닝", "딥러닝", "llm",
        "프롬프트", "prompt", "neural", "챗봇", "생성형", "midjourney", "stable diffusion",
        "openai", "anthropic", "copilot", "gemini", "자동화"
    ],
    "Prompt": [
        "프롬프트", "prompt engineering", "지시문", "system prompt", "few-shot",
        "chain of thought", "역할극", "페르소나", "역할 부여"
    ],
    "업무": [
        "미팅", "회의", "mps", "키파운드리", "파운드리", "반도체", "wafer", "capa",
        "영업", "고객", "납품", "출장", "보고서", "전략회의", "gsm", "lta",
        "skkf", "audit", "pmic", "bcd", "fab", "공정", "수율", "wspm", "fot",
        "hynix", "하이닉스", "삼성", "tsmc", "smic"
    ],
    "재무": [
        "재무", "주식", "투자", "자산", "수익", "손익", "금융", "세금", "연금",
        "펀드", "etf", "배당", "포트폴리오", "절세", "부동산", "대출", "이자",
        "소득", "지출", "예산", "보험", "은행", "opm", "매출", "영업이익"
    ],
    "법률": [
        "법률", "계약", "소송", "법원", "변호사", "규정", "조례", "법적",
        "소장", "합의", "조정", "판결", "항소", "등기", "공증", "저작권",
        "특허", "상표", "법인"
    ],
    "골프": [
        "골프", "라운딩", "스코어", "클럽", "스윙", "퍼팅", "드라이버", "아이언",
        "버디", "파", "보기", "핸디캡", "필드", "그린", "페어웨이", "티샷",
        "캐디", "gdr", "골프장"
    ],
    "금거래소": [
        "금거래소", "금거래", "금값", "금시세", "금투자", "골드", "은시세",
        "귀금속", "한국금거래소", "순금", "금매입", "gold"
    ],
    "은퇴후": [
        "은퇴", "노후", "퇴직", "연금", "여행", "취미", "건강", "노년",
        "제2의 인생", "귀농", "귀촌", "재취업"
    ],
    "사업": [
        "사업", "창업", "비즈니스", "스타트업", "매출", "이익", "사업계획",
        "사업화", "투자유치", "vc", "엔젤", "피칭", "bm", "revenue",
        "b2b", "b2c", "마케팅", "브랜딩"
    ],
    "개인": [
        "일기", "생각", "느낌", "감정", "회고", "반성", "다짐", "목표",
        "습관", "루틴", "독서", "책", "공부", "성장", "자기계발"
    ],
    "정보": [
        "뉴스", "기사", "자료", "정보", "데이터", "통계", "분석", "리포트",
        "조사", "연구", "트렌드", "시장"
    ],
}

# 우선순위 (앞에 있을수록 먼저 매칭)
CATEGORY_PRIORITY = [
    "골프", "금거래소", "Prompt", "AI", "법률", "재무",
    "업무", "사업", "은퇴후", "개인", "정보"
]


def detect_category(title: str, content: str) -> str:
    """제목과 내용에서 카테고리를 자동 감지"""
    text = (title + " " + content).lower()

    for category in CATEGORY_PRIORITY:
        keywords = CATEGORY_KEYWORDS.get(category, [])
        for kw in keywords:
            if kw.lower() in text:
                return category

    return "정보"  # 기본값


def extract_existing_frontmatter(content: str) -> tuple[dict, str]:
    """기존 YAML frontmatter 추출"""
    if not content.startswith("---"):
        return {}, content

    end = content.find("---", 3)
    if end == -1:
        return {}, content

    frontmatter_str = content[3:end].strip()
    body = content[end + 3:].strip()

    fm = {}
    for line in frontmatter_str.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()

    return fm, body


def build_frontmatter(category: str, tags: list[str], title: str) -> str:
    """YAML frontmatter 생성"""
    tag_str = "\n".join(f"  - {t}" for t in tags)
    return f"""---
category: {category}
tags:
{tag_str}
source: apple-notes
---
"""


def process_note(filepath: Path) -> str | None:
    """노트 파일 처리 - frontmatter 추가/업데이트, 카테고리 반환"""
    try:
        text = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  ⚠️  읽기 실패: {filepath.name} — {e}")
        return None

    existing_fm, body = extract_existing_frontmatter(text)

    # 이미 처리된 경우 스킵
    if existing_fm.get("source") == "apple-notes" and "category" in existing_fm:
        return existing_fm.get("category")

    title = filepath.stem
    category = existing_fm.get("category") or detect_category(title, body[:500])

    tags = [f"애플메모/{category}", "apple-notes"]
    new_fm = build_frontmatter(category, tags, title)
    new_content = new_fm + "\n" + body

    filepath.write_text(new_content, encoding="utf-8")
    return category


def create_moc_file(moc_dir: Path, category: str, notes: list[Path]):
    """카테고리 MOC 파일 생성"""
    moc_path = moc_dir / f"MOC_{category}.md"
    lines = [
        f"# {category} 메모 모음\n",
        f"> 총 **{len(notes)}개** 노트  |  마지막 업데이트: {datetime.now().strftime('%Y-%m-%d')}\n",
        "\n---\n",
        "```dataview",
        f'TABLE 메모내용요약 AS "요약"',
        f'FROM "애플메모정리"',
        f'WHERE category = "{category}"',
        'SORT file.mtime DESC',
        "```\n",
        "---\n",
        "## 전체 목록\n",
    ]

    for note in sorted(notes, key=lambda p: p.stem):
        lines.append(f"- [[{note.stem}]]")

    moc_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅  MOC 생성: {moc_path.name} ({len(notes)}개)")


def create_master_moc(moc_dir: Path, category_counts: dict[str, int]):
    """전체 카테고리 마스터 인덱스 생성"""
    master_path = moc_dir / "MOC_애플메모_전체.md"
    lines = [
        "# 애플메모 전체 인덱스\n",
        f"> 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        "\n---\n",
        "## 카테고리별 노트 수\n",
    ]

    total = sum(category_counts.values())
    for cat, cnt in sorted(category_counts.items(), key=lambda x: -x[1]):
        pct = cnt / total * 100 if total else 0
        lines.append(f"| [[MOC_{cat}\\|{cat}]] | {cnt}개 | {pct:.1f}% |")

    lines = lines[:lines.index("## 카테고리별 노트 수\n") + 1] + [
        "| 카테고리 | 노트 수 | 비중 |",
        "|---------|--------|------|",
    ] + lines[lines.index("## 카테고리별 노트 수\n") + 1:]

    lines.append(f"\n**합계: {total}개**\n")
    master_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  ✅  마스터 MOC 생성: {master_path.name}")


def main():
    notes_dir = VAULT_PATH / NOTES_FOLDER
    moc_dir = VAULT_PATH / MOC_FOLDER

    if not notes_dir.exists():
        print(f"❌ 폴더를 찾을 수 없습니다: {notes_dir}")
        print(f"   볼트 경로를 확인하세요: {VAULT_PATH}")
        sys.exit(1)

    moc_dir.mkdir(exist_ok=True)

    md_files = list(notes_dir.rglob("*.md"))
    print(f"\n📂 대상 폴더: {notes_dir}")
    print(f"📝 총 {len(md_files)}개 노트 처리 시작...\n")

    category_notes: dict[str, list[Path]] = {cat: [] for cat in CATEGORY_KEYWORDS}
    processed = 0
    skipped = 0

    for i, filepath in enumerate(md_files, 1):
        if i % 100 == 0:
            print(f"   진행: {i}/{len(md_files)}...")

        category = process_note(filepath)
        if category:
            category_notes.setdefault(category, []).append(filepath)
            processed += 1
        else:
            skipped += 1

    print(f"\n✅ 처리 완료: {processed}개  |  스킵: {skipped}개\n")
    print("📁 MOC 파일 생성 중...")

    for category, notes in category_notes.items():
        if notes:
            create_moc_file(moc_dir, category, notes)

    category_counts = {cat: len(notes) for cat, notes in category_notes.items() if notes}
    create_master_moc(moc_dir, category_counts)

    print("\n🎉 완료! Obsidian을 재시작하거나 볼트를 새로고침하세요.")
    print(f"   MOC 파일 위치: {moc_dir}")


if __name__ == "__main__":
    main()
