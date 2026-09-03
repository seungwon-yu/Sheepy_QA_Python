# Sheepy_QA_Python

Steam 게임 `Sheepy: A Short Adventure`를 대상으로 Python 기반 자동화 QA를 연습하는 프로젝트입니다.

이번 프로젝트는 처음부터 하네스 엔지니어링이나 루프 엔지니어링을 적용하지 않고, 먼저 일반적인 자동화 QA 방식으로 테스트 기준과 TC를 설계합니다.

이후 자동화가 반복되거나 실패 분석이 복잡해지는 지점을 확인한 뒤, 하네스 또는 루프 엔지니어링이 필요한지 비교하는 것을 목표로 합니다.

## 프로젝트 기준

이 프로젝트의 테스트 설계 기준은 다음 두 문서를 함께 사용합니다.

- ISTQB CTFL Foundation Level: 테스트 설계 절차, 테스트 베이시스, 테스트 조건, 테스트 케이스, 기대결과, 실행 결과 기준
- ISTQB CTFL Game Testing: 게임 QA 특화 리스크, 게임 메커닉, 그래픽, 사운드, 레벨, 컨트롤러, 로컬라이제이션 기준

상세 기준은 `docs/test-basis-and-standards.md`에 정리합니다.

## 현재 목표

```text
실제 Steam 게임
↓
Python 자동화 QA
↓
테스트 기준 수립
↓
TC 대분류/소분류 설계
↓
실행/화면/입력/evidence 중심 테스트
↓
하네스와 루프 필요성 비교
```

## 문서 구조

- `AGENTS.md`: 다음 작업자가 먼저 읽을 프로젝트 지도
- `docs/test-basis-and-standards.md`: 테스트 기준과 적용 원칙
- `docs/test-classification.md`: TC 대분류와 소분류 기준
- `docs/test-cases.md`: 전체 TC 목록과 상세 분류
- `docs/traceability-matrix.md`: 기준, 대분류, 소분류, TC 연결표
- `docs/guardrails.md`: 테스트 수행 원칙과 제한사항
- `docs/sprint-plan.md`: Sprint별 자동화 진행 순서와 개별 실행 단위
- `docs/sprint-strategy.md`: Sprint를 나눈 기준과 ISTQB 연결 근거
- `docs/player-state-strategy.md`: 최초 실행 유저와 기존 플레이 유저 분리 기준
- `docs/judgement-basis.md`: PASS/FAIL/REVIEW_REQUIRED 판단 근거 기록 기준
- `docs/progress.md`: 현재 완료 범위와 다음 작업 후보
- `docs/code-convention.md`: 코드 작성 컨벤션
- `docs/commit-convention.md`: 커밋 메시지 컨벤션
- `docs/ci.md`: CI 범위와 로컬 QA 범위 구분

## 프로젝트 구조

```text
Sheepy_QA_Python/
├─ src/
│  └─ sheepy_qa/
│     ├─ config.py
│     ├─ steam_app.py
│     ├─ steam_environment.py
│     ├─ process_check.py
│     ├─ screen_capture.py
│     ├─ image_analysis.py
│     ├─ language_screen.py
│     ├─ post_language_screen.py
│     ├─ image_diff.py
│     ├─ keyboard_input.py
│     ├─ window_state.py
│     ├─ judgement.py
│     ├─ wait.py
│     ├─ local_test_config.py
│     └─ evidence.py
├─ tests/
│  ├─ unit/
│  └─ local/
├─ docs/
├─ .github/
│  └─ workflows/
│     └─ ci.yml
├─ pyproject.toml
├─ pytest.ini
└─ requirements.txt
```

## 초기 TC 대분류

| 대분류 | 목적 |
| --- | --- |
| 설치 및 실행 환경 | Steam, OS, 게임 설치, 실행 가능 상태 확인 |
| 실행/종료 | 게임 프로세스 시작과 종료 확인 |
| 메인 화면 및 초기 진입 | 초기 화면 도달과 기본 UI 확인 |
| 입력 반응 | 키보드 입력에 대한 반응 확인 |
| 기본 플레이 흐름 | 새 게임 시작 후 기본 이동/점프 흐름 확인 |
| 화면/그래픽 표시 | 화면 깨짐, 검은 화면, UI 표시 문제 확인 |
| 안정성/크래시/프리즈 | 일정 시간 동안 중단 없이 동작하는지 확인 |
| Evidence 및 리포트 | 실패 시 증거와 실행 결과를 남기는지 확인 |

