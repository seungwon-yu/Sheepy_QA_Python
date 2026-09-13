# 2026-09-13 개편 전 실행·진행 이력

이 문서는 과거 기록이다. 현재 구현·판정·통과 상태의 근거로 사용하지 않는다. 당시 판단값은 재해석하거나 현재 결과로 변환하지 않았다. 이전 문서의 상대 경로는 당시 docs/ 위치 기준이다.


---

## 원본: progress.md

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

### Sprint 7: 플레이어 상태, 세이브 보존, 기본 플레이 흐름

- TC-013 최초 실행 유저 상태 식별을 구현했다.
- TC-014 기존 플레이 유저 상태 식별을 구현했다.
- TC-015 세이브 상태 보존 확인을 구현했다.
- TC-016 기본 이동/점프 플레이 흐름을 구현했다.
- `src/sheepy_qa/player_state.py`에서 로비 CTA 신호를 기준으로 `PLAYER_NEW`, `PLAYER_RETURNING`, `PLAYER_UNKNOWN`을 분류한다.
- `src/sheepy_qa/save_data.py`에서 Sheepy 관련 저장 파일 후보를 비파괴적으로 스냅샷하고, 관찰 전후 누락 여부를 비교한다.
- `src/sheepy_qa/gameplay_flow.py`에서 플레이 화면 후보 상태와 입력 전후 이미지 변화량을 기준으로 기본 플레이 흐름을 요약한다.
- 각 TC는 개별 PowerShell 스크립트로 실행할 수 있게 분리했다.

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

1. TC-001 Steam 실행 환경 감지 로직 개선
2. `ensurePostLanguageScreen()` helper 추가
3. `ensureLobbyScreen()` 또는 로비 진입 복구 helper 추가
4. TC-013, TC-014의 세이브 상태별 실행 절차 분리
5. TC-016의 플레이 화면 진입 사전조건 자동 준비
6. Sprint 4 입력 TC가 상태 오염 없이 반복 실행되도록 사전조건 복구 또는 하네스 필요성 검토

## 미해결 TC 후속 작업

| TC | 현재 상태 | 후속 작업 |
| --- | --- | --- |
| TC-001 | `FAIL` | Steam 기본 설치 경로와 실행 중인 Steam 프로세스만 보지 말고, `steam://` URL protocol 등록 여부 또는 AppID 실행 가능 신호까지 Steam 환경 evidence에 포함한다. |
| TC-006 | `XFAIL / REVIEW_REQUIRED` | 기본 액션 입력 전 `POST_LANGUAGE_SCREEN` 사전조건을 자동으로 준비하거나, 현재 화면이 전환 중 `BLACK_SCREEN`이면 재대기 후 재캡처한다. |
| TC-010 | `XFAIL / REVIEW_REQUIRED` | 로비 CTA가 보일 때까지 언어 선택 이후 화면과 로비 화면을 준비하는 `ensureLobbyScreen()` helper를 추가한다. |
| TC-011 | `XFAIL / REVIEW_REQUIRED` | 이동 입력 전 `POST_LANGUAGE_SCREEN` 사전조건을 독립적으로 준비해 TC-018 실행 결과에 의존하지 않게 한다. |
| TC-013 | 구현 완료, 현재 `XFAIL / REVIEW_REQUIRED` | 최초 실행 유저 전용 실행 절차를 분리한다. 세이브 파일을 직접 삭제하지 않는 방침을 유지하면서, 별도 테스트 계정 또는 깨끗한 세이브 상태에서 실행하는 기준을 문서화한다. |
| TC-014 | 구현 완료, 현재 `XFAIL / REVIEW_REQUIRED` | 기존 플레이 유저 전용 실행 절차를 분리한다. Continue CTA가 관찰 가능한 로비 상태를 사전조건으로 준비한다. |
| TC-016 | 구현 완료, 현재 `XFAIL / REVIEW_REQUIRED` | 플레이 화면 후보 상태까지 진입한 뒤 이동/점프 입력을 수행하도록 로비 진입과 플레이 진입 helper를 연결한다. |
| TC-018 | `XFAIL / REVIEW_REQUIRED` | 언어 선택 직후 또는 화면 전환 중 발생하는 `BLACK_SCREEN`을 즉시 최종 판정하지 않고, 제한 시간 동안 재캡처 후 판단한다. |
| TC-019 | `XFAIL / REVIEW_REQUIRED` | 로비 CTA 후보 영역 분석 전에 로비 화면 사전조건을 준비하고, UI 배치 변경 시 후보 영역 기준을 재검토한다. |

