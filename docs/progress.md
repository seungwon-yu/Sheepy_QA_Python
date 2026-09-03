# 진행 상황

## 목적

이 문서는 프로젝트를 이어서 작업할 때 현재 완료된 범위와 다음 작업을 빠르게 확인하기 위한 기록이다.

상세 기준은 `docs/test-basis-and-standards.md`, TC 분류는 `docs/test-classification.md`, Sprint 순서는 `docs/sprint-plan.md`를 따른다.

## 완료된 작업

### 프로젝트 초기 구조

- Python 기반 자동화 QA 프로젝트 구조를 생성했다.
- `pytest`, `Pillow`, `psutil` 기반의 기본 의존성을 설정했다.
- GitHub Actions CI를 추가해 기본 단위 테스트와 import 오류를 확인하도록 했다.
- 실제 Steam 게임 실행 테스트는 CI가 아니라 로컬 전용 테스트로 분리했다.

### 테스트 기준과 TC 분류

- ISTQB CTFL Foundation 기준으로 테스트 베이시스, 테스트 조건, 기대결과, evidence 중심의 TC 작성 방식을 정리했다.
- ISTQB CTFL Game Testing 기준으로 게임 QA 대분류를 설치/실행 환경, 실행/종료, 메인 화면, 입력 반응, 기본 플레이, 화면/그래픽, 안정성, evidence/리포트로 나누었다.
- 각 TC가 어느 대분류와 소분류에 연결되는지 추적 매트릭스로 정리했다.

### Sprint 1: 실행 환경과 초기 진입

- TC-001 Steam 실행 환경 확인을 구현했다.
- TC-002 Sheepy AppID 실행 시도를 구현했다.
- TC-003 게임 프로세스 감지를 구현했다.
- TC-004 초기 화면 스크린샷 저장을 구현했다.
- TC-001부터 TC-004까지 `judgement.json`을 저장해 테스트 동작, 기대 신호, 이상 신호를 분리해서 기록한다.
- 각 TC를 개별 PowerShell 스크립트로 실행할 수 있게 분리했다.

### Sprint 2: 화면 상태 판별

- TC-005 검은 화면 여부 확인을 구현했다.
- `src/sheepy_qa/image_analysis.py`에서 screenshot의 평균 밝기, 어두운 픽셀 비율, 샘플 색상 수를 분석한다.
- `screen-state.json`에 기대결과, 실제결과, 판단 근거, 분석 값을 함께 저장한다.
- `judgement.json`에 화면 상태 판별의 기대 신호와 검은 화면 지속 여부를 함께 기록한다.
- Sprint 2 전체 실행 스크립트 `scripts/run_sprint_2_screen_state.ps1`를 추가했다.

### Sprint 3: 언어 선택 화면과 선택 입력

- TC-009 언어 선택 화면 도달 확인을 구현했다.
- TC-017 언어 선택 입력 반응 확인을 구현했다.
- 언어 선택 화면 판별은 중앙 영역의 언어 선택 항목, 어두운 배경, 채도 있는 색상 블록을 기준으로 한다.
- 입력 반응은 Enter 입력 전후 screenshot 차이를 비교해 판단한다.
- `foreground-window.json`을 저장해 입력이 어느 창을 대상으로 수행되었는지 확인할 수 있게 했다.
- `judgement.json`을 저장해 테스트 동작 수행 여부, 기대 신호, 이상 신호, 차단 조건을 분리해서 기록한다.
- `scripts/run_sprint_3_language_selection.ps1`로 Sprint 3만 별도 실행할 수 있게 했다.

### Sprint 4: 언어 선택 이후 화면과 입력 반응

- TC-018 언어 선택 이후 화면 상태 확인을 구현했다.
- TC-019 로비 CTA 버튼 상태 확인을 구현했다.
- TC-006 기본 액션 입력 반응 확인을 구현했다.
- TC-011 이동 입력 반응 확인을 구현했다.
- `src/sheepy_qa/post_language_screen.py`에서 언어 선택 이후 화면을 `POST_LANGUAGE_SCREEN`, `LANGUAGE_SELECTION_SCREEN`, `BLACK_SCREEN`, `REVIEW_REQUIRED`로 분류한다.
- `src/sheepy_qa/lobby_menu.py`에서 Continue와 Start Your Journey 후보 영역의 메뉴 텍스트 신호를 분석한다.
- 입력 반응은 무입력 대기 변화량과 입력 후 변화량을 분리해서 비교한다.
- `foreground-window.json`을 저장해 입력 대상이 Sheepy 창인지 확인한다.
- `idle-diff.json`, `input-diff.json`, `input-log.json`을 저장해 입력 반응 판단 근거를 남긴다.
- `scripts/run_sprint_4_input_response.ps1`로 Sprint 4만 별도 실행할 수 있게 했다.
- Space 입력은 화면을 다음 상태로 진행시킬 수 있으므로 Sprint 4 통합 실행에서는 TC-006을 마지막에 둔다.

