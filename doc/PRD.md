# PRD — 확장 가능한 Python 길이 단위 변환 학습 시스템

| 항목 | 내용 |
|------|------|
| **저장소** | `c:\DEV\2-4.unit_converter` |
| **문서 버전** | Phase 4 기준 (Epic / User Stories US-01~07 / Gherkin 8 Scenarios) |
| **원천 요구** | [README.md](../README.md), 레거시 `main/UnitConverter.py` |
| **상태** | 승인 전 초안 |

---

## 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 0.1 | 2026-05-20 | Phase 4 산출물 통합 초안 |

---

# 1. 프로젝트 개요

## 1.1 한 줄 목적문 (What / Who / Why)

| | |
|---|---|
| **What** | meter 기준 길이 단위 변환 CLI를 **계약·pytest·Gherkin·BCE 레이어**로 검증 가능하게 만드는 학습용 시스템 |
| **Who** | Python 3.11+ · TDD · 클린 아키텍처를 학습하는 실습자(생성형 AI 6시간 과정) |
| **Why** | 레거시 단일 스크립트에서 **계약 고정 → 테스트 선행 → boundary/control/entity 분리** 습관을 얻기 위해 (환산 알고리즘 숙달이 주목적이 아님) |

## 1.2 배경 및 문제 정의 (관찰 관점)

저장소에는 `단위:값` 한 줄 입력으로 meter·feet·yard를 stdout에 나열하는 변환 스크립트가 있다. 비율은 분기문에 고정되어 있고, README가 요구하는 OCP/SRP·음수 검증·설정 외부화·동적 등록·다중 출력 포맷·계약 테스트는 아직 충족되지 않았다. 실습자는 AI로 빠르게 “돌아가는 코드”를 만들 수 있으나, **무엇이 항상 참인지(불변식·error code·출력 형식)** 가 문서·테스트로 고정되지 않으면 리팩터·확장 시 회귀를 감지할 수 없다.

## 1.3 목표 (측정 가능)

| ID | 목표 | 측정 방법 | 통과 기준 |
|----|------|-----------|-----------|
| **G-01** | Domain 환산·등록 불변식 충족 | `pytest tests/entity/` | 실패 0건; INV-D TC pass |
| **G-02** | 계약 표면(입력·stderr) 고정 | Boundary TC + Gherkin 8 scenarios | error code·message regex·exit 100% 일치; 8/8 pass |
| **G-03** | README 기본 변환 재현 | CLI `meter:2.5`, format=table | stdout에 `2.5 meter = 8.2 feet`, `2.5 meter = 2.7 yard`; 줄 수=등록 단위 수 |
| **G-04** | 레이어·커버리지 게이트 | `pytest-cov` | entity line ≥95%, boundary ≥85%, data ≥90%, control ≥90%, overall ≥85% |
| **G-05** | 확장 시 Engine 불변(OCP) | cubit 등록 후 API diff | ConversionEngine 공개 API 변경 0건; feet↔yard 직접 비율 0건 |

## 1.4 비목표 (Non-Goal)

| ID | 비목표 | 경계 |
|----|--------|------|
| **NG-01** | 제품화·다채널 UI | GUI, 웹, REST, 모바일, 다국어 UI — CLI만 in-scope |
| **NG-02** | 도메인 확장 | 질량·온도·통화 등 길이 외 quantity |
| **NG-03** | 운영·배포 체계 | CI 정의, SLA, 계정·감사, 국가 표준 실시간 동기화 |

**인수 정의:** §1.3 G-01~G-05를 리뷰어가 재현 가능한 명령으로 확인하는 것 (상용 출시 아님).

---

# 2. 사용자 및 이해관계자

## 2.1 타깃 사용자 (페르소나)

| 항목 | 내용 |
|------|------|
| **이름** | 지훈 (가명) |
| **역할** | Python·pytest·클린 아키텍처 학습자 |
| **목표** | RED→GREEN→REFACTOR, US-01~07 AC·Gherkin 8 pass |
| **제약** | 6시간 Activities; AI 가속 허용, **계약·assert 완화 금지** |

### 이해관계자

| 이해관계자 | 역할 |
|------------|------|
| 강사·리뷰어 | G-01~G-05, NEG-01, 표현 계약 통과/불합격 |
| 생성형 AI | 구현 초안; error code·비율·테스트 기대값 변경 거부 |
| README | meter/feet/yard·추가 3요구의 비즈니스 상한 |

