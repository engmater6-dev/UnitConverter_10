# RED Phase Tests — Dual-Track UI + Logic TDD

| 항목 | 내용 |
|------|------|
| **프로젝트** | `c:\DEV\2-4.unit_converter` |
| **현재 코드 가정** | `UnitConverter.py` 단일 `main()`, if-else, **ValueError/TypeError 미사용** |
| **비율 계약** | 1 meter = 3.28084 feet · 1 meter = 1.09361 yard |
| **pytest 실행 (RED만)** | `py -3 -m pytest tests/red/ -v` |
| **구현/GREEN/REFACTOR** | **금지** (본 문서·`tests/red/` 만) |

---

# UI RED Tests — Test ID / Given/When/Then / Invariant

## UI-RED-01 — Happy Path CONVERT

| 항목 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_red_01_meter_2_5_returns_formatted_conversion` |
| **Given** | 등록 단위 meter·feet·yard; 비율 1 m = 3.28084 ft, 1 m = 1.09361 yd; 입력 문자열 `"meter:2.5"` |
| **When** | Boundary가 CONVERT를 파싱·실행해 변환 결과 문자열을 반환한다 |
| **Then** | 반환값에 `"2.5 meter = 8.202100 feet"` 포함 (Domain raw 8.2021, **표시 6자리** 계약) |
| **Invariant** | **INV-UI-01** Happy path — `meter:2.5` → feet 환산 결과가 비율 곱과 일치하며 계약 포맷을 따른다 |
| **RED 실패 사유 (현재)** | 레거시는 `8.2021` raw 출력·6자리 고정 포맷·**반환값 없음**(print만) |

---

## UI-RED-02 — 콜론 없는 입력

| 항목 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_red_02_no_colon_raises_value_or_type_error` |
| **Given** | 잘못된 형식 입력 `"meter"` (콜론 없음) |
| **When** | Boundary 파서/실행기에 전달 |
| **Then** | `ValueError` 또는 `TypeError` 발생; stdout 변환 줄 0줄 |
| **Invariant** | **INV-UI-02** 형식 오류는 예외로 표면화 — stderr print 후 return 금지 |
| **RED 실패 사유** | 레거시는 `print` 후 `return`만 하고 **예외 미발생** |

---

## UI-RED-03 — 음수 입력

| 항목 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_red_03_negative_meter_raises_value_or_type_error` |
| **Given** | NEG-01 정책; 입력 `"meter:-1.0"` |
| **When** | Boundary 실행 |
| **Then** | `ValueError` 또는 `TypeError`; 변환 결과 미반환 |
| **Invariant** | **INV-UI-03** `amount >= 0` — 음수는 예외 |
| **RED 실패 사유** | 레거시는 음수를 **환산함** (검증 없음) |

---

## UI-RED-04 — 미등록 단위

| 항목 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_red_04_unknown_unit_parsec_raises_value_or_type_error` |
| **Given** | Registry에 `parsec` 없음; 입력 `"parsec:1.0"` |
| **When** | Boundary 실행 |
| **Then** | `ValueError` 또는 `TypeError` |
| **Invariant** | **INV-UI-04** 미등록 단위는 예외 — Unknown print 후 return 금지 |
| **RED 실패 사유** | 레거시는 `Unknown unit` **print** 후 return |

---

## UI-RED-05 — 소수 파싱 실패 (TC-A-05 확장)

| 항목 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_red_05_non_numeric_amount_raises_value_or_type_error` |
| **Given** | 입력 `"meter:abc"` |
| **When** | Boundary 파싱 |
| **Then** | `ValueError` 또는 `TypeError` |
| **Invariant** | **INV-UI-05** 비숫자 amount는 예외 |
| **RED 실패 사유** | 레거시는 `Invalid number` print 후 return |

---

## UI-RED-06 — 표현 계약 (LHS 보존)

| 항목 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_red_06_output_preserves_source_unit_and_amount` |
| **Given** | 입력 `"meter:2.5"`; 표현 계약 PRD §6.1 |
| **When** | table 포맷 줄 생성 |
| **Then** | 모든 출력 줄이 `"2.5 meter = "` 로 시작 |
| **Invariant** | **INV-UI-06** LHS = 사용자 입력 amount·unit (변환된 source 금지) |
| **RED 실패 사유** | 레거시는 LHS는 맞으나 **API 반환·table half-up** 미구현 — 포맷 검증 API 없음 |

---

## UI-RED-07 — JSON 출력 스키마

