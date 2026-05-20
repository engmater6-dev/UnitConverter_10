# Unit Converter (Python)

**meter 기준 길이 단위 변환 CLI**를 계약·pytest·BCE 레이어로 검증하며, **Python·TDD·클린 아키텍처 학습자**가 OCP/SRP와 테스트 선행 리팩터링을 체득하기 위한 실습 프로젝트입니다.

![unit-converter](./unit-converter.jpg)

---

## 목차

- [개요 (Overview)](#개요-overview)
- [진행 상황 (Progress)](#진행-상황-progress)
- [빠른 시작 (Quick Start)](#빠른-시작-quick-start)
- [지원 단위 및 비율](#지원-단위-및-비율)
- [입력 형식 계약](#입력-형식-계약)
- [아키텍처](#아키텍처)
- [테스트 실행](#테스트-실행)
- [설정 파일 (JSON/YAML)](#설정-파일-jsonyaml)
- [출력 포맷](#출력-포맷)
- [기여 가이드 (Contributing)](#기여-가이드-contributing)
- [라이선스](#라이선스)
- [관련 문서](#관련-문서)

---

## 개요 (Overview)

### 이 프로젝트가 해결하는 문제

- `단위:값` 한 줄 입력으로 등록된 길이 단위를 **상호 변환**해 출력한다.
- 레거시 스크립트는 비율이 코드 분기에 박혀 있어 **단위 추가·회귀 검증**이 어렵다.
- 본 프로젝트는 “곱셈 공식”보다 **계약(입력·stderr·출력)·불변식·테스트**를 먼저 고정하고, AI 보조 구현 환경에서도 행위가 흔들리지 않게 한다.

### 주요 학습 목표

| 목표 | 내용 |
|------|------|
| **OCP** | 신규 단위는 Registry·설정으로 추가; 환산 엔진 공개 API는 유지 |
| **SRP** | 환산(entity)·유스케이스(control)·파싱·포맷(boundary)·설정(data) 분리 |
| **BCE** | boundary → control → entity 의존; entity는 I/O·포맷 무의존 |
| **TDD** | RED(실패 테스트) → GREEN(최소 구현) → REFACTOR(green 유지) |

### PRD와의 연결

요구·인수·회귀 규칙의 **단일 기준(Source of Truth)** 은 [doc/PRD.md](doc/PRD.md)이며, 작업 진행은 [doc/TODO.md](doc/TODO.md)를 따릅니다.

> **구현 상태:** TDD **RED** 완료 — pytest 계약 테스트만 존재, `entity`/`boundary` **미구현**. CLI는 레거시 `main/UnitConverter.py`만 동작. 상세는 [진행 상황](#진행-상황-progress).

---

## 진행 상황 (Progress)

**최종 갱신:** 2026-05-20 · **현재 단계:** TDD RED (01)

### TDD 사이클

| 단계 | 상태 | 비고 |
|------|------|------|
| **RED** | ✅ 완료 | Domain·Boundary pytest 추가, 실행 시 fail 확인 |
| **GREEN** | 🔲 예정 | `entity/`, `boundary/` 최소 구현 |
| **REFACTOR** | 🔲 예정 | pytest green 유지하며 구조 정리 |

### 완료 항목

| 구분 | 산출물 | 설명 |
|------|--------|------|
| 문서 | `doc/PRD.md`, `doc/TODO.md`, `.cursorrules` | 계약·작업 기준선 |
| 테스트 | `pytest.ini`, `tests/helpers.py`, `tests/conftest.py` | EPS·Background fixture |
| entity RED | `tests/entity/test_registry.py` | meter/feet/yard 비율, `DUPLICATE_UNIT` |
| entity RED | `tests/entity/test_conversion.py` | `meter:2.5`, `feet:1` 역변환 (EPS) |
| boundary RED | `tests/boundary/test_input_parser.py` | F-02 오류 5종 (`MALFORMED_INPUT` 등) |
| boundary RED | `tests/boundary/test_output_formatter.py` | LHS 보존, target 1자리 half-up |
| boundary RED | `tests/boundary/test_error_presenter.py` | stderr `code`/`message`, exit 1 |
| 기록 | [prompt/01.red.md](prompt/01.red.md), [report/01.red.md](report/01.red.md) | 프롬프트 로그·RED 보고서 |

### 미구현 (GREEN 대상)

- `entity/` — `UnitRegistry`, `ConversionEngine`, `DomainError`
- `boundary/` — `CliInputParser`, `OutputFormatter`, `ErrorPresenter`
- `control/`, `data/`, `config/units.json` — v1.0 이후

### pytest 현황 (RED 검증)

```bash
py -3 -m pytest tests/ -v
# → exit 4, ModuleNotFoundError: No module named 'entity'
# (conftest가 entity를 import; 수집 TC 0건 — 구현 추가 후 assert 단계 fail/pass 재검증)
```

| 레이어 테스트 | 파일 수 | 실행 |
|---------------|---------|------|
| `tests/entity/` | 2 | import 실패로 미실행 |
| `tests/boundary/` | 3 | import 실패로 미실행 |

### TODO 연동 (doc/TODO.md)

| ID | RED 테스트 반영 | GREEN 구현 |
|----|-----------------|------------|
| M-01 | `test_registry.py` | 🔲 |
| M-02 | `test_conversion.py` | 🔲 |
| M-04, M-05 | `test_input_parser.py` | 🔲 |
| M-06 | `test_output_formatter.py` | 🔲 |
| M-07 | `test_error_presenter.py` | 🔲 |
| M-09 | Domain RED 게이트 | 🔲 assert fail → pass |

**다음 작업:** `entity/`·`boundary/` 스켈레톤 추가 후 `pytest tests/entity/ -v` → GREEN.

---

## 빠른 시작 (Quick Start)

### 사전 조건

| 항목 | 요구 |
|------|------|
| Python | **3.11+** |
| 패키지 관리 | `venv` 권장 |
| 테스트 (목표) | `pytest`, `pytest-cov` |
| 검증 (목표) | `pydantic` |

### 가상환경 · 실행 (레거시)

현재 저장소에는 레거시 진입점만 있습니다.

```bash
# 가상환경 생성
python -m venv venv

# 활성화 (Windows)
venv\Scripts\activate

# 활성화 (macOS/Linux)
source venv/bin/activate

# 실행 (레거시)
python main/UnitConverter.py
```

프롬프트에 `Insert value for converting (ex: meter:2.5):` 가 나오면 입력합니다.

### 예시 입출력 (목표 계약 · table)

**입력**

```text
meter:5.0
```

**stdout (목표 · PRD §6.1, 표시 1자리 half-up)**

```text
5.0 meter = 16.4 feet
5.0 meter = 5.5 yard
5.0 meter = 5.0 meter
```

| 항목 | 값 |
|------|-----|
| Domain raw (검증용) | feet ≈ 16.4042, yard ≈ 5.46805 |
| 줄 수 | 등록 단위 수 (기본 3) |
| exit code | `0` |

**표현 계약:** 모든 줄의 왼쪽 `{amount} {unit}` 은 **사용자 입력과 동일**합니다.

### 목표 진입점 (v1.0 이후)

```bash
# 목표 구조 (구현 후)
python -m boundary.main
# 또는
python boundary/main.py
```

---

## 지원 단위 및 비율

**기준 단위(hub):** `meter` — 모든 환산은 `meters_per_unit` 으로만 유도합니다.  
**feet ↔ yard 직접 비율 상수 사용 금지.**

| 표시명 | 식별자 (`unit_id`) | meters_per_unit (1 unit = X meter) | 출처 |
|--------|-------------------|-------------------------------------|------|
| meter | `meter` | `1.0` | PRD §5.1 · 기준 |
| feet | `feet` | `3.28084` | README · `1 m = 3.28084 ft` |
| yard | `yard` | `1.09361` | README · `1 m = 1.09361 yd` |

**동적 등록(권장):** 런타임에 `register:cubit=0.4572:meter` 등으로 추가.  
**부동소수 동등(EPS):** `|a−b| ≤ max(1e-9, 1e-9 × max(|a|,|b|))`

---

## 입력 형식 계약

### 명령 종류

| 명령 | 패턴 | 우선순위 |
|------|------|----------|
| CONVERT | `{unit_id}:{amount}` | 필수 |
| REGISTER | `register:{new}={ratio}:{ref_unit}` | 권장 |
| SET_FORMAT | `format:table` \| `format:json` \| `format:csv` | 권장 |

- `unit_id`: `[a-z][a-z0-9_]{0,31}`
- `amount`: 유한 실수, **`>= 0`** (정책 **NEG-01**)
- 입력 한 줄 최대 **256자**

### 정상 예시 3개

| 입력 | 의미 |
|------|------|
| `meter:2.5` | 2.5 meter를 모든 등록 단위로 변환 |
| `feet:3.28084` | 3.28084 feet → meter ≈ 1.0 (표현 계약: LHS `3.28084 feet`) |
| `register:cubit=0.4572:meter` | 1 cubit = 0.4572 meter 등록 (권장) |

### 비정상 예시 3개 + 에러

| 입력 | `code` | exit | stderr message 패턴 |
|------|--------|------|---------------------|
| `meter` (콜론 없음) | `MALFORMED_INPUT` | 1 | `Invalid format. Use unit:value (ex: meter:2.5)` |
| `meter:2.5.3` | `NON_NUMERIC` | 1 | `Invalid number: 2.5.3` |
| `meter:-1` | `NEGATIVE_VALUE` | 1 | `Value must be non-negative: -1` |

**실패 공통:** stdout에 `{source} = {target}` 형태 변환 줄 **0줄**.

### 기타 error code (참고)

| 조건 | `code` | exit |
|------|--------|------|
| 미등록 단위 `cubit:1` | `UNKNOWN_UNIT` | 1 |
| 257자 이상 | `INPUT_TOO_LONG` | 1 |
| `Meter` (대문자) | `INVALID_UNIT_ID` | 1 |
| NaN / Inf | `NON_FINITE_VALUE` | 1 |
| 설정 파일 오류 (기동) | `CONFIG_LOAD_FAILED` / `SCHEMA_INVALID` | 2 |
| `format:xml` | `UNSUPPORTED_FORMAT` | 1 |

상세: [doc/PRD.md §3.2](doc/PRD.md)

---

## 아키텍처

### BCE 레이어 (목표 구조)

```mermaid
flowchart TB
    subgraph boundary["boundary"]
        CLI[CliInputParser]
        FMT[OutputFormatter]
        ERR[ErrorPresenter]
    end
    subgraph control["control"]
        UC[ConvertUseCase / RegisterUseCase]
    end
    subgraph entity["entity"]
        REG[UnitRegistry]
        ENG[ConversionEngine]
    end
    subgraph data["data"]
        REPO[UnitRatioRepository]
    end
    CLI --> UC
    UC --> REG
    UC --> ENG
    UC --> REPO
    FMT --> CLI
    ERR --> CLI
    REPO -.->|implements Port| entity
```

### 의존성 방향

| 허용 | 금지 |
|------|------|
| boundary → control | entity → boundary |
| control → entity | entity → data 구현체 |
| control → data (Port) | control → boundary |

### 새 단위 추가 (코드 최소화)

1. **설정:** `config/units.json` 의 `units[]` 에 `{ "id": "...", "meters_per_unit": ... }` 추가  
2. **또는 런타임:** `register:new_unit=ratio:ref_unit` 입력  
3. **검증:** `pytest tests/entity/` — 기존 환산 TC는 수정 없이 pass  
4. **금지:** `ConversionEngine` 에 `if unit == "new":` 분기 추가  

환산식 (단일 경로):

```text
target_amount = source_amount × MetersPerUnit(source) ÷ MetersPerUnit(target)
```

### 디렉터리

**현재 (2026-05-20)**

```text
tests/           # ✅ RED pytest (entity / boundary)
tests/entity/    # test_registry.py, test_conversion.py
tests/boundary/  # test_input_parser.py, test_output_formatter.py, test_error_presenter.py
main/            # UnitConverter.py (레거시)
doc/             # PRD, TODO
prompt/          # 01.red.md
report/          # 01.red.md
pytest.ini
```

**목표 (v1.0)**

```text
entity/      # Domain — I/O 금지
control/     # UseCase
boundary/    # CLI · 파싱 · 포맷 · stderr
data/        # JSON 설정 Repository
tests/       # pytest (entity / boundary / data / integration)
config/      # units.json
```

---

## 테스트 실행

### 프레임워크

- **pytest** + **pytest-cov**

### 명령

```bash
# 전체 테스트 (현재: entity 미구현 → import 실패, RED)
py -3 -m pytest tests/ -v

# Domain만 (GREEN 이후)
py -3 -m pytest tests/entity/ -v

# 커버리지 (PRD §4.3)
python -m pytest tests/ \
  --cov=entity --cov=control --cov=boundary --cov=data \
  --cov-report=term-missing \
  --cov-fail-under=85
```

### 커버리지 목표

| 레이어 | Line % | Branch % |
|--------|--------|----------|
| entity | ≥ 95 | ≥ 90 |
| control | ≥ 90 | ≥ 85 |
| boundary | ≥ 85 | ≥ 80 |
| data | ≥ 90 | ≥ 85 |
| **overall** | ≥ 85 | — |

### 인수 · BDD

- **Gherkin:** 8 scenarios (PRD 부록 B) — happy path, 형식 오류, NON_NUMERIC, 음수, unknown unit, 표현 계약, zero, meter 경유  
- **체크리스트:** [doc/TODO.md](doc/TODO.md) §회귀 방지

---

## 설정 파일 (JSON/YAML)

### 위치 · 형식 (JSON 권장)

**경로:** `config/units.json`

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

| 규칙 | 실패 시 |
|------|---------|
| `schema_version` must be `1` | `SCHEMA_INVALID` |
| `meter` 행 필수, 비율 > 0 | `SCHEMA_INVALID` |
| 파일 없음 / JSON 깨짐 | `FILE_NOT_FOUND` / `PARSE_ERROR` / `CONFIG_LOAD_FAILED` |

기동 실패 시 **exit 2**, 변환 수행 없음.

**YAML:** 선택(v2). 스키마 의미는 JSON와 동일.

### 동적 단위 등록 (런타임)

```text
register:cubit=0.4572:meter
```

| 항목 | 값 |
|------|-----|
| 의미 | 1 cubit = 0.4572 meter |
| 검증 예 | `cubit:10` → meter amount ≈ **4.572** (EPS 내) |
| 등록 전 | `cubit:1` → `UNKNOWN_UNIT` |

---

## 출력 포맷

기본: **table** (`format:table` 또는 미지정)

### 콘솔 (table) — PRD §6.1

```text
{source_amount} {source_unit} = {target_amount} {target_unit}
```

- **target:** 소수 1자리, half-up  
- **source:** 입력 amount·unit 그대로 (표현 계약)

### JSON — PRD §6.2 (권장)

```json
{
  "command": "CONVERT",
  "source": { "unit": "meter", "amount": 5.0 },
  "results": [
    { "unit": "feet", "amount": 16.4042 },
    { "unit": "yard", "amount": 5.4681 },
    { "unit": "meter", "amount": 5.0 }
  ]
}
```

- `results[].amount`: **4자리** half-up  
- `results` 길이 = 등록 단위 수

### CSV — PRD §6.3 (권장)

```csv
source_unit,source_amount,target_unit,target_amount
meter,5.0,feet,16.4042
meter,5.0,yard,5.4681
meter,5.0,meter,5.0
```

- 헤더 1행 + 데이터 행 수 = 등록 단위 수  
- `source_unit`, `source_amount` 는 모든 데이터 행에서 동일

### 포맷 정합

동일 CONVERT 입력에 대해 table · json · csv 의 **(target_unit → amount) 집합은 동일** (포맷별 반올림 자릿수만 다름).

---

## 기여 가이드 (Contributing)

### 계약 변경 금지

- [doc/PRD.md](doc/PRD.md) §3.2·§3.3·§6·§7.1 과 **모순되는** 입출력·비율·error code·stderr 패턴 변경은 **별도 RFC + 테스트 일괄 갱신** 없이 merge 하지 않습니다.
- 테스트를 통과시키기 위해 **assert·기대값·error code만 완화**하는 PR은 거부합니다 (PRD REG-05).

### 테스트 없는 PR

- 신규 동작·버그 수정 PR은 **대응 pytest**(또는 Gherkin) **필수**.
- Domain 변경은 `tests/entity/`; 파싱·포맷은 `tests/boundary/`; 설정은 `tests/data/`.

### RED → GREEN → REFACTOR

1. 실패하는 테스트 추가 (RED)  
2. 최소 구현으로 해당 테스트만 green  
3. 전체 관련 pytest green 유지하며 refactor  

### 커밋 메시지 컨벤션

```text
<type>: <scope> — <summary>

type: feat | fix | test | refactor | docs
scope: entity | control | boundary | data | config
```

예:

```text
test: entity — add roundtrip feet to meters invariant
feat: boundary — map NEGATIVE_VALUE to stderr contract
docs: readme — align error codes with PRD 3.2
```

### 회귀 확인 (merge 전)

- [ ] `pytest` 0 fail  
- [ ] cov 임계 충족 (§4.3)  
- [ ] Gherkin 8/8 (또는 동등 체크리스트)  
- [ ] [doc/TODO.md](doc/TODO.md) 회귀 § REG-01~06  

---

## 라이선스

**MIT License** — 학습·실습용.

---

## 관련 문서

| 문서 | 설명 |
|------|------|
| [doc/PRD.md](doc/PRD.md) | 요구·계약·인수·회귀 (Source of Truth) |
| [doc/TODO.md](doc/TODO.md) | v1.0 작업·마일스톤·회귀 체크리스트 |
| [doc/README_ref.md](doc/README_ref.md) | 초기 README 보존본 |
| [report/01.red.md](report/01.red.md) | RED 단계 보고서 (산출물·pytest·GREEN 체크리스트) |
| [prompt/01.red.md](prompt/01.red.md) | RED 단계 프롬프트·답변 로그 |

---

## 생성형 AI 활용 Activities (6시간)

| 단계 | 시간 | 내용 |
|------|------|------|
| 1 | 0.5h | 레거시·PRD·계약 분석 — **진행 중** |
| 2 | 2h | 필수 요구·OCP/SRP·입력 검증 (M-01~M-11) — **RED 테스트 완료** |
| 3 | 0.5h | 환산·검증 TC |
| 4 | 2h | 설정·등록·포맷 (S-01~S-08) |
| 5 | 1h | 회고·인수 (G-01~G-05, AC, Gherkin) |

진행 상황: [진행 상황 (Progress)](#진행-상황-progress) · [doc/TODO.md](doc/TODO.md) 🔴 필수 항목 · [report/01.red.md](report/01.red.md)