## 2.2 주요 사용 시나리오 (Phase 4 Journey)

| 시나리오 | Journey | 통과 신호 |
|----------|---------|-----------|
| **A** 계약→Domain GREEN | Awareness→Action | G-01; feet-yard 직접 상수 0 |
| **B** Boundary·README 데모 | Entry→Validation | G-02, G-03; Gherkin #1~#5 |
| **C** 확장·회귀·인수 | Action→Outcome | G-04, G-05; Gherkin 8/8; US-04~06 |

---

# 3. 기능 요구사항

## 3.0 기능·Story 추적

| 기능 ID | 기능명 | 우선순위 | Story |
|---------|--------|----------|-------|
| F-01 | 변환 (CONVERT) | 필수 | US-03 |
| F-02 | 입력 검증 | 필수 | US-01 |
| F-03 | Registry·환산 (OCP) | 필수 | US-02 |
| F-04 | table 출력·표현 계약 | 필수 | US-04 |
| F-05 | 에러 표면화 | 필수 | US-01 |
| F-06 | JSON 설정 로드 | 권장 | US-05 |
| F-07 | 동적 등록 (REGISTER) | 권장 | US-06 |
| F-08 | json/csv 출력 | 권장 | US-04 |
| F-09 | YAML 설정 | 선택 | US-05 |
| F-10 | 등록 영속 save | 선택 | US-06 |
| F-11 | TDD·레이어 게이트 | 필수 | US-07 |

## 3.1 우선순위 요약

### 필수 (MUST)

F-01, F-02, F-03, F-04, F-05, F-11

### 권장 (SHOULD)

F-06, F-07, F-08 (README 추가 요구 3항)

### 선택 (MAY)

F-09, F-10

## 3.2 기능별 입·출력 계약 (문자열)

### F-01 — CONVERT

| 항목 | 계약 |
|------|------|
| 입력 | `{unit_id}:{amount_text}` |
| `unit_id` | `[a-z][a-z0-9_]{0,31}` |
| 성공 exit | `0` |
| stdout (table) | 등록 단위마다 `{source_amount} {source_unit} = {target_amount} {target_unit}` |
| 환산 | `target = source × MetersPerUnit(source) ÷ MetersPerUnit(target)` |

### F-02 — 입력 검증

**정책 NEG-01:** `amount >= 0` 유한실수; `< 0` → `NEGATIVE_VALUE`; NaN/Inf → `NON_FINITE_VALUE`

| 조건 | code | exit | message 패턴 |
|------|------|------|----------------|
| 257자 이상 | `INPUT_TOO_LONG` | 1 | `Input exceeds 256 characters` |
| `:` 없음 | `MALFORMED_INPUT` | 1 | `Invalid format. Use unit:value (ex: meter:2.5)` |
| 비숫자 (`2.5.3`) | `NON_NUMERIC` | 1 | `Invalid number: {amount_text}` |
| 음수 | `NEGATIVE_VALUE` | 1 | `Value must be non-negative: {amount_text}` |
| non-finite | `NON_FINITE_VALUE` | 1 | `Value must be finite` |
| unit 문법 위반 | `INVALID_UNIT_ID` | 1 | `Invalid unit id: {unit_id}` |
| 미등록 unit | `UNKNOWN_UNIT` | 1 | `Unknown unit: {unit_id}` |

실패 시 stdout 변환 줄 **0줄**.

### F-03 — Registry·환산

| 항목 | 값 |
|------|-----|
| Background | meter=1.0, feet=3.28084, yard=1.09361 |
| 기준 | `meter` |
| 금지 | feet↔yard 직접 상수 |
| 중복 등록 | `DUPLICATE_UNIT` |
| `convert_all` 행 수 | = Registry 등록 수 |

### F-04 — table·표현 계약

- 모든 줄 LHS = **사용자 입력** amount·unit (변환된 source 금지)
- target (table): 소수 **1자리** half-up
- 예: `meter:2.5` → `2.5 meter = 8.2 feet`, `2.5 meter = 2.7 yard`

### F-05 — stderr·exit

| 상황 | exit |
|------|------|
| 입력·변환 실패 | 1 |
| 설정·기동 실패 | 2 |

stderr에 `code` = F-02 표 문자열; `message` = 패턴 전체 일치.

### F-06 — 설정 로드

- 파일: `config/units.json` (권장)
- `schema_version: 1`, `base_unit: "meter"`, `units[{id, meters_per_unit}]`
- 실패: `SCHEMA_INVALID`, `FILE_NOT_FOUND`, `PARSE_ERROR`, `CONFIG_LOAD_FAILED`