### Sprint 5: 기본 플레이 진입

- TC-010 로비 CTA를 통한 플레이 화면 진입 확인을 구현했다.
- `src/sheepy_qa/gameplay_screen.py`에서 입력 후 화면을 `GAMEPLAY_SCREEN_CANDIDATE`, `LOBBY_MENU_SCREEN`, `LANGUAGE_SELECTION_SCREEN`, `BLACK_SCREEN`, `REVIEW_REQUIRED`로 분류한다.
- 로비 CTA가 입력 후 사라졌는지, 로비 대비 화면 변화량이 충분한지, 언어 선택 화면이나 검은 화면이 아닌지를 판단 근거로 기록한다.
- 현재 선택된 CTA에 Enter를 보내므로 `Continue` 선택 상태에서는 기존 플레이 유저 흐름으로 진입할 수 있다.

### Sprint 6: 안정성 관찰

- TC-007 짧은 실행 안정성 확인을 구현했다.
- TC-012 프리즈 감지를 구현했다.
- `src/sheepy_qa/stability.py`에서 관찰 샘플을 요약해 `STABLE_SHORT_RUN`, `PROCESS_EXITED_DURING_OBSERVATION`, `SCREENSHOT_CAPTURE_UNSTABLE`, `REVIEW_REQUIRED`로 분류한다.
- `src/sheepy_qa/freeze_detection.py`에서 연속 screenshot 비교 결과를 요약해 `FREEZE_NOT_DETECTED` 또는 `REVIEW_REQUIRED`로 분류한다.
- 30초 동안 주기적으로 Sheepy 프로세스 유지 여부와 screenshot 저장 여부를 기록한다.
- 프리즈 여부는 20초 동안 연속 screenshot을 저장하고 이미지 변화량을 비교해 판단한다.

### 플레이어 상태 분리 기준

- 최초 실행 유저와 기존 플레이 유저는 사전조건과 기대결과가 달라질 수 있으므로 별도 조건 축으로 분리했다.
- `docs/player-state-strategy.md`에 `PLAYER-NEW`, `PLAYER-RETURNING`, `PLAYER-UNKNOWN` 기준을 정리했다.
- 세이브 파일을 직접 수정하는 테스트는 사용자 데이터 손상 위험이 있으므로, 세이브 경로와 백업/복원 기준 확인 후 후속 Sprint에서 구현한다.

## 최근 검증 결과

기본 테스트:

```text
26 passed, 10 skipped
```

Sprint 1 로컬 테스트:

```text
4 passed
```

Sprint 2 로컬 테스트:

```text
1 passed
```

로컬 Steam smoke 테스트:

```text
5 passed
```

Sprint 3 로컬 테스트:

```text
2 passed
```

Sprint 4 로컬 테스트:

```text
첫 실행: 2 passed, 1 xfailed
재실행: 3 xfailed
TC-019 개별 실행: 1 passed
```

TC-010 로컬 테스트:

```text
1 passed
```

TC-007 로컬 테스트:

```text
1 passed
```

TC-012 로컬 테스트:

```text
1 passed
```

Sprint 4 결과 해석:

- `TC-018`은 언어 선택 이후 화면이 관찰되었을 때 PASS했다.
- `TC-006`은 Space 입력 후 무입력 대비 화면 변화량이 커서 PASS했다.
- `TC-019`는 현재 로비 화면에서 Continue와 Start Your Journey가 모두 관찰되어 PASS했다.
- `TC-011`은 앞선 Space 입력 이후 화면 상태가 바뀌어 사전조건이 맞지 않아 `REVIEW_REQUIRED`로 기록되었다.
- 재실행 시 현재 화면이 다시 언어 선택 화면으로 분류되어 TC-018, TC-011, TC-006 모두 `REVIEW_REQUIRED`로 기록되었다.
- 이 결과는 하네스 없이 일반 자동화로 진행할 때 테스트 간 상태 오염과 사전조건 관리가 중요하다는 근거로 사용한다.

TC-010 결과 해석:

- 입력 전 로비 상태는 `LOBBY_MENU_WITH_CONTINUE_AND_START`였다.
- 선택된 진입 CTA 힌트는 `Continue`였고, 플레이어 상태 힌트는 `PLAYER-RETURNING`이었다.
- Enter 입력 후 로비 CTA가 사라졌고, 화면 변화량 `0.5194`가 관찰되어 `GAMEPLAY_SCREEN_CANDIDATE`로 PASS했다.

TC-007 결과 해석:

- 30초 관찰 동안 5개 샘플이 저장되었다.
- 모든 샘플에서 Sheepy 프로세스가 유지되었다.
- 모든 샘플에서 screenshot 저장이 성공했다.
- 비정상 종료 또는 캡처 실패 샘플은 0개였다.

TC-012 결과 해석:

- 20초 관찰 동안 4장 screenshot이 저장되었다.
- 비교 가능한 screenshot 쌍 3개가 생성되었다.
- 3개 비교쌍 모두 화면 변화가 관찰되어 `FREEZE_NOT_DETECTED`로 PASS했다.
- 최대 변화량은 `0.0062`, 평균 변화량은 `0.0043`이었다.

TC-009 실행 evidence:

```text
artifacts/evidence/2026-09-03T10-03-26.098+00-00-TC-009
```

TC-017 실행 evidence:

```text
artifacts/evidence/2026-09-03T10-03-31.449+00-00-TC-017
```

최신 Sprint 1~3 실행 evidence:

```text
artifacts/evidence/2026-09-03T12-40-27.744+00-00-TC-001
artifacts/evidence/2026-09-03T12-40-30.511+00-00-TC-002
artifacts/evidence/2026-09-03T12-40-30.528+00-00-TC-003
artifacts/evidence/2026-09-03T12-40-32.102+00-00-TC-004
artifacts/evidence/2026-09-03T12-40-41.509+00-00-TC-005
artifacts/evidence/2026-09-03T12-40-54.232+00-00-TC-009
artifacts/evidence/2026-09-03T12-41-00.046+00-00-TC-017
```

Sprint 4 실행 evidence:

```text
artifacts/evidence/2026-09-03T12-58-12.753+00-00-TC-018
artifacts/evidence/2026-09-03T12-58-16.627+00-00-TC-006
artifacts/evidence/2026-09-03T12-58-22.702+00-00-TC-011
artifacts/evidence/2026-09-03T13-01-54.948+00-00-TC-018
artifacts/evidence/2026-09-03T13-01-59.149+00-00-TC-011
artifacts/evidence/2026-09-03T13-02-03.651+00-00-TC-006
artifacts/evidence/2026-09-03T13-10-38.635+00-00-TC-019
artifacts/evidence/2026-09-03T13-21-42.859+00-00-TC-010
artifacts/evidence/2026-09-03T13-25-25.308+00-00-TC-007
artifacts/evidence/2026-09-03T13-32-09.410+00-00-TC-012
```

공통 저장 파일:

- 모든 구현 TC는 `judgement.json`을 저장한다.
- TC별로 `process-state.json`, `execution-log.json`, screenshot, image analysis, image diff 등이 함께 저장된다.
- `judgement.json`은 테스트 동작 수행 여부, 기대 신호, 이상 신호, 차단 조건을 분리해서 기록한다.

## 다음 작업 후보

1. TC-008 실패 evidence 저장 확인 구현
2. TC-013, TC-014, TC-015로 최초 실행 유저와 기존 플레이 유저 상태 분리
3. TC-016 기본 이동/점프 플레이 흐름 구현
4. Sprint 4 입력 TC가 상태 오염 없이 반복 실행되도록 사전조건 복구 또는 하네스 필요성 검토

## 별도 문서 작업 후보

- Markdown 실행 요약 리포트 생성은 제품 동작을 검증하는 TC가 아니므로 TC 번호에서 제외하고 문서/리포트 작업으로 관리한다.

## 현재 주의할 점

- TC-005는 전체 화면 screenshot을 분석하므로 게임 창이 다른 창에 가려지면 판단이 부정확할 수 있다.
- TC-009와 TC-017은 Sheepy 창 탐지 후 창 단독 screenshot 캡처를 우선 사용한다.
- TC-018, TC-006, TC-011은 언어 선택 이후 화면을 사전조건으로 하며, 언어 선택 화면이 다시 감지되면 `REVIEW_REQUIRED`로 기록한다.
- TC-019는 OCR 없이 후보 영역의 이미지 신호로 Continue와 Start Your Journey를 판별하므로 UI 배치 변경 시 기준 재검토가 필요하다.
- TC-010은 플레이 화면 후보 진입까지만 확인하며, 실제 조작 가능 여부는 후속 TC에서 확인한다.
- TC-007은 크래시와 캡처 실패 중심의 안정성 테스트이며, 프리즈 판정은 아직 포함하지 않는다.
- TC-012는 이미지 변화 기반 프리즈 감지이므로 내부 렌더 상태나 FPS를 직접 확인하지 않는다.
- 아직 UI 텍스트 OCR, 메인 메뉴 판별, 세이브 상태별 분리 자동화는 구현하지 않았다.
- 하네스와 루프는 아직 적용하지 않는다. 반복 코드와 불안정한 대기가 누적되는 시점에 필요성을 비교한다.
