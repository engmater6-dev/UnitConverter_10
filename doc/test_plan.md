# 테스트 계획서 — Unit Converter (Python)

| 항목 | 내용 |
|------|------|
| **문서 버전** | 1.0 |
| **작성 관점** | 시니어 QA 리드 |
| **기준 문서** | [README.md](../README.md), [PRD.md](./PRD.md), [TODO.md](./TODO.md) |
| **샘플 예제 (정본)** | **meter 기준 전 단위 변환 (CONVERT · `convert_all`)** |
| **대표 입력** | `meter:2.5` |
| **대표 Domain 기대** | `2.5 meter → feet raw 8.2021` (`2.5 × 3.28084`, EPS 동등) |
| **대표 CLI table 기대** | `2.5 meter = 8.2 feet`, `2.5 meter = 2.7 yard`, `2.5 meter = 2.5 meter` |
| **기술 스택** | Python 3.11+, pytest, pytest-cov, pydantic |
| **방법론** | Dual-Track TDD — Logic(Domain) RED 우선, UI(Boundary) Mock |

---

## 1. 목적 및 범위

### 1.1 목적

본 계획서는 샘플 예제 **`meter:2.5` CONVERT** 를 중심으로, README 기본 요구사항 **1번**(다단위 출력)·**4번**(변환 정확성 TC) 및 PRD **F-01·F-02·F-03·F-04** 인수를 pytest로 검증하기 위한 단위·경계 테스트 범위를 정의한다.

### 1.2 In-Scope

| 레이어 | 패키지(목표) | 테스트 디렉터리 | 책임 |
|--------|--------------|-----------------|------|
| **Domain (Logic)** | `entity/` | `tests/entity/` | Registry, ConversionEngine, 환산식, NEG-01, EPS |
| **Control** | `control/` | `tests/control/` | ConvertUseCase 오케스트레이션 (Mock I/O) |
| **Boundary (UI)** | `boundary/` | `tests/boundary/` | CliInputParser, OutputFormatter, ErrorPresenter |
| **Data** | `data/` | `tests/data/` | JSON Repository (본 샘플의 2차 우선) |

### 1.3 Out-of-Scope (본 문서 1차 사이클)

- GUI / REST / 다국어
- REGISTER·json/csv·설정 로드 전체 시나리오 (별도 테스트 플랜 확장)
- `red_temp/` 아카이브 코드

---

## 2. 샘플 예제 추적 매트릭스

| 추적 ID | 요구 출처 | 검증 포인트 |
|---------|-----------|-------------|
| README 기본 **#1** | `meter:2.5` → 3줄 stdout, exit 0 | Boundary + 통합 |
| README 기본 **#4** | 단위 간 변환 정확성 TC | Entity (raw + EPS) |
| README 비즈니스 로직 | `1 m = 3.28084 ft`, `1 m = 1.09361 yd` | Entity; feet↔yard 직접 상수 **금지** |
| PRD **F-01** | CONVERT, `convert_all` 행 수 = 등록 수 | Entity + Control |
| PRD **F-02** | 입력 검증·stderr code | Boundary |
| PRD **F-03** | meter 허브, Background 비율 | Entity fixture |
| PRD **F-04** | LHS 입력 보존, table 1자리 half-up | Boundary |
| PRD **AC-01** | `meter:2.5` table 8.2/2.7 | Boundary capsys |
| PRD **Gherkin #1** | happy-path | Boundary / BDD |
| PRD **G-01** | Domain 환산 불변식 | Entity |
| PRD **G-03** | README 기본 변환 재현 | Boundary CLI |

### 2.1 환산 정본 (테스트 데이터)

| 단위 | meters_per_unit | `meter:2.5` target raw |
|------|-----------------|-------------------------|
| meter | 1.0 | 2.5 |
| feet | 3.28084 | **8.2021** |
| yard | 1.09361 | **2.734025** |

**EPS 동등:** `|a−b| ≤ max(1e-9, 1e-9 × max(|a|,|b|))` (PRD §3.3, §5.1)