| 항목 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_red_07_format_json_returns_valid_schema` |
| **Given** | `format:json` 요청 후 `meter:2.5` CONVERT |
| **When** | JSON OutputFormatter 실행 |
| **Then** | `command=="CONVERT"`, `source.unit=="meter"`, `results[]` 길이=등록 단위 수, feet amount 4자리 half-up |
| **Invariant** | **INV-UI-07** PRD §6.2 JSON 스키마·키 집합 고정 |
| **RED 실패 사유** | 레거시에 **JSON 출력·format 명령 없음** (`ModuleNotFoundError` / API 부재) |

---

# Logic RED Tests — Test ID / Scenario / Invariant

> **전제 API (미구현):** `logic.converter.convert`, `convert_all`, `register_unit`, `logic.config.load_config`  
> **현재:** `UnitConverter.py` `main()` only → **ImportError / pytest.fail**

---

## LOGIC-RED-01 — meter → feet

| 항목 | 내용 |
|------|------|
| **Test ID** | LOGIC-RED-01 |
| **Scenario** | `convert("meter", 2.5, "feet")` — 1 meter = 3.28084 feet |
| **Invariant** | **INV-D-01** `result ≈ 8.20210` (오차 ≤ 1e-5) |
| **RED 실패** | `logic.converter` 모듈 없음 |

---

## LOGIC-RED-02 — meter → yard

| 항목 | 내용 |
|------|------|
| **Test ID** | LOGIC-RED-02 |
| **Scenario** | `convert("meter", 1.0, "yard")` — 1 meter = 1.09361 yard |
| **Invariant** | **INV-D-02** `result ≈ 1.09361` (오차 ≤ 1e-5) |
| **RED 실패** | Domain API 미구현 |

---

## LOGIC-RED-03 — feet → meter (역변환)

| 항목 | 내용 |
|------|------|
| **Test ID** | LOGIC-RED-03 |
| **Scenario** | `convert("feet", 1.0, "meter")` — 역변환 |
| **Invariant** | **INV-D-03** `result ≈ 0.30480` (1÷3.28084, 오차 ≤ 1e-5) |
| **RED 실패** | Domain API 미구현 |

---

## LOGIC-RED-04 — convertAll

| 항목 | 내용 |
|------|------|
| **Test ID** | LOGIC-RED-04 |
| **Scenario** | `convert_all("meter", 1.0)` → meter·feet·yard **전 단위** |
| **Invariant** | **INV-D-04** 반환 len = Registry 등록 수; feet≈3.28084, yard≈1.09361 |
| **RED 실패** | `convert_all` 함수 없음 |

---

## LOGIC-RED-05 — registerUnit

| 항목 | 내용 |
|------|------|
| **Test ID** | LOGIC-RED-05 |
| **Scenario** | `register_unit("cubit", 0.4572)` 후 `convert("cubit", 10, "meter")` |
| **Invariant** | **INV-D-05** 1 cubit = 0.4572 m → 결과 ≈ 4.572 (EPS) |
| **RED 실패** | 동적 등록 API 없음 |

---

## LOGIC-RED-06 — loadConfig 유효 JSON

| 항목 | 내용 |
|------|------|
| **Test ID** | LOGIC-RED-06 |
| **Scenario** | `load_config(valid_json_path)` → 파일 비율 Registry 적용 |
| **Invariant** | **INV-D-06** `feet==3.28084`, `yard==1.09361` (파일 정의와 동일) |
| **RED 실패** | `logic.config` 미구현 |

---

## LOGIC-RED-07 — loadConfig 없는 경로

| 항목 | 내용 |
|------|------|
| **Test ID** | LOGIC-RED-07 |
| **Scenario** | `load_config("/nonexistent/units.json")` |
| **Invariant** | **INV-D-07** 기본값 유지 — feet=3.28084, yard=1.09361 |
| **RED 실패** | 설정 로드 API 미구현 |

---

## LOGIC-RED-08 — meter:abc (Domain 경계, Boundary와 분리)

| 항목 | 내용 |
|------|------|
| **Test ID** | LOGIC-RED-08 |
| **Scenario** | Domain `convert`는 파싱 책임 없음 — 음수·NaN만 DomainError |
| **Invariant** | **INV-D-08** entity 테스트에 I/O 0건 |
| **RED 실패** | (Logic 패키지 부재로 RED-01~07과 동일) |

---

## 실행·게이트

```bash
py -3 -m pytest tests/red/ -v --tb=short
# 기대: RED 구간 전부 FAIL (legacy + API 부재)
# GREEN 단계에서 logic/·boundary/ 구현 후 별도 tests/ 스위트 통과
```