## 자동화 방향

초기 자동화는 다음 도구 후보를 기준으로 합니다.

- `pytest`: 테스트 실행
- `pyautogui` 또는 `pydirectinput`: 키보드/마우스 입력
- `Pillow`: 스크린샷 저장
- `opencv-python`: 화면 이미지 비교
- `psutil`: 프로세스 상태 확인

## 로컬 테스트

```bash
pip install -r requirements.txt
pytest
```

현재 단위 테스트는 실제 Steam 게임을 실행하지 않고, 실행 명령 생성, 프로세스 상태 판단, evidence 파일 저장 같은 기본 유틸을 먼저 검증합니다.

## 로컬 Steam 테스트

실제 Steam과 Sheepy 실행이 필요한 테스트는 기본 `pytest`에서는 skip됩니다.

로컬에서 실제 게임 테스트를 실행하려면 다음 조건이 필요합니다.

- Steam 설치
- Steam 로그인
- Sheepy 설치
- GUI 화면 세션

실행 명령:

```bash
$env:SHEEPY_RUN_STEAM_TESTS = "1"
pytest tests/local
```

또는 Windows PowerShell에서 아래 스크립트로 한 번에 실행할 수 있습니다.

```powershell
.\scripts\run_local_steam_tests.ps1
```

각 TC는 다음 스크립트로 하나씩 실행할 수 있습니다.

```powershell
.\scripts\run_tc_001_steam_environment.ps1
.\scripts\run_tc_002_sheepy_launch.ps1
.\scripts\run_tc_003_process_detection.ps1
.\scripts\run_tc_004_initial_screenshot.ps1
.\scripts\run_tc_005_black_screen_check.ps1
.\scripts\run_tc_009_language_selection_screen.ps1
.\scripts\run_tc_017_language_selection_input.ps1
.\scripts\run_tc_018_post_language_screen.ps1
.\scripts\run_tc_011_movement_input.ps1
.\scripts\run_tc_006_basic_action_input.ps1
```

Sprint 1 실행 환경과 초기 진입은 다음 스크립트로 실행합니다.

```powershell
.\scripts\run_sprint_1_initial_entry.ps1
```

Sprint 2 화면 상태 판별은 다음 스크립트로 실행합니다.

```powershell
.\scripts\run_sprint_2_screen_state.ps1
```

Sprint 3 언어 선택 화면과 선택 입력은 다음 스크립트로 실행합니다.

```powershell
.\scripts\run_sprint_3_language_selection.ps1
```

Sprint 4 언어 선택 이후 화면과 입력 반응은 다음 스크립트로 실행합니다.

```powershell
.\scripts\run_sprint_4_input_response.ps1
```

현재 로컬 Steam smoke 테스트는 `TC-001`부터 `TC-005`까지의 실행 환경, AppID 실행, 프로세스 감지, 초기 화면 screenshot 저장, 검은 화면 여부 확인을 대상으로 합니다.

`TC-017`은 실제 Enter 입력을 전송하므로 Sprint 3 스크립트 또는 개별 TC 스크립트로 명시적으로 실행합니다.

`TC-006`, `TC-011`은 실제 키보드 입력을 전송하므로 Sprint 4 스크립트 또는 개별 TC 스크립트로 명시적으로 실행합니다.

## CI

GitHub Actions CI는 실제 Steam 게임을 실행하지 않습니다.

CI는 Python 의존성 설치, import 오류, 기본 유틸 테스트가 깨지지 않았는지 확인하는 용도입니다.

실제 Sheepy 실행, 게임 화면 캡처, 키보드 입력 반응 확인은 로컬 QA에서 수행합니다.

## 현재 상태

문서 기반 테스트 설계와 Python 자동화 기본 구조를 작성한 상태입니다.

실제 Steam 실행이 필요한 `TC-001`부터 `TC-005`, `TC-009`, `TC-017`, `TC-018`, `TC-006`, `TC-011`까지는 로컬 전용 pytest 테스트로 분리해 구현했습니다.