**표현 계약:** 출력 LHS `{amount} {unit}` = 사용자 입력 그대로 (PRD §6.1).

---

## 3. pytest 단위 테스트 범위 및 우선순위

### 3.1 우선순위 정의

| 우선순위 | 의미 | 실행 게이트 |
|----------|------|-------------|
| **P0** | 샘플 예제·릴리스 차단 — 미통과 시 merge 불가 | 매 커밋 / PR |
| **P1** | 계약·회귀 — stderr 패턴·표현 계약·Gherkin 동등 | PR / 일일 |
| **P2** | Control·Data·cov branch 보강 | 마일스톤 M2~M3 |
| **P3** | 통합·성능·선택 요구 | v1.0 인수 전 |

### 3.2 P0 — Domain (Logic Track) · `tests/entity/`

| ID | 테스트 대상 | 시나리오 | 기대 |
|----|-------------|----------|------|
| E-P0-01 | `ConversionEngine.convert_all` | `meter:2.5` | results 3건; feet≈8.2021, yard≈2.734025, meter=2.5 (EPS) |
| E-P0-02 | meter→feet 단일 환산 | amount=1.0 | 1.0 × 3.28084 = 3.28084 (비율 직접 검증) |
| E-P0-03 | meter→yard 단일 환산 | amount=1.0 | 1.0 × 1.09361 = 1.09361 |
| E-P0-04 | `UnitRegistry` Background | 기본 3단위 | meter=1.0, feet=3.28084, yard=1.09361 |
| E-P0-05 | feet↔yard 금지 | 정적/동적 환산 | feet-yard **직접 비율 상수 0건**; meter 경유만 |
| E-P0-06 | `convert_all` 행 수 | Registry N단위 | 결과 len = N |
| E-P0-07 | 영값 | source `yard`, amount `0` | 모든 target amount = 0 |
| E-P0-08 | 음수 정책 NEG-01 | amount `< 0` | 변환 결과 **미생성**; `NEGATIVE_VALUE` (DomainError/Result) |
| E-P0-09 | 역변환 | `feet:3.28084` | meter raw ≈ 1.0 (EPS); LHS는 Boundary에서 검증 |

**규칙:** open/read/print/subprocess **0건** (PRD F-11).

### 3.3 P0 — Boundary (UI Track) · `tests/boundary/`

Domain은 **Mock/Stub**; 문자열·exit·stderr만 검증.

| ID | 테스트 대상 | 입력 | 기대 |
|----|-------------|------|------|
| B-P0-01 | CliInputParser + UseCase(Mock) | `meter:2.5` | exit 0; stdout 3줄; `8.2 feet`, `2.7 yard` (table) |
| B-P0-02 | ErrorPresenter | `meter:-1` | code `NEGATIVE_VALUE`, exit 1, stdout 0줄 |
| B-P0-03 | ErrorPresenter | `meter:abc` | code `NON_NUMERIC`, exit 1 |
| B-P0-04 | ErrorPresenter | `meter` (콜론 없음) | code `MALFORMED_INPUT`, exit 1 |
| B-P0-05 | ErrorPresenter | `parsec:1.0` | code `UNKNOWN_UNIT`, exit 1 |
| B-P0-06 | OutputFormatter table | `meter:2.5` | 모든 줄 LHS `2.5 meter` |
| B-P0-07 | 영값 CLI | `yard:0` | 3줄, target 전부 `0`; LHS `0 yard` |

### 3.4 P1 — 계약 보강

| ID | 레이어 | 시나리오 |
|----|--------|----------|
| E-P1-01 | entity | `meter:2.5.3` 파싱 전 — Domain은 미호출 (Boundary 책임) |
| B-P1-01 | boundary | `meter:2.5.3` → `NON_NUMERIC`, message `Invalid number: 2.5.3` |
| B-P1-02 | boundary | Gherkin #1~#5, #7, #8 동등 TC |
| E-P1-02 | entity | `feet:1` round-trip meter (REG-01 회귀용) |
| C-P1-01 | control | ConvertUseCase — Mock Registry로 `meter:2.5` 오케스트레이션 |

