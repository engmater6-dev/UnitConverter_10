# To-Do 리스트 — UnitConverter (Python)

| 항목 | 내용 |
|------|------|
| **워크스페이스** | `c:\DEV\2-4.unit_converter` |
| **기준 문서** | [PRD.md](./PRD.md) §3 기능 · §7.1 인수 · §7.2 회귀 |
| **v1.0 정의** | 필수(Must) + AC-01~05,08,09 + G-01~03, G-05 |
| **검증 주체** | **학습자** = 구현·로컬 pytest · **리뷰어** = 인수·레이어·회귀 · **자동** = pytest/cov/Gherkin |

---

## 🔴 필수 (Must-Have) — v1.0 릴리스 차단 항목

- [ ] **M-01** entity 레이어 골격 및 Registry 3단위 고정 | PRD F-03, §5.1, §3.3 Background | **학습자**가 `pytest tests/entity/` 실행 시 **리뷰어**가 meter=1.0·feet=3.28084·yard=1.09361 동등·`DUPLICATE_UNIT` on meter 재등록 pass 확인
- [ ] **M-02** ConversionEngine `convert_all` meter 경유 환산 | PRD F-01, F-03, G-01, AC-01 | **학습자**가 entity TC에서 `meter:2.5` raw feet≈8.2021·yard≈2.734025·`feet:1` 역변환 EPS pass 제출 → **리뷰어** 승인
- [ ] **M-03** feet↔yard 직접 비율 상수 0건 | PRD F-03, G-05, REG-01 | **리뷰어**가 entity/control/boundary 정적 검색·TC에서 직접 상수 0건 확인 후 pass
- [ ] **M-04** CONVERT 파싱·검증 (F-02 전 code) | PRD F-02, US-01, AC-02~04 | **자동** Boundary/entity TC가 `MALFORMED_INPUT`·`NON_NUMERIC`·`NEGATIVE_VALUE`·`UNKNOWN_UNIT`·`INPUT_TOO_LONG`·`INVALID_UNIT_ID` 각 exit 1·stdout 0줄 pass
- [ ] **M-05** NEG-01 음수·non-finite 거부 | PRD §3.2 NEG-01, AC-03 | **학습자**가 `meter:-1`·NaN/Inf 입력 TC green → **리뷰어** Gherkin #4 및 TC 대조 pass
- [ ] **M-06** table 출력·표현 계약 (LHS 입력 보존) | PRD F-04, §6.1, AC-01, AC-05 | **학습자**가 CLI `meter:2.5`·`feet:3.28084` 실행 캡처 제출 → **리뷰어**가 모든 줄 LHS=입력·target 1자리 half-up(8.2/2.7) 확인
- [ ] **M-07** ErrorPresenter stderr code·message·exit | PRD F-05, G-02 | **자동** TC가 F-02 표의 message regex·exit 1/2 100% 일치 → **리뷰어** spot 5종 stderr 승인
- [ ] **M-08** boundary/control/entity/data 디렉터리·의존 방향 | PRD §4.2, F-11, REG-06 | **리뷰어**가 entity→boundary/data import 0건 grep 후 pass
- [ ] **M-09** Domain RED→GREEN 게이트 (entity I/O 금지) | PRD F-11, US-07 | **학습자**가 RED fail 스크린샷·이후 `tests/entity/` 0 fail 로그 제출 → **리뷰어** entity 테스트 내 open/print/subprocess 0 확인
- [ ] **M-10** control ConvertUseCase 오케스트레이션 | PRD §4.2, F-01 | **자동** `tests/control/` pass 시 **학습자**가 boundary Mock 없이 control 단위 green 확인
- [ ] **M-11** boundary CliInputParser + table OutputFormatter | PRD F-01, F-04, G-03 | **학습자**가 `python`(진입점) `meter:2.5` 실행 → **리뷰어** AC-01 stdout 3줄·exit 0 확인
- [ ] **M-12** Gherkin 8 scenarios 전부 pass | PRD AC-09, G-02, 부록 B | **학습자**가 BDD 또는 수동 시나리오 체크리스트 8/8 제출 → **리뷰어** #1~#8 서명
- [ ] **M-13** AC-01~05, AC-08, AC-09 인수 체크 | PRD §7.1 | **리뷰어**가 §7.1 표 해당 행 전부 ☑ 후 v1.0 릴리스 승인
- [ ] **M-14** `yard:0` zero 변환 | PRD F-01, Gherkin #7, US-03 | **자동** TC·Gherkin #7에서 모든 target 0·LHS `0 yard` pass

---

## 🟡 권장 (Should-Have) — 품질 향상 항목