### F-07 — REGISTER

| 항목 | 계약 |
|------|------|
| 입력 | `register:{new_unit}={ratio}:{ref_unit}` |
| 의미 | `1 {new_unit} = {ratio} {ref_unit}` |
| 예시 | `register:cubit=0.4572:meter` |
| 검증 | `cubit:10` → meter raw ≈ 4.572 (EPS) |

### F-08 — json/csv

| format | 규칙 |
|--------|------|
| `format:json` | keys: `command`, `source`, `results[]`; target amount **4자리** half-up |
| `format:csv` | 헤더 `source_unit,source_amount,target_unit,target_amount` |
| `format:xml` | `UNSUPPORTED_FORMAT` |

### F-11 — TDD·레이어

- entity 테스트: I/O 0건
- RED → GREEN → REFACTOR (refactor 시 pytest green 유지)
- cov: §4.3

## 3.3 제약 (Gherkin Background 정본)

```text
base_unit = meter
meter  → 1.0
feet   → 3.28084
yard   → 1.09361
default format = table
EPS_ABS = 1e-9, EPS_REL = 1e-9
```

| 명령 | 패턴 |
|------|------|
| CONVERT | `{unit}:{amount}` |
| REGISTER | `register:{new}={ratio}:{ref}` |
| SET_FORMAT | `format:table|json|csv` |

---

# 4. 비기능 요구사항

## 4.1 기술 스택

| 항목 | 버전·도구 |
|------|-----------|
| 언어 | Python **3.11+** |
| 테스트 | **pytest**, **pytest-cov** |
| 검증·DTO | **pydantic** |
| 스타일 | Black, isort (line 88), 타입 힌트 필수 |

## 4.2 아키텍처

| 레이어 | 책임 |
|--------|------|
| **entity** | 환산·등록·불변식 (I/O 금지) |
| **control** | UseCase 오케스트레이션 |
| **boundary** | 파싱·포맷·stderr |
| **data** | Repository (JSON 등) |

**의존성:** boundary → control → entity; entity ↛ boundary/data

**원칙:** OCP(단위·포맷 확장), SRP, Dual-Track TDD

## 4.3 커버리지 목표

| 레이어 | Line % | Branch % |
|--------|--------|----------|
| entity | ≥ 95 | ≥ 90 |
| control | ≥ 90 | ≥ 85 |
| boundary | ≥ 85 | ≥ 80 |
| data | ≥ 90 | ≥ 85 |
| **overall** | ≥ 85 | — |

## 4.4 확장성

- 신규 단위: Registry/설정만; Engine if-elif 금지
- 신규 포맷: boundary만
- 신규 error code: ErrorPresenter + TC + Gherkin(해당 시) 동시 추가

---

# 5. 데이터 요구사항

## 5.1 단위 비율 (meter 허브)

| unit_id | meters_per_unit |
|---------|-----------------|
| meter | 1.0 |
| feet | 3.28084 |
| yard | 1.09361 |

feet↔yard: 위 비율로만 유도. 동등: `|a-b| <= max(1e-9, 1e-9×max(|a|,|b|))`

## 5.2 설정 외부화

```json
{
  "schema_version": 1,
  "base_unit": "meter",
  "units": [
    { "id": "meter", "meters_per_unit": 1.0 },
    { "id": "feet", "meters_per_unit": 3.28084 },
    { "id": "yard", "meters_per_unit": 1.09361 }
  ]
}
```

- 운영 기본: File(JSON)
- 테스트: InMemory 동일 스냅샷

## 5.3 동적 등록

`register:cubit=0.4572:meter` → `MetersPerUnit(cubit)=0.4572`

---

# 6. 출력 요구사항

## 6.1 table (기본)

| 항목 | 규칙 |
|------|------|
| 채널 | stdout (성공), stderr (실패) |
| 줄 | `{source} = {target}` — LHS 입력 보존 |
| target | 1자리 half-up |

## 6.2 JSON

| 필드 | 규칙 |
|------|------|
| `command` | `"CONVERT"` |
| `source.unit`, `source.amount` | 입력 |
| `results[].amount` | 4자리 half-up |
| `results.length` | = 등록 단위 수 |

## 6.3 CSV

헤더: `source_unit,source_amount,target_unit,target_amount`  
데이터 행 수 = 등록 단위 수; source 열 모든 행 동일.