현재 `REVIEW_REQUIRED`는 제품 결함 단정이 아니라 사전조건 또는 관찰 조건 부족을 의미한다. 후속 작업에서는 PASS를 만들기 위해 assertion을 완화하지 않고, 테스트가 필요한 화면 상태를 안정적으로 준비하도록 개선한다.

## 별도 문서 작업 후보

- Markdown 실행 요약 리포트 생성은 제품 동작을 검증하는 TC가 아니므로 TC 번호에서 제외하고 문서/리포트 작업으로 관리한다.

## 포트폴리오 문서 보강

- `README.md`에 포트폴리오에서 먼저 볼 문서, 대표 산출물 구조, Python 가상환경 실행 기준을 추가했다.
- `docs/evidence-samples.md`에 TC-010, TC-019, TC-012 대표 evidence와 judgement 해석 예시를 정리했다.
- `docs/local-environment.md`에 Windows PowerShell 기준 `.venv` 생성, `python -m pytest` 실행, Steam 로컬 테스트 조건, Python PATH 문제 해결 기준을 정리했다.

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

---

## 원본: evidence-samples.md

# Evidence 샘플

## 목적

이 문서는 `artifacts/evidence/`에 생성되는 로컬 실행 산출물이 어떤 의미를 가지는지 빠르게 보여주기 위한 샘플 문서이다.

`artifacts/`는 실행 PC의 Steam 상태, 화면 해상도, 실행 시각에 따라 달라지는 로컬 결과물이므로 저장소에는 포함하지 않는다. 대신 이 문서에 대표 TC의 evidence 구조와 판단 근거 예시를 남긴다.

## 공통 evidence 구조

각 TC는 가능한 경우 독립 실행 폴더를 생성한다.

```text
artifacts/evidence/<timestamp>-TC-xxx/
├─ judgement.json
├─ process-state.json
├─ execution-log.json
├─ screen-analysis.json
├─ image-diff.json
├─ foreground-window.json
└─ *.png
```

모든 TC가 모든 파일을 저장하지는 않는다. 예를 들어 프리즈 감지는 `freeze-summary.json`과 연속 screenshot을 저장하고, 입력 반응 테스트는 입력 전후 screenshot과 image diff를 저장한다.

## judgement.json 기준

`judgement.json`은 자동화 결과를 단순 PASS/FAIL로만 남기지 않고 아래 조건을 분리한다.

| 항목 | 의미 |
| --- | --- |
| `actionPerformed` | 자동화가 의도한 동작을 실제로 수행했는지 |
| `expectedSignals` | 기대결과를 지지하는 관찰 신호 |
| `forbiddenSignals` | 발생하면 안 되는 이상 신호 |
| `blockingConditions` | 제품 결함 판단 전에 만족해야 하는 사전조건 |
| `judgementBasis` | 사람이 읽는 판단 근거 요약 |

사전조건이나 관찰 근거가 부족하면 제품 결함으로 단정하지 않고 `REVIEW_REQUIRED`로 기록한다.

## 대표 샘플 1: TC-010 플레이 화면 진입

목적: 로비 CTA에서 Enter 입력 후 플레이 화면 후보로 전환되는지 확인한다.

대표 evidence:

```text
before-gameplay-entry.png
after-gameplay-entry.png
before-lobby-menu-analysis.json
after-lobby-menu-analysis.json
transition-diff.json
gameplay-screen.json
entry-input-log.json
judgement.json
```

대표 판단값:

```json
{
  "result": "PASS",
  "expectedResult": "GAMEPLAY_SCREEN_CANDIDATE",
  "actualResult": "GAMEPLAY_SCREEN_CANDIDATE",
  "actionPerformed": true
}
```

핵심 근거:

| 기준 | 기대 | 실제 |
| --- | --- | --- |
| 로비 진입 CTA 표시 | Continue 또는 Start Your Journey | `LOBBY_MENU_WITH_CONTINUE_AND_START` |
| 입력 후 플레이 화면 후보 | `GAMEPLAY_SCREEN_CANDIDATE` | `GAMEPLAY_SCREEN_CANDIDATE` |
| 로비 대비 화면 변화량 | `changedPixelRatio >= 0.05` | `0.5194` |
| 언어 선택 화면 잔류 | false | false |
| 검은 화면 지속 | false | false |

해석:

```text
로비 CTA가 사라졌고 입력 전후 화면 변화와 충분한 시각 정보가 관찰되었다.
```

## 대표 샘플 2: TC-019 로비 CTA 상태

목적: 언어 선택 이후 로비 화면에서 Continue와 Start Your Journey 후보 영역이 관찰되는지 확인한다.

대표 evidence:

```text
lobby-menu.png
screen-analysis.json
language-screen-analysis.json
post-language-screen.json
lobby-menu-analysis.json
judgement.json
```

대표 판단값:

```json
{
  "result": "PASS",
  "expectedResult": "LOBBY_MENU_WITH_CONTINUE_AND_START",
  "actualResult": "LOBBY_MENU_WITH_CONTINUE_AND_START",
  "actionPerformed": true
}
```

핵심 근거:

| 기준 | 기대 | 실제 |
| --- | --- | --- |
| 언어 선택 이후 화면 상태 | `POST_LANGUAGE_SCREEN` | `POST_LANGUAGE_SCREEN` |
| Continue CTA 표시 | true | true |
| Start Your Journey CTA 표시 | true | true |
| 언어 선택 화면 잔류 | false | false |
| 검은 화면 지속 | false | false |

해석:

```text
Continue와 Start Your Journey 후보 영역에서 메뉴 텍스트 신호가 모두 관찰되었다.
```

## 대표 샘플 3: TC-012 프리즈 감지

목적: 일정 시간 동안 연속 screenshot을 비교해 화면이 멈춘 것으로 볼 근거가 있는지 확인한다.

대표 evidence:

```text
freeze-sample-00.png
freeze-sample-01.png
freeze-sample-02.png
freeze-sample-03.png
freeze-diff-00-01.json
freeze-diff-01-02.json
freeze-diff-02-03.json
freeze-summary.json
final-process-state.json
judgement.json
```

대표 판단값:

```json
{
  "comparisonCount": 3,
  "visibleChangeCount": 3,
  "maxChangedPixelRatio": 0.0062,
  "averageChangedPixelRatio": 0.0043,
  "resultState": "FREEZE_NOT_DETECTED"
}
```

핵심 근거:

| 기준 | 기대 | 실제 |
| --- | --- | --- |
| 비교 가능한 screenshot 쌍 | 1개 이상 | 3 |
| 관찰 중 화면 변화 | `visibleChangeCount >= 1` | 3 |
| 프로세스 종료 | false | false |
| Sheepy process detected | true | true |
| Sheepy window detected | true | true |

해석:

```text
연속 screenshot 비교에서 화면 변화가 관찰되어 프리즈로 판단하지 않는다.
```

## 이미지 기반 판정의 방어 논리

이 프로젝트는 실제 Steam 게임을 외부에서 관찰하는 방식이므로, 내부 좌표나 UI 텍스트를 완전히 읽지 못한다.

따라서 이미지 기반 판정은 제품 결함을 단정하는 단독 근거가 아니라, 아래 조건과 함께 해석한다.

- 게임 프로세스가 살아 있는가
- 대상 게임 창을 찾았는가
- foreground window가 테스트 대상인가
- screenshot이 저장되었는가
- 기대 신호와 이상 신호가 분리되어 기록되었는가
- 근거가 부족할 때 `REVIEW_REQUIRED`로 빠지는가

면접에서는 “픽셀 변화만으로 충분하다”가 아니라, “외부 관찰 자동화의 한계를 인정하고 오판을 줄이기 위해 사전조건, 기대 신호, 이상 신호, 검토 필요 상태를 분리했다”라고 설명하는 것이 좋다.
