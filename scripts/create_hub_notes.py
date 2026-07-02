#!/usr/bin/env python3
"""
주요 허브 노트 생성 스크립트
- MPS, 키파운드리, 금거래소 등 핵심 주제 노트 생성
- 관련 노트들의 백링크 허브 역할
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

def find_vault(vault_arg: str = None) -> Path:
    # 1. 명령줄 인자
    if vault_arg:
        p = Path(vault_arg)
        if p.exists():
            print(f"✅ 볼트 (인자): {p.resolve()}")
            return p.resolve()
        print(f"❌ 인자 경로 없음: {vault_arg}")

    # 2. 환경변수
    env_path = os.environ.get("VAULT_PATH")
    if env_path:
        p = Path(env_path)
        if p.exists():
            print(f"✅ 볼트 (환경변수): {p.resolve()}")
            return p.resolve()

    # 3. 자동 탐색
    markers = ["00_Index", "_Templates", "01_업무", "Apple Notes", "06_개인"]
    candidates = [
        Path.home() / "Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian_Vault",
        Path("."),
        Path("Obsidian_Vault"),
    ]
    for p in candidates:
        if any((p / m).exists() for m in markers):
            print(f"✅ 볼트: {p.resolve()}")
            return p.resolve()

    print("❌ 볼트를 찾을 수 없습니다.")
    print(f"   현재 위치: {Path('.').resolve()}")
    print(f"   현재 폴더 내용: {[x.name for x in Path('.').iterdir() if x.is_dir()][:10]}")
    print()
    print("   a-Shell 사용법:")
    print("   pickFolder  ← Obsidian_Vault 선택")
    print("   python3 ~/cdpark1968/scripts/create_hub_notes.py")
    sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("--vault", help="볼트 경로 직접 지정")
args, _ = parser.parse_known_args()

VAULT = find_vault(args.vault)
TODAY = datetime.now().strftime("%Y-%m-%d")

HUB_NOTES = {

# ────────────────────────────────────────────────────────────────
"02_전략/MPS.md": f"""---
category: 전략
tags:
  - 전략/MPS
  - 고객
  - 허브노트
created: {TODAY}
---

# MPS (Monolithic Power Systems)

> **핵심 고객** | 반도체 팹리스 | 본사: 미국
> 관계 요약: SKKF 최대 고객이자 최대 리스크 — 관계 재정립 필요

---

## 기본 현황

| 항목 | 내용 |
|------|------|
| 매출 규모 | ~2.8B$ ('25) → 3.5B$ ('26 예상) |
| SKKF 공급 | 8인치 27K WSPM (전체 92K 중) |
| 2026 요구 | FOT 기준 **28K WSPM** |
| 2027 요구 | **40~45K WSPM** |
| 필요 투자 | 70~80M USD (증설) |
| 주요 End Market | AI Server, Automotive, Robotics, Storage |

---

## 공급망 현황

- 8인치 TTL 92K: [[SMIC]] 45K / [[SKKF]] 27K / [[Vishay]] 7K / [[HHG]] 3K
- 12인치 TTL 49K: [[HHG]] 35K / [[SMIC]] 5K / [[TSMC]] 2K
- 주요 고객사: NV 500M / Intel 300M / Samsung 230M / AMD 170M / Google 100M / [[SK하이닉스]] 80M

---

## 주요 이슈

### 🔴 이슈 1. 캐파 갭
- 2026 요구 28K vs 현 공급 ~18K → **+10K 갭**
- 2027년 40~45K 요구로 갭 확대
- [[SystemIC]] (중국) 오버플로우 제안 → SK그룹 규제로 **불가**

### 🔴 이슈 2. 팹 비효율
- [[MPS]] [[FOT]] 16K → **[[6-metal]] 공정 → 팹 비효율 발생**
- 60% 수준 운영 중 → 추가 감소 필요
- [[OPM]] 15% 목표 달성 불가

### 🟠 이슈 3. 협상 전략
- MPS의 전술: 공급 병목 → 압박 → [[LTA]] 확약 유도
- **2028년부터 [[16GF]] 감소 예정** (12인치 전환, 2nd source)
- 지금이 관계 재정립 유일한 기회

---

## 대응 전략 (2트랙)

### Track 1. 조건부 증설 (단기)
- 증설 규모: +10~15K [[WSPM]]
- **조건**: MPS [[Consignment]] 투자 + 가격 인상 + [[LTA]] 의무조항
- 기한: 2026.07.06 제안서

### Track 2. Plan-B (중장기)
- 상방 고정: MPS 30~35K (이 이상 증가 불허)
- 하방 준비:
  - 2028: +5K (Automotive 고객)
  - 2029: +5K (AI DC / Humanoid)

---

## 핵심 연락처

| 이름 | 역할 |
|------|------|
| [[Deming]] Xiao | 경영진 |
| [[Zachary]] Yao | Sales |
| [[Derek]] | 경영진 (Jackary 미팅) |
| 백채욱 상무 | MPS Korea Sales |
| 안경은 상무 | QA |

---

## 관련 노트

- [[01_업무/미팅노트/MPS, Jackary Conference 회의록, 2026-06-22]]
- [[02_전략/키파운드리/키파운드리 전략]]
- [[00_Index/MOC_전략]]

---

## Action Items

- [ ] 2026.07.06 — 증설 제안서 제출 (Sales + Finance)
- [ ] 2026.07.08 — 고객 대면 미팅 일정 조율
- [ ] 이사회 증설 투자 안건 상정 (70~80M USD)
- [ ] [[Pull-in]] 프리미엄 정책 수립
""",

# ────────────────────────────────────────────────────────────────
"02_전략/키파운드리.md": f"""---
category: 전략
tags:
  - 전략/키파운드리
  - 허브노트
  - 회사