## 6.4 포맷 정합

동일 CONVERT 입력 → table·json·csv의 (target_unit→amount) 집합 동일 (반올림 규칙만 상이).

---

# 7. 성공 지표

## 7.1 인수 기준

| ☐ | 기준 | Story / Gherkin |
|---|------|-----------------|
| ☐ | AC-01 | `meter:2.5` table 8.2/2.7, LHS 보존 | US-03,04 / #1 |
| ☐ | AC-02 | `meter:2.5.3` NON_NUMERIC | US-01 / #3 |
| ☐ | AC-03 | `meter:-1` NEGATIVE_VALUE | US-01 / #4 |
| ☐ | AC-04 | `cubit:1` UNKNOWN_UNIT | US-06 / #5 |
| ☐ | AC-05 | `feet:3.28084` 표현·meter 경유 yard | US-03,04 / #6,#8 |
| ☐ | AC-06 | register cubit → `cubit:10` | US-06 |
| ☐ | AC-07 | 설정 오류 시 기동 실패 | US-05 |
| ☐ | AC-08 | cov 임계·pytest 0 fail | US-07, G-04 |
| ☐ | AC-09 | Gherkin 8/8 pass | G-02 |

## 7.2 회귀 보호

| ID | 규칙 |
|----|------|
| REG-01 | Background 비율 변경 → 환산 TC 의도 fail |
| REG-02 | stderr regex·exit 변경 → Boundary TC fail |
| REG-03 | NEG-01·표현 계약 변경 → US-01·Gherkin #4,#6,#7 fail |
| REG-04 | schema_version 변경 without migration TC → fail |
| REG-05 | skip·assert 완화로 green → 인수 불합격 |
| REG-06 | entity→boundary import → 불합격 |

---

# 8. 용어 정의 (Glossary)

| 용어 | 정의 |
|------|------|
| **base unit** | 환산 허브; 고정 `meter` |
| **meters_per_unit** | 1 unit_id가 몇 meter인지 (양수 유한) |
| **UnitRegistry** | unit_id→비율 등록·조회 (entity) |
| **ConversionEngine** | Registry만 사용한 `convert_all` |
| **표현 계약** | 출력 줄 LHS = 사용자 입력 amount·unit |
| **NEG-01** | amount ≥ 0 유한; 음수 거부 |
| **error code** | stderr·TC·Gherkin 공통 식별자 |
| **EPS 동등** | \|a-b\| ≤ max(1e-9, 1e-9×max(\|a\|,\|b\|)) |
| **Dual-Track TDD** | Domain RED 우선; Boundary는 Mock |

---

# 부록 A — User Stories 요약

| Story | 요약 |
|-------|------|
| US-01 | 형식·숫자·음수·256자·문법·미등록 |
| US-02 | Registry·OCP·행 수·중복 |
| US-03 | README 수치·역변환·zero |
| US-04 | table/json/csv·표현 계약 |
| US-05 | JSON load·schema·기동 실패 |
| US-06 | register·cubit |
| US-07 | 레이어·RED·cov·회귀 |

---

# 부록 B — Gherkin 8 Scenarios 인덱스

| # | Tag | 요약 |
|---|-----|------|
| 1 | happy-path | `meter:2.5` |
| 2 | input-format | `meter` 무콜론 |
| 3 | decimal-parse-failure | `meter:2.5.3` |
| 4 | negative-policy | `meter:-1` |
| 5 | unknown-unit | `cubit:1` |
| 6 | expression-contract-feet | `feet:3.28084` LHS |
| 7 | zero-input | `yard:0` |
| 8 | feet-yard-via-meter | meter 경유 only |

> 상세 Feature 정의: Phase 4 Gherkin 문서 (8 scenarios).  
> **공백:** json/csv·REGISTER happy·설정 기동 실패는 US·PRD에 있으나 8-scenario 미포함 → pytest로 보완.

---

# 부록 C — Phase 4 추적

| PRD | Epic | Story | Gherkin |
|-----|------|-------|---------|
| §1.3 G-01~05 | SC-01~07 | US-02,03,06,07 | #1,#5,#8 |
| §3.3 Background | — | US-03,05 | BG, #1,#7,#8 |
| §7.1 AC-01~09 | — | US-01~07 | #1~#8 |

**Source of Truth:** 구현·테스트 작성 시 본 PRD §3.2·§3.3·§6·§7.1 우선. README와 충돌 시 PRD 계약 + README 비즈니스 비율을 병기 검토.
