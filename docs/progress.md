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
- TC-006 기본 액션 입력 반응 확인을 구현했다.
- TC-011 이동 입력 반응 확인을 구현했다.
- `src/sheepy_qa/post_language_screen.py`에서 언어 선택 이후 화면을 `POST_LANGUAGE_SCREEN`, `LANGUAGE_SELECTION_SCREEN`, `BLACK_SCREEN`, `REVIEW_REQUIRED`로 분류한다.
- 입력 반응은 무입력 대기 변화량과 입력 후 변화량을 분리해서 비교한다.
- `foreground-window.json`을 저장해 입력 대상이 Sheepy 창인지 확인한다.
- `idle-diff.json`, `input-diff.json`, `input-log.json`을 저장해 입력 반응 판단 근거를 남긴다.
- `scripts/run_sprint_4_input_response.ps1`로 Sprint 4만 별도 실행할 수 있게 했다.
- Space 입력은 화면을 다음 상태로 진행시킬 수 있으므로 Sprint 4 통합 실행에서는 TC-006을 마지막에 둔다.

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
```

Sprint 4 결과 해석:

- `TC-018`은 언어 선택 이후 화면이 관찰되었을 때 PASS했다.
- `TC-006`은 Space 입력 후 무입력 대비 화면 변화량이 커서 PASS했다.
- `TC-011`은 앞선 Space 입력 이후 화면 상태가 바뀌어 사전조건이 맞지 않아 `REVIEW_REQUIRED`로 기록되었다.
- 재실행 시 현재 화면이 다시 언어 선택 화면으로 분류되어 TC-018, TC-011, TC-006 모두 `REVIEW_REQUIRED`로 기록되었다.
- 이 결과는 하네스 없이 일반 자동화로 진행할 때 테스트 간 상태 오염과 사전조건 관리가 중요하다는 근거로 사용한다.

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
```

공통 저장 파일:

- 모든 구현 TC는 `judgement.json`을 저장한다.
- TC별로 `process-state.json`, `execution-log.json`, screenshot, image analysis, image diff 등이 함께 저장된다.
- `judgement.json`은 테스트 동작 수행 여부, 기대 신호, 이상 신호, 차단 조건을 분리해서 기록한다.

## 다음 작업 후보

1. TC-007 짧은 실행 안정성 확인 구현
2. TC-012 프리즈 감지 구현
3. 사람이 보기 좋은 Markdown 실행 요약 리포트 생성 검토
4. TC-014, TC-015, TC-016으로 최초 실행 유저와 기존 플레이 유저 상태 분리
5. Sprint 4 입력 TC가 상태 오염 없이 반복 실행되도록 사전조건 복구 또는 하네스 필요성 검토

## 현재 주의할 점

- TC-005는 전체 화면 screenshot을 분석하므로 게임 창이 다른 창에 가려지면 판단이 부정확할 수 있다.
- TC-009와 TC-017은 Sheepy 창 탐지 후 창 단독 screenshot 캡처를 우선 사용한다.
- TC-018, TC-006, TC-011은 언어 선택 이후 화면을 사전조건으로 하며, 언어 선택 화면이 다시 감지되면 `REVIEW_REQUIRED`로 기록한다.
- 아직 UI 텍스트 OCR, 메인 메뉴 판별, 세이브 상태별 분리 자동화는 구현하지 않았다.
- 하네스와 루프는 아직 적용하지 않는다. 반복 코드와 불안정한 대기가 누적되는 시점에 필요성을 비교한다.
