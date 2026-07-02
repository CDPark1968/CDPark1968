#!/usr/bin/env python3
"""
Obsidian Wikilink 자동 처리 스크립트
- 주요 단어를 [[단어]] 형태로 자동 변환
- YAML frontmatter, 코드블록, 기존 링크 내부는 건드리지 않음
- 파일당 각 단어의 첫 번째 등장만 링크 처리 (과도한 링크 방지)
"""

import re
import sys
from pathlib import Path

# ─── 볼트 자동 탐색 ─────────────────────────────────────────────
def find_vault() -> Path:
    candidates = [
        Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian_Vault",
        Path("."),
        Path("Obsidian_Vault"),
    ]
    for p in candidates:
        if any((p / m).exists() for m in ["00_Index", "_Templates", "01_업무", "Apple Notes"]):
            print(f"✅ 볼트: {p.resolve()}")
            return p.resolve()
    print("❌ 볼트를 찾을 수 없습니다. pickFolder 후 재실행하세요.")
    sys.exit(1)

VAULT = find_vault()

# ─── 주요 링크 단어 정의 ─────────────────────────────────────────
# (표시 텍스트, 링크 대상) 또는 문자열(동일하게 사용)
# 앞에 있을수록 우선순위 높음

WIKILINK_TERMS = [
    # ── 회사 / 고객 ──────────────────────────────────────────────
    "MPS",
    "키파운드리",
    "SKKF",
    "SK하이닉스",
    "하이닉스",
    "TSMC",
    "SMIC",
    "SystemIC",
    "DBH",
    "HHG",
    "Vishay",
    "Elmos",
    "Onsemi",
    "Maxlinear",
    "Skyworks",
    "Renesas",
    "LXS",
    "Unitree",
    "Magnachip",
    "PSMC",

    # ── 사람 ────────────────────────────────────────────────────
    "Jackary",
    "Deming",
    "Zachary",
    "Derek",

    # ── 기술 / 공정 용어 ─────────────────────────────────────────
    "PMIC",
    "BCD",
    "DCDC",
    "SiC",
    "16GF",
    "6-metal",
    "8인치",
    "12인치",
    "WSPM",
    "FOT",
    "COTT",
    "DPL",
    "KrF",
    "DTI",
    "WLR",
    "PCN",
    "AECQ-100",
    "Trench",
    "BCDN",

    # ── 비즈니스 / 전략 용어 ──────────────────────────────────────
    "LTA",
    "Capa",
    "캐파",
    "OPM",
    "Consignment",
    "Pull-in",
    "2nd source",
    "Plan-B",
    "Audit",
    "GSM",
    "QBR",
    "SCM",
    "FAE",
    "Allocation",

    # ── 투자 / 재무 ──────────────────────────────────────────────
    "IRP",
    "ISA",
    "JEPQ",
    "NVDA",
    "MSFT",
    "SMR",
    "IONQ",
    "S&P500",
    "ETF",
    "IRM",
    "퇴직금",
    "배당",
    "금거래소",

    # ── 장소 / 자산 ──────────────────────────────────────────────
    "잠실",
    "용인",
    "분당",
    "위례",
    "청주",

    # ── 개인 / 삶 ────────────────────────────────────────────────
    "은퇴",
    "골프",
    "당뇨",
    "비전",
]

# ─── 처리 제외 폴더 ─────────────────────────────────────────────
SKIP_FOLDERS = {"00_Index", "_Templates"}

# ─── 핵심 함수 ──────────────────────────────────────────────────

def split_protected_regions(text: str):
    """
    텍스트를 '처리 가능 구간'과 '보호 구간'으로 분리.
    보호 구간: YAML frontmatter, 코드블록(```), 기존 [[링크]], ![[이미지]]
    반환: [(is_protected, chunk), ...]
    """
    # 패턴: YAML frontmatter | 코드블록 | 기존 wikilink | 이미지 링크 | 인라인코드
    protected_pattern = re.compile(
        r'(^---[\s\S]*?^---\n)'      # YAML frontmatter
        r'|(```[\s\S]*?```)'          # 코드블록
        r'|(!?\[\[.*?\]\])'           # 기존 wikilink / 이미지
        r'|(`[^`]+`)',                # 인라인 코드
        re.MULTILINE
    )

    segments = []
    last = 0
    for m in protected_pattern.finditer(text):
        if m.start() > last:
            segments.append((False, text[last:m.start()]))
        segments.append((True, m.group()))
        last = m.end()
    if last < len(text):
        segments.append((False, text[last:]))
    return segments


def add_wikilinks_to_text(text: str, terms: list[str]) -> tuple[str, int]:
    """텍스트에 wikilink 추가. 파일당 각 단어 첫 등장만 처리."""
    segments = split_protected_regions(text)
    linked = set()  # 이미 링크된 단어 추적
    total_count = 0

    result = []
    for is_protected, chunk in segments:
        if is_protected:
            result.append(chunk)
            continue

        for term in terms:
            if term in linked:
                continue
            # 단어 경계: 한국어는 경계 없이, 영문은 단어 경계 적용
            if re.search(r'[A-Za-z]', term):
                pattern = re.compile(r'(?<!\[)(?<!\w)' + re.escape(term) + r'(?!\w)(?!\])')
            else:
                pattern = re.compile(r'(?<!\[)' + re.escape(term) + r'(?!\])')

            if pattern.search(chunk):
                chunk = pattern.sub(f'[[{term}]]', chunk, count=1)
                linked.add(term)
                total_count += 1

        result.append(chunk)

    return "".join(result), total_count


def process_file(filepath: Path) -> int:
    """단일 파일 처리. 변경된 링크 수 반환."""
    try:
        original = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"  ⚠️  읽기 실패: {filepath.name} — {e}")
        return 0

    updated, count = add_wikilinks_to_text(original, WIKILINK_TERMS)

    if count > 0 and updated != original:
        filepath.write_text(updated, encoding="utf-8")

    return count


# ─── 메인 ───────────────────────────────────────────────────────
def main():
    print(f"\n🔗 Wikilink 자동 처리 시작\n")

    all_md = [
        f for f in VAULT.rglob("*.md")
        if not any(part in SKIP_FOLDERS for part in f.parts)
        and "Apple Notes" not in str(f)  # Apple Notes는 너무 많아서 별도 처리
    ]

    print(f"📝 대상 파일: {len(all_md)}개 (Apple Notes 제외)\n")

    total_links = 0
    modified_files = 0

    for i, filepath in enumerate(all_md, 1):
        count = process_file(filepath)
        if count > 0:
            rel = filepath.relative_to(VAULT)
            print(f"  ✅ {rel}  (+{count}개 링크)")
            total_links += count
            modified_files += 1

    print(f"\n{'='*50}")
    print(f"🎉 완료!")
    print(f"   수정된 파일: {modified_files}개")
    print(f"   추가된 링크: {total_links}개")
    print(f"\nObsidian에서 Cmd+R 로 새로고침하세요.")
    print(f"그래프 보기(Cmd+G)에서 연결 관계를 확인할 수 있습니다.")

    # Apple Notes 처리 여부 확인
    apple_notes = list((VAULT / "06_개인" / "Apple Notes").rglob("*.md"))
    if apple_notes:
        print(f"\n💡 Apple Notes({len(apple_notes)}개)도 처리하려면:")
        print(f"   스크립트에서 'Apple Notes' 제외 조건을 삭제 후 재실행")
        print(f"   (파일이 많아 시간이 걸릴 수 있습니다)")


if __name__ == "__main__":
    main()
