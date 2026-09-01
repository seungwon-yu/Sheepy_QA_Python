# AGENTS.md

## 프로젝트 역할

이 저장소는 Steam 게임 `Sheepy: A Short Adventure`를 대상으로 Python 자동화 QA를 연습하는 프로젝트이다.

이번 프로젝트의 1차 목표는 하네스나 루프 엔지니어링을 바로 적용하는 것이 아니라, ISTQB 기준으로 테스트 대분류와 TC를 체계적으로 나누고 일반 자동화 QA를 먼저 구현하는 것이다.

## 읽는 순서

1. `README.md`에서 프로젝트 목적을 확인한다.
2. `docs/test-basis-and-standards.md`에서 어떤 기준으로 테스트를 설계하는지 확인한다.
3. `docs/test-classification.md`에서 TC 대분류와 소분류 기준을 확인한다.
4. `docs/test-cases.md`에서 개별 TC를 확인한다.
5. `docs/traceability-matrix.md`에서 기준, 대분류, 소분류, TC 연결을 확인한다.
6. `docs/sprint-plan.md`에서 Sprint별 실행 순서와 개별 실행 스크립트를 확인한다.
7. `docs/guardrails.md`에서 테스트 수행 제한사항을 확인한다.
8. 코드를 수정하기 전에 `docs/code-convention.md`를 확인한다.
9. 커밋하기 전에 `docs/commit-convention.md`를 확인한다.
10. CI 관련 변경 전 `docs/ci.md`를 확인한다.

## 저장소 지도

- `src/sheepy_qa/config.py`: Sheepy AppID와 공통 설정.
- `src/sheepy_qa/steam_app.py`: Steam AppID 실행 명령 생성.
- `src/sheepy_qa/steam_environment.py`: Steam 실행 환경 snapshot 생성.
- `src/sheepy_qa/process_check.py`: 프로세스 상태 관찰 유틸.
- `src/sheepy_qa/screen_capture.py`: 화면 캡처 유틸.
- `src/sheepy_qa/wait.py`: 로컬 자동화용 제한 시간 대기 유틸.
- `src/sheepy_qa/local_test_config.py`: 로컬 Steam 테스트 실행 플래그.
- `src/sheepy_qa/evidence.py`: evidence 디렉터리와 JSON 저장 유틸.
- `tests/unit/`: 실제 게임 실행 없이 검증 가능한 기본 유틸 테스트.
- `tests/local/`: 실제 Steam과 Sheepy 실행이 필요한 로컬 전용 테스트.
- `scripts/`: 로컬 테스트 실행 스크립트.
- `.github/workflows/ci.yml`: GitHub Actions 단위 테스트 workflow.
- `docs/`: 테스트 기준, TC 분류, 컨벤션 문서.

## 테스트 설계 규칙

항상 테스트 기준을 먼저 확인한 뒤 TC를 작성한다.

TC는 반드시 대분류와 소분류에 연결한다.

각 TC는 테스트 베이시스, 테스트 조건, 사전조건, 절차, 기대결과, evidence를 가진다.

실패를 제품 버그로 단정하기 전에 실행 환경, 테스트 코드, 관찰 근거 부족 여부를 구분한다.

## 이번 프로젝트의 제한

초기 단계에서는 하네스 엔지니어링과 루프 엔지니어링을 적용하지 않는다.

먼저 일반 Python 자동화 QA로 실행, 화면, 입력, evidence 수집을 구현한다.

반복 코드나 불안정한 대기가 늘어나는 시점에 하네스와 루프의 필요성을 문서로 비교한다.

## 검증 명령

```bash
pytest
```

실제 Steam 게임을 실행하는 테스트는 별도 표시를 두고, 기본 단위 테스트와 분리한다.

CI에서는 실제 Steam 게임을 실행하지 않는다.

CI는 의존성 설치, import 오류, 기본 유틸 테스트를 확인하는 범위로 제한한다.

로컬 Steam 테스트 실행 명령은 다음과 같다.

```bash
$env:SHEEPY_RUN_STEAM_TESTS = "1"
pytest tests/local
```

Windows PowerShell에서는 다음 스크립트로 같은 흐름을 실행할 수 있다.

```powershell
.\scripts\run_local_steam_tests.ps1
```

개별 TC는 다음 스크립트로 하나씩 실행한다.

```powershell
.\scripts\run_tc_001_steam_environment.ps1
.\scripts\run_tc_002_sheepy_launch.ps1
.\scripts\run_tc_003_process_detection.ps1
.\scripts\run_tc_004_initial_screenshot.ps1
```