- [ ] **S-01** `config/units.json` + JsonFileRepository | PRD F-06, §5.2, AC-07 | **학습자**가 유효 JSON 기동 후 3단위 Registry 일치 TC pass → **리뷰어** 파일 삭제 시 exit 2·`meter:2.5` 변환 없음 확인
- [ ] **S-02** 설정 실패 code (`SCHEMA_INVALID`, `PARSE_ERROR`, `FILE_NOT_FOUND`) | PRD F-06, US-05 | **자동** `tests/data/` 3종 fail·pass → **리뷰어** AC-07 ☑
- [ ] **S-03** REGISTER `register:cubit=0.4572:meter` | PRD F-07, AC-06, US-06 | **학습자**가 등록 후 `cubit:10` meter≈4.572 TC·로그 제출 → **리뷰어** 등록 전 `UNKNOWN_UNIT` 확인
- [ ] **S-04** REGISTER 실패 (`DUPLICATE_UNIT`, `INVALID_RATIO`, ref `UNKNOWN_UNIT`) | PRD F-07, US-06 | **자동** register TC 3종 pass
- [ ] **S-05** `format:json` 출력 스키마 | PRD F-08, §6.2, US-04 | **자동** boundary TC가 keys·results 길이·4자리 half-up pass
- [ ] **S-06** `format:csv` 헤더·행 수·source 열 일정 | PRD F-08, §6.3 | **자동** csv TC pass → **리뷰어** AC-04 보완 ☑
- [ ] **S-07** 3포맷 수치 집합 동일 | PRD §6.4, US-04 | **자동** 동일 입력 table/json/csv target 집합 TC pass
- [ ] **S-08** `format:xml` → `UNSUPPORTED_FORMAT` | PRD F-08 | **자동** TC exit 1·code 일치 pass
- [ ] **S-09** pytest-cov 레이어 임계 | PRD §4.3, G-04, AC-08 | **학습자**가 cov 리포트 제출 → **리뷰어** entity≥95·boundary≥85·data≥90·control≥90·overall≥85 확인
- [ ] **S-10** 통합 TC (register→convert, 설정 실패 기동) | PRD AC-06, AC-07, 부록 B 공백 보완 | **자동** `tests/integration/` ≥2 pass (Gherkin에 없는 AC-06·07)
- [ ] **S-11** README 실행·계약 요약 갱신 | PRD 부록 C, Phase 6 이관 | **학습자**가 루트 README에 명령·error code·config 경로 추가 PR → **리뷰어** PRD §3.2와 모순 0건 확인
- [ ] **S-12** AC-06·AC-07 인수 | PRD §7.1 | **리뷰어** AC-06·07 ☑ (v1.1 품질 게이트)

---

## 🟢 선택 (Nice-to-Have) — v2.0 후보

- [ ] **N-01** YAML 설정 로더 (JSON 동일 스키마) | PRD F-09 | **기대 가치:** 설정 포맷 선택 유연성 without Engine 변경
- [ ] **N-02** REGISTER 후 `units.json` 영속 save | PRD F-10 | **기대 가치:** 재기동 후에도 cubit 등록 유지
- [ ] **N-03** Gherkin에 json/csv·register happy·config 기동 시나리오 추가 | PRD 부록 B 공백 | **기대 가치:** BDD만으로 AC-06·07·US-04 완전 추적
- [ ] **N-04** stderr `field` 메타 (unit/value/line) | PRD F-02 확장 | **기대 가치:** 클라이언트 파싱·디버깅 일관성
- [ ] **N-05** 다중 명령 REPL 루프 (format 세션 유지) | — | **기대 가치:** 연속 실습 UX (계약 명시 필요)
- [ ] **N-06** `.cursorrules` / `pyproject.toml` 프로젝트 규칙 고정 | PRD §4.1 | **기대 가치:** AI 보조 시 레이어·TDD 자동 준수

---

## 🔵 기술 부채 (Tech Debt)

- [ ] **TD-01** 단일 파일 `UnitConverter.py` if-elif·하드코딩 비율 | PRD §1.2 | **원인:** 초기 실습용 스크립트 · **방향:** M-01~M-11 완료 후 진입점만 boundary `main`에 위임·레거시 deprecate
- [ ] **TD-02** stderr가 error code 없이 plain print만 | PRD F-05 | **원인:** 레거시 · **방향:** M-07 ErrorPresenter 단일 매핑
- [ ] **TD-03** 음수·256자·INVALID_UNIT_ID 미검증 | PRD F-02, US-01 | **원인:** 레거시 최소 검증 · **방향:** M-04, M-05
- [ ] **TD-04** README 예시만 있고 PRD 계약(NEG-01·표현·EPS) 미문서화 | PRD §7, Phase 6 | **원인:** README가 비즈니스만 기술 · **방향:** S-11 또는 `doc/CONTRACT.md` 링크
- [ ] **TD-05** Epic SC-04 “4 scenarios” vs PRD 8 scenarios 표기 혼재 | 부록 B | **원인:** Phase 4 문서 버전 분기 · **방향:** PRD 부록 B를 정본으로 통일(완료 시 TD-05 ☑)
- [ ] **TD-06** Gherkin 8 vs pytest AC-06·07·08 공백 | PRD §7.1 | **원인:** BDD 범위 축소 · **방향:** S-10 통합 TC 필수화 또는 N-03
- [ ] **TD-07** 테스트·src 레이어 디렉터리 부재 | PRD §4.2 | **원인:** 문서 선행 · **방향:** M-08 트리 생성 후 F-11 cov 게이트