created: {TODAY}
---

# 키파운드리 (KeyFoundry / SKKF)

> 8인치 파운드리 | 현 소속사 | 목표 [[OPM]] 15%

---

## 캐파 현황

| 구분 | 수량 |
|------|------|
| 총 캐파 | ~90K WSPM |
| [[MPS]] | 27K (30%) |
| [[Vishay]] | 10K |
| [[LXS]] | 15K |
| Others | ~18K |
| 목표 캐파 ('28) | 105K |

---

## 고객 포트폴리오 전략

- **상방**: [[MPS]] 30~35K 고정 (Consignment/투자 조건부)
- **성장**: Automotive ([[Elmos]], 현대모비스) / AI DC / Humanoid
- **2028 Plan-B**: MPS 16GF 감소분 → 신규 고객으로 대체

---

## 기술 강점

- HV (High Voltage) 공정
- Trench Isolation (23μm)
- [[BCDN]], 120V [[BCD]]+Flash
- Automotive: 현대차 지정 파운드리 (말레이시아 배제)

---

## 관련 노트

- [[02_전략/MPS]]
- [[00_Index/MOC_전략]]
""",

# ────────────────────────────────────────────────────────────────
"05_재무투자/금거래소.md": f"""---
category: 재무투자
tags:
  - 재무투자/금거래소
  - 사업
  - 허브노트
  - 은퇴
created: {TODAY}
---

# 금거래소 (한국금거래소 대리점)

> 목적: 은퇴 후 **Cash Flow 창출**
> 운영: 아내 (주하) 중심 운영

---

## 사업 개요

| 항목 | 내용 |
|------|------|
| 형태 | 한국금거래소 대리점 |
| 지역 | 위례 (또는 하남) |
| 초기 투자 | ~10억 (현물 8억 + 권리금 1.5억) |
| 임대료 | 3,000/176만 |
| 대리점비 | 월 300만 |
| 대출 이자 | 월 220만 (5억 기준) |
| 목표 Cash Flow | 월 1,500만+ |

---

## 장점

- 재고 부담 없음 (금 현물 → 망해도 본전)
- 전문지식 불필요
- 방문객 구매 전환율 높음
- 구/시 단위 독점 권리

---

## 리스크

- 경쟁 심화: 삼성금거래소 등 후발주자
- 금값 상승 시 손님 감소
- [[은퇴]] 후 직접 운영 → **시스템화 필수**

---

## 운영 원칙

1. 아내를 대표로 세우되 **진짜 대표로 존중**
2. 내가 매일 나가야 돌아가는 구조는 금지
3. 직원 + 보안 + 세무 + 고객DB 시스템 먼저

---

## 성장 방향

- 2년 후: 유동인구 많은 곳으로 이전 (미사/하남 스타필드)
- 금방금방 앱 활용 확대
- 블로그/홈페이지 운영

---

## 관련 노트

- [[05_재무투자/주식 투자 방향]]
- [[00_Index/MOC_재무투자]]
""",

# ────────────────────────────────────────────────────────────────
"05_재무투자/투자원칙.md": f"""---
category: 재무투자
tags:
  - 재무투자/원칙
  - 허브노트
  - 투자
created: {TODAY}
---

# 투자 원칙

> 목표: 20억 / 15년
> 원칙: **현금흐름 우선 + 복잡성 최소화**

---

## 포트폴리오 구조

| 자산 | 내용 | 목적 |
|------|------|------|
| [[IRP]] | Tiger S&P500 40% + 채권 30% + 배당 30% | 장기 성장 |
| 직접투자 | [[NVDA]], [[MSFT]], [[SMR]], [[IONQ]] | 성장 |
| 배당 | [[JEPQ]], IRM | 월 현금흐름 |
| 부동산 | 잠실 트리지움, 용인 아파트 | 안정 기반 |
| [[금거래소]] | 현물 보유 | 사업 + 헷지 |
| [[ETF]] | [[S&P500]], 금 ETF | 분산 |

---

## 투자 5원칙 (75세의 나)

1. **복잡한 자산을 줄여라** — 노후엔 스트레스
2. **현금흐름을 만들어라** — 매월 들어오는 돈
3. **세금은 미리 설계해라** — 늦으면 비싸다
4. **배우자 보호 구조 먼저** — 아내 혼자도 가능하게
5. **자녀에게 너무 많이 주지 마라** — 자립심

---

## 월 납입 루틴

- [[IRP]]: 월 58만 (연 700만)
- [[JEPQ]]: 월 50만
- IRM: 월 25만
- [[NVDA]] 1주 + [[MSFT]] 1주 + [[SMR]] 1주 + [[IONQ]] 1주

---

## 관련 노트

- [[05_재무투자/금거래소]]
- [[00_Index/MOC_재무투자]]
""",

}

def main():
    print(f"\n📝 허브 노트 생성 중...\n")
    created = 0
    for rel_path, content in HUB_NOTES.items():
        filepath = VAULT / rel_path
        filepath.parent.mkdir(parents=True, exist_ok=True)
        if filepath.exists():
            print(f"  ⚠️  이미 존재 (스킵): {rel_path}")
            continue
        filepath.write_text(content, encoding="utf-8")
        print(f"  ✅ 생성: {rel_path}")
        created += 1

    print(f"\n🎉 완료! {created}개 허브 노트 생성됨")
    print(f"\n다음 단계:")
    print(f"  1. Obsidian 새로고침 (Cmd+R)")
    print(f"  2. '02_전략/MPS.md' 열기")
    print(f"  3. 우클릭 → '로컬 그래프 열기'")
    print(f"  4. MPS와 연결된 모든 노트가 그래프로 표시됩니다")

if __name__ == "__main__":
    main()