### 3.5 P2 / P3

| 우선순위 | 범위 |
|----------|------|
| P2 | `tests/data/` 설정 로드, `tests/control/` cov branch |
| P3 | `tests/integration/` register→convert, config 실패 기동 |

### 3.6 Dual-Track 실행 순서 (RED → GREEN)

1. **RED (Logic):** E-P0-01~09 실패 테스트 추가  
2. **RED (UI):** B-P0-01~07 — Engine Mock 후 실패 테스트  
3. **GREEN (Logic):** entity 최소 구현 → `pytest tests/entity/` green  
4. **GREEN (UI):** boundary 최소 구현 → `pytest tests/boundary/` green  
5. **REFACTOR:** pytest green 유지, 테스트 추가 없음  

---

## 4. 경계값 케이스 목록

### 4.1 샘플 예제 연계 — 정상·영값

| Case ID | 입력 | 레이어 | 기대 결과 | 우선순위 |
|---------|------|--------|-----------|----------|
| BV-01 | `meter:2.5` | entity + boundary | Happy path; raw 8.2021 / table 8.2·2.7 | P0 |
| BV-02 | `yard:0` | entity + boundary | 모든 target 0; LHS `0 yard`; exit 0 | P0 |
| BV-03 | `meter:0` | entity | feet=0, yard=0, meter=0 | P0 |

### 4.2 음수·부호 정책 (NEG-01)

| Case ID | 입력 | code | exit | stdout 변환 줄 |
|---------|------|------|------|----------------|
| BV-04 | `meter:-1` | `NEGATIVE_VALUE` | 1 | 0 |
| BV-05 | `feet:-0.001` | `NEGATIVE_VALUE` | 1 | 0 |
| BV-06 | `meter:-0` | 성공 허용 여부 명시 | 0 | `0`은 non-negative — **0.0 허용** (구현 시 TC 고정) |

### 4.3 파싱·형식 경계

| Case ID | 입력 | code | message 패턴 (PRD F-02) |
|---------|------|------|-------------------------|
| BV-07 | `meter:abc` | `NON_NUMERIC` | `Invalid number: abc` |
| BV-08 | `meter:2.5.3` | `NON_NUMERIC` | `Invalid number: 2.5.3` |
| BV-09 | `meter` (콜론 없음) | `MALFORMED_INPUT` | `Invalid format. Use unit:value (ex: meter:2.5)` |
| BV-10 | `parsec:1.0` | `UNKNOWN_UNIT` | `Unknown unit: parsec` |
| BV-11 | `Meter:1` | `INVALID_UNIT_ID` | `Invalid unit id: Meter` |
| BV-12 | 257자 이상 한 줄 | `INPUT_TOO_LONG` | `Input exceeds 256 characters` |

### 4.4 수치 극단 — 매우 큰 수·non-finite

| Case ID | 입력 | 검증 의도 | 기대 (초안) |
|---------|------|-----------|-------------|
| BV-13 | `meter:1e100` | 오버플로·finite 정책 | 결과가 **유한**이면 환산 성공; `inf`/`nan` 생성 시 `NON_FINITE_VALUE` 또는 Domain 거부 — **구현 확정 후 TC 잠금** |
| BV-14 | `meter:1.7976931348623157e308` | float 상한 근접 | 파싱 성공 시 overflow 여부 관측; 실패 시 `NON_FINITE_VALUE` |
| BV-15 | `meter:nan` / `meter:inf` | non-finite 입력 | `NON_FINITE_VALUE`, exit 1, stdout 0줄 |

> **QA 노트:** BV-13·14는 RED 단계에서 **관측 가능한 계약**을 먼저 고정한다. assert 완화·skip 금지 (REG-05).

### 4.5 표현·반올림 경계 (Boundary)