---

## ✅ 완료 항목 (Done)

- [x] PRD 통합 문서 작성 (`doc/PRD.md`) | 2026-05-20 | docs: add PRD Phase 4/5 baseline
- [x] README 원본 보존 (`doc/README_ref.md`) | 2026-05-20 | docs: archive README reference
- [x] 레거시 `UnitConverter.py` 기본 변환 프로토타입 (meter/feet/yard) | (선행) | feat: initial unit converter script — **PRD 인수 미달, v1.0 차단 해제 아님**

---

## 📋 회귀 방지 체크리스트 (PRD §7.2)

**배포(v1.0 인수) 전 — 리뷰어가 전항 ☑, 학습자가 증거 첨부**

| ☐ | 항목 | 누가 | 무엇을 | 어떻게 → 통과 |
|---|------|------|--------|----------------|
| ☐ | REG-01 | 학습자 | feet 비율 1건 의도 변경 | pytest entity 환산 TC **다수 fail** 확인 후 원복 |
| ☐ | REG-02 | 자동 | stderr·exit 변경 | Boundary TC **전부 fail** → 패턴 복구 후 green |
| ☐ | REG-03 | 자동 | NEG-01·표현 계약 | `meter:-1`·`feet:3.28084` LHS TC·Gherkin #4,#6,#7 pass |
| ☐ | REG-04 | 학습자 | `schema_version:2` 실험 | data·통합 TC fail 확인 후 파일 복구 |
| ☐ | REG-05 | 리뷰어 | skip·assert 완화 여부 | PR diff에 `skip`·완화 assert **0건** |
| ☐ | REG-06 | 리뷰어 | 레이어 역import | entity→boundary/data **0건** |
| ☐ | 계약 테스트 | 학습자 | 전체 pytest | `pytest` **0 fail** |
| ☐ | 커버리지 | 학습자 | pytest-cov | §4.3 임계 **전부 충족** (AC-08) |
| ☐ | Gherkin | 학습자 | 8 scenarios | **8/8 pass** (AC-09) |
| ☐ | README | 학습자 | 루트 README | 실행 명령·3비율·추가 요구 **PRD와 모순 없음** (S-11) |

---

## 🗓️ 마일스톤

| 마일스톤 | 포함 항목 (PRD) | 목표일 | 상태 | 통과 판정자 |
|----------|-----------------|--------|------|-------------|
| **M0 문서·기준선** | PRD §1~§8, TODO, README_ref | 2026-05-20 | ✅ Done | 리뷰어 |
| **M1 Domain GREEN** | F-03, F-01(entity), F-11(entity), M-01~M-05, M-09, M-14, G-01 | T+1일 | 🔲 Planned | 학습자 TC + 리뷰어 G-01 |
| **M2 Boundary·README v1** | F-02, F-04, F-05, M-06~M-08, M-10~M-12, G-02, G-03, AC-01~05, AC-09 | T+2일 | 🔲 Planned | 리뷰어 AC-01~05·09 |
| **M3 품질·확장 v1.1** | F-06~F-08, S-01~S-12, G-04, AC-06~08 | T+3일 | 🔲 Planned | 리뷰어 AC-06~08·G-04 |
| **M4 v1.0 인수** | §7.1 AC 필수 전부, §7.2 REG, G-01~G-05 | T+4일 | 🔲 Planned | 리뷰어 §7.1·7.2 ☑ = 릴리스 |
| **M5 v2.0 후보** | F-09, F-10, N-01~N-06 | 미정 | 🔲 Backlog | — |

> **T+n:** 실습 6시간 캘린더에 맞춰 팀이 M1~M3를 0.5+2+0.5+2h Activities에 매핑.

---

## v1.0 릴리스 게이트 (한 줄)

**리뷰어**가 Must M-01~M-14 전부 ☑ **및** §7.1 AC-01~05·08·09 ☑ **및** 회귀 체크리스트 전항 ☑일 때만 v1.0 인수.
