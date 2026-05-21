# 결함 목록 (Defect List) — Unit Converter

| 항목 | 내용 |
|------|------|
| **문서 버전** | 1.0 |
| **기준** | [test_plan.md](./test_plan.md), pytest `tests/` (36건) |
| **작성** | QA 리드 |
| **최종 갱신** | 2026-05-21 |
| **상태 요약** | 발견 8건 · **수정 완료 8건** · 회귀 **36/36 pass** |

---

## 결함 표

| ID | Severity | 변환 타입 | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-----------|-----------|--------|--------|-----------|-----------|
| DEF-001 | **Critical** | meter→feet | `ConversionEngine.convert("meter", 2.5, "feet")` 또는 입력 `meter:2.5` | `8.202100` (2.5×3.28084) | `0.762000` | `entity/conversion_engine.py` 에서 registry 계수(1 m = 3.28084 ft)를 **MPU÷MPU** 로 잘못 적용 (`amount * mpu_src / mpu_tgt`) | meter 허브: `amount_in_meter = amount / factor_src`, `return amount_in_meter * factor_tgt` (`conversion_engine.py` 41~44행) |
| DEF-002 | **Critical** | meter→yard | `convert("meter", 1.0, "yard")` | `1.093610` | `0.914403` | DEF-001과 동일 공식 오류 | DEF-001 수정으로 해소 |
| DEF-003 | **Critical** | feet→meter (역변환) | `convert("feet", 1.0, "meter")` | `0.304800` (1÷3.28084) | `3.280840` | 역변환 시 **나눗셈·곱셈 방향 반대** (허브 미경유) | DEF-001 수정으로 해소 |
| DEF-004 | **Critical** | convertAll | `convert_all("meter", 1.0)` → feet target | `3.280840` | `0.304800` | `convert_all` 이 오류 있는 `convert()` 호출 (연쇄) | DEF-001 수정으로 해소 |
| DEF-005 | **Major** | meter→feet (대량) | `convert("meter", 1e6, "feet")` | `3280840.0` | `304799.99` | DEF-001 동일 — 경계값이 아닌 **로직 오류** | DEF-001 수정으로 해소 |
| DEF-006 | **Major** | meter→feet (소수 6자리) | `convert("meter", 1.123456, "feet")` | `≈ 3.685879` | `≈ 0.342429` | DEF-001 동일 — 정밀도 TC 연쇄 실패 | DEF-001 수정으로 해소 |
| DEF-007 | **Minor** | CLI table (meter→feet·yard) | `UnitConverterApp.run_line("meter:2.5")` stdout | `2.5 meter = 8.2 feet`, `2.7 yard` | `2.5 meter = 0.8 feet`, `2.3 yard` | Boundary는 Domain 결과 표시만 함 — **DEF-001 파생** | DEF-001 수정 후 `test_app_meter_2_5_returns_three_line_table` pass |
| DEF-008 | **Major** | registerUnit→convert (cubit) | `register_from_ref("cubit", 0.4572, "meter")` 후 `convert("cubit", 10, "meter")` | `4.572000` | (수정 전) 비율 뒤집힘 가능 | `unit_registry.py` 에서 `ratio * ref_factor` 로 등록 — 허브와 불일치 | `ref_factor / ratio` 로 변경 (`unit_registry.py` 33~37행) |

---

## 심각도 정의 (사용 기준)

| Severity | 기준 |
|----------|------|
| **Critical** | 핵심 CONVERT 결과가 계약·비즈니스 비율과 완전히 불일치 |
| **Major** | 경계·등록·대량 입력 등 파생 기능 실패 (로직/데이터 오류) |
| **Minor** | 표시·포맷만 틀림 (Domain 수정 시 자동 해소) |
| **Info** | 스타일·문서·레거시 미연동 (본 목록 미등재) |

---

## 재현 명령 (결함 확인·회귀)

```bash
cd c:\DEV\2-4.unit_converter
py -3 -m pip install -r requirements-dev.txt

# 결함 재현 시점(수정 전): entity 정상 변환 5건 + boundary table 1건 FAIL
py -3 -m pytest tests/entity/test_conversion_normal.py tests/boundary/test_app_integration.py::test_app_meter_2_5_returns_three_line_table -v --tb=short

# 수정 후 회귀 (전체 Green)
py -3 -m pytest tests/ -v
```

---

## 회귀·인수 상태

| ☐ | 항목 | 결과 |
|---|------|------|
| ☑ | DEF-001 ~ DEF-008 수정 반영 | `entity/conversion_engine.py`, `entity/unit_registry.py` |
| ☑ | pytest 전체 | **36 passed** (2026-05-21) |
| ☑ | 샘플 `meter:2.5` | entity raw 8.2021 · CLI table 8.2 / 2.7 |
| ☐ | cov 게이트 entity ≥95%, boundary ≥85% | 별도 `pytest --cov` 실행 시 확인 |

---

## 참고 (범위 외)

| 항목 | 설명 |
|------|------|
| `UnitConverter.py` (레거시) | 루트 스크립트는 `meter_value * 3.28084` 로 **부분 정상**이나 BCE·pytest 스위트 미연동 — 본 결함 목록의 재현 경로 아님 |
| `red_temp/` | 아카이브 — 검토·결함 추적 제외 |

---

## 문서 이력

| 버전 | 날짜 | 변경 |
|------|------|------|
| 1.0 | 2026-05-21 | 초기 8건 등록 (RED/GREEN 디버깅 기준), 전건 수정·회귀 pass |