| Case ID | 입력 | 검증 |
|---------|------|------|
| BV-16 | `meter:2.5` | table target 1자리 half-up: `8.2`, `2.7` (not 8.2021 on stdout) |
| BV-17 | `feet:3.28084` | LHS `3.28084 feet`; meter 경유 yard (Gherkin #6, #8) |

---

## 5. 예외·특이 케이스 목록

| Case ID | 분류 | 설명 | 기대 |
|---------|------|------|------|
| EX-01 | 계약 | 실패 시 stdout 변환 줄 **0줄** | F-02 공통 |
| EX-02 | 계약 | stderr `code` + `message` regex 100% | F-05, G-02 |
| EX-03 | exit 분기 | 설정·기동 실패 | exit **2** (`CONFIG_LOAD_FAILED` 등) |
| EX-04 | exit 분기 | 입력·변환 실패 | exit **1** |
| EX-05 | Registry | meter 중복 등록 | `DUPLICATE_UNIT` |
| EX-06 | OCP 회귀 | feet 비율 1건 변경 | entity 환산 TC **다수 fail** (REG-01) |
| EX-07 | 레이어 | entity → boundary/data import | **0건** (REG-06) |
| EX-08 | TDD 금지 | skip / xfail / assert 완화 | PR 거부 |
| EX-09 | 표현 | Domain raw vs table 표시 | entity는 **8.2021**; CLI는 **8.2** — 동일 TC에서 혼동 금지 |
| EX-10 | Mock 경계 | Boundary가 실제 ConversionEngine 호출 | Dual-Track 위반 — Mock만 |
| EX-11 | 미등록 vs 문법 | `parsec:1` vs `Meter:1` | `UNKNOWN_UNIT` vs `INVALID_UNIT_ID` |
| EX-12 | 빈 amount | `meter:` | `NON_NUMERIC` 또는 `MALFORMED_INPUT` — **RED에서 기대값 고정** |

---

## 6. 테스트 설계 규칙

### 6.1 구조·네이밍

- 패턴: **AAA** (Arrange – Act – Assert)
- 이름: `test_<behavior>_<condition>_<expected>`
- fixture: `default_registry` (session) — meter/feet/yard 고정
- invariant docstring: RED 테스트에 1줄 (예: `INV-D01 meter hub conversion`)

### 6.2 Dual-Track 분리

| Track | 금지 | 허용 assert |
|-------|------|-------------|
| Logic | stdin/stdout/파일/JSON 포맷 | float EPS, Result/DTO, 행 수 |
| UI | 실제 환산식 중복 구현 | capsys, exit code, regex, LHS 문자열 |

### 6.3 pydantic

- 설정 DTO·입력 DTO 검증 실패 → `SCHEMA_INVALID` / validation error 매핑 (`tests/data/`, P2)

---

## 7. 커버리지 목표

출처: PRD §4.3, `.cursorrules` `testing.coverage_thresholds`

| 레이어 | Line % | Branch % | 본 샘플 예제 기여 |
|--------|--------|----------|-------------------|
| **entity (Domain)** | **≥ 95** | **≥ 90** | E-P0 전부 — **핵심** |
| **boundary (UI)** | **≥ 85** | **≥ 80** | B-P0, BV 파싱·stderr |
| control | ≥ 90 | ≥ 85 | ConvertUseCase (P1) |
| data | ≥ 90 | ≥ 85 | P2 |
| **overall** | **≥ 85** | — | `pytest --cov-fail-under=85` |

### 7.1 샘플 예제별 커버리지 포인트

| 모듈(목표) | 커버 대상 라인 |
|------------|----------------|
| `entity/conversion_engine.py` | `convert_all`, meter 허브 공식 |
| `entity/unit_registry.py` | `get_meters_per_unit`, 3단위 seed |
| `boundary/cli_input_parser.py` | `:` split, amount parse |
| `boundary/error_presenter.py` | F-02 code → message map |
| `boundary/output_formatter.py` | table half-up, LHS |

---

## 8. 커버리지 측정 전략

### 8.1 환경 준비

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install pytest pytest-cov pydantic
```

### 8.2 실행 명령 (레이어별 — 권장)

프로젝트 목표 구조는 패키지 `entity`, `control`, `boundary`, `data` 이다. **PRD·CI 정본:**

```bash
python -m pytest tests/ -v \
  --cov=entity --cov=control --cov=boundary --cov=data \
  --cov-report=term-missing \
  --cov-fail-under=85
```

**Domain·Boundary 게이트 분리 실행:**

```bash
# Domain (Logic) — 95% line 게이트
python -m pytest tests/entity/ -v \
  --cov=entity \
  --cov-report=term-missing \
  --cov-fail-under=95

# Boundary (UI) — 85% line 게이트
python -m pytest tests/boundary/ -v \
  --cov=boundary \
  --cov-report=term-missing \
  --cov-fail-under=85
```

### 8.3 요청 형식 (`--cov=unit_converter`) 매핑

단일 패키지명으로 측정할 경우(레거시·통합 패키지명 `unit_converter` 사용 시):

```bash
pip install pytest-cov
pytest --cov=unit_converter --cov-report=term-missing
```

| 상황 | 권장 |
|------|------|
| BCE 레이어 구현 후 | §8.2 **다중 `--cov=`** (정본) |
| 레거시 단일 모듈만 존재 | `--cov=unit_converter` 또는 `--cov=.` |
| HTML 리포트 | `--cov-report=html` → `htmlcov/` |

> **QA 판정:** Domain PR은 `entity` line ≥95%, Boundary PR은 `boundary` line ≥85%를 각각 확인. overall 85%는 merge 전 필수.

### 8.4 측정·게이트 절차

1. **로컬:** P0 TC green → 레이어별 cov 확인  
2. **PR:** `term-missing` 미커버 라인 리뷰 — 샘플 예제 관련 환산·파싱 경로 우선 보강  
3. **인수:** `doc/TODO.md` REG-01~06 + Gherkin 8/8 + AC-01~05  
4. **금지:** `pragma: no cover`로 임계 회피 (F-11)

### 8.5 `.coveragerc` (권장 초안)

```ini
[run]
source = entity, control, boundary, data
omit =
    tests/*
    */conftest.py

[report]
precision = 2
show_missing = True
fail_under = 85
```

---

## 9. 테스트 데이터·fixture

| Fixture | 내용 |
|---------|------|
| `default_registry` | meter=1.0, feet=3.28084, yard=1.09361 |
| `eps` | ABS=1e-9, REL=1e-9 |
| `mock_engine` | Boundary — `convert_all` 고정 반환 |
| `capsys` | stdout/stderr 캡처 |

---

## 10. 인수·완료 기준 (샘플 예제 기준)

| ☐ | 기준 |
|---|------|
| ☐ | `meter:2.5` entity TC — feet≈8.2021, yard≈2.734025 (EPS) |
| ☐ | `meter:2.5` CLI — 3줄, 8.2/2.7, LHS 보존, exit 0 |
| ☐ | BV-02~06, BV-07~12 전부 code·exit·stdout 0줄 일치 |
| ☐ | BV-13~15 계약 확정 후 TC green |
| ☐ | entity line ≥95%, boundary line ≥85% |
| ☐ | REG-05: skip·assert 완화 0건 |

---

## 11. 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-21 | 샘플 `meter:2.5` 기반 초안 — P0/P1, 경계값, cov 전략 |

---

## 부록 A — 샘플 TC 매핑 (pytest 제목 예시, 구현 참고용)

| Case ID | 예시 테스트명 |
|---------|---------------|
| E-P0-01 | `test_convert_all_meter_2_5_returns_three_targets_eps` |
| B-P0-01 | `test_cli_meter_2_5_table_three_lines_half_up` |
| BV-04 | `test_cli_meter_negative_one_negative_value_exit_1` |
| BV-07 | `test_cli_meter_abc_non_numeric_exit_1` |
| BV-09 | `test_cli_meter_no_colon_malformed_input_exit_1` |
| BV-10 | `test_cli_parsec_unknown_unit_exit_1` |
| BV-02 | `test_convert_all_yard_zero_all_targets_zero` |

*본 부록은 명명 가이드이며, 실제 코드는 RED 단계에서 별도 추가한다.*
