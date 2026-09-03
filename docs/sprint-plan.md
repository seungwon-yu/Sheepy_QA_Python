# Sprint 진행 계획

## 목적

이 문서는 Sheepy 자동화 QA를 한 번에 크게 구현하지 않고, 작은 자동화 단위로 나누어 진행하기 위한 계획이다.

실제 Steam 게임 자동화는 실행 환경, 창 포커스, 화면 상태, 입력 반응에 따라 실패 원인이 달라질 수 있다.

따라서 게임 진입부터 게임 진행까지 한 번에 묶지 않고, 각 Sprint와 TC를 독립적으로 실행할 수 있게 나눈다.

Sprint를 나눈 상세 기준은 `docs/sprint-strategy.md`에 정리한다.

## 진행 원칙

1. 한 Sprint는 하나의 주요 QA 목적을 가진다.
2. 한 TC는 하나의 주요 기대결과를 가진다.
3. 앞 단계가 불안정하면 다음 단계로 넘어가지 않는다.
4. 실패하면 제품 문제로 단정하지 않고 evidence를 먼저 확인한다.
5. 하네스와 루프는 초기 Sprint에 넣지 않고, 일반 자동화의 한계를 확인한 뒤 비교 대상으로 도입한다.
6. 최초 실행 유저와 기존 플레이 유저처럼 사전조건과 기대결과가 달라지는 경우 플레이어 상태를 별도 조건으로 기록한다.
7. 모든 구현 TC는 `judgement.json`에 테스트 동작 수행 여부, 기대 신호, 이상 신호, 차단 조건을 분리해 기록한다.

## Sprint 1: 실행 환경과 초기 진입

목표: 자동화가 Steam과 Sheepy를 실행하고 관찰할 수 있는 최소 조건을 확인한다.

| 순서 | TC | 실행 스크립트 | 목적 |
| --- | --- | --- | --- |
| 1 | TC-001 Steam 실행 환경 확인 | `scripts/run_tc_001_steam_environment.ps1` | Steam 실행 가능 상태 확인 |
| 2 | TC-002 Sheepy AppID 실행 시도 | `scripts/run_tc_002_sheepy_launch.ps1` | `steam://run/1568400` 호출 확인 |
| 3 | TC-003 게임 프로세스 감지 | `scripts/run_tc_003_process_detection.ps1` | Sheepy 프로세스가 뜨는지 확인 |
| 4 | TC-004 초기 화면 스크린샷 저장 | `scripts/run_tc_004_initial_screenshot.ps1` | 화면 evidence 저장 가능 여부 확인 |

전체 Sprint 1 로컬 실행:

```powershell
.\scripts\run_sprint_1_initial_entry.ps1
```

Sprint 1 evidence 공통 항목:

- process-state.json 또는 screen-metadata.json
- judgement.json

## Sprint 2: 화면 상태 판별

목표: 단순 screenshot 저장을 넘어, 화면이 테스트 가능한 상태인지 판단한다.

후보 TC:

| TC | 대분류 | 목적 |
| --- | --- | --- |
| TC-005 검은 화면 여부 확인 | 화면/그래픽 표시 | screenshot이 검은 화면 상태인지 확인 |
| TC-009 메인 메뉴 진입 확인 | 메인 화면 및 초기 진입 | 초기 화면이 메뉴 또는 진행 가능한 화면인지 확인 |

예상 evidence:

- screenshot.png
- image-analysis.json
- screen-state.json
- judgement.json

현재 구현된 Sprint 2 실행:

```powershell
.\scripts\run_sprint_2_screen_state.ps1
```

개별 실행:

```powershell
.\scripts\run_tc_005_black_screen_check.ps1
```

주의: TC-005는 화면이 완전한 검은 화면인지 판별하는 테스트이다. 아직 메인 메뉴의 특정 로고, 버튼, 문구를 인식하는 테스트는 아니며, TC-009에서 별도 기준을 세운 뒤 확장한다.

## Sprint 3: 언어 선택 화면과 선택 입력

목표: 현재 관찰된 언어 선택 화면을 테스트 기준으로 정리하고, 언어 선택 입력 후 화면 전환이 발생하는지 확인한다.

후보 TC:

| TC | 대분류 | 목적 |
| --- | --- | --- |
| TC-009 언어 선택 화면 도달 확인 | 메인 화면 및 초기 진입 | 초기 진입 화면이 언어 선택 화면인지 확인 |
| TC-017 언어 선택 입력 반응 확인 | 입력 반응 | 언어 선택 입력 후 화면 전환 확인 |

예상 evidence:

- language-selection-screen.png
- screen-analysis.json
- language-screen-analysis.json
- before-language-input.png
- after-language-input.png
- image-diff.json
- input-log.json
- foreground-window.json
- judgement.json

플레이어 상태 기준:

- 언어 선택 화면이 최초 실행 유저에게만 나오는지 아직 확정하지 않는다.
- 초기 자동화는 `PLAYER-UNKNOWN`으로 실행하고, 반복 실행 결과와 세이브 데이터 기준을 확인한 뒤 `PLAYER-NEW` 전용 TC인지 결정한다.

전체 Sprint 3 로컬 실행:

```powershell
.\scripts\run_sprint_3_language_selection.ps1
```

개별 실행:

```powershell
.\scripts\run_tc_009_language_selection_screen.ps1
.\scripts\run_tc_017_language_selection_input.ps1
```

주의: `TC-017`은 실제 Enter 입력을 전송하므로 게임 창 포커스 상태를 evidence로 함께 저장한다.

판단 근거:

- 테스트 동작이 실제로 수행됐는지 기록한다.
- 언어 선택 화면 후보 개수, 어두운 배경 비율, 채도 픽셀 비율 같은 기대 신호를 기록한다.
- 검은 화면 지속, 입력 전후 동일 화면 같은 이상 신호를 기록한다.
- 사전조건이 부족하면 제품 FAIL로 단정하지 않고 REVIEW_REQUIRED로 남긴다.

## Sprint 4: 기본 입력 반응

목표: 언어 선택 이후 화면을 캡처하고, 그 화면에서 키보드 입력 전후 화면 변화가 있는지 확인한다.

후보 TC:

| TC | 대분류 | 목적 |
| --- | --- | --- |
| TC-018 언어 선택 이후 화면 상태 확인 | 메인 화면 및 초기 진입 | 언어 선택 완료 후 화면을 캡처하고 분류 |
| TC-019 로비 CTA 버튼 상태 확인 | 메인 화면 및 초기 진입 | Continue와 Start Your Journey 표시 여부 확인 |
| TC-006 기본 입력 반응 확인 | 입력 반응 | 점프 입력 전후 화면 변화 확인 |
| TC-011 이동 입력 반응 | 입력 반응 | 좌우 입력 전후 화면 변화 확인 |

예상 evidence:

- post-language-screen.png
- before-action-input.png, idle-action-input.png, after-action-input.png
- before-movement-input.png, idle-movement-input.png, after-movement-input.png
- screen-analysis.json
- language-screen-analysis.json
- post-language-screen.json
- lobby-menu-analysis.json
- idle-diff.json
- input-diff.json
- input-log.json
- foreground-window.json
- judgement.json

전체 Sprint 4 로컬 실행:

```powershell
.\scripts\run_sprint_4_input_response.ps1
```

개별 실행:

```powershell
.\scripts\run_tc_018_post_language_screen.ps1
.\scripts\run_tc_019_lobby_menu_options.ps1
.\scripts\run_tc_011_movement_input.ps1
.\scripts\run_tc_006_basic_action_input.ps1
```

주의:

- Sprint 4는 “언어 선택 이후 화면”을 사전조건으로 한다.
- TC-019는 로비 CTA 표시 상태를 확인하며, `Continue`와 `Start Your Journey`가 모두 보이면 기존 플레이 유저 가능성을 `PLAYER-RETURNING` 힌트로 기록한다.
- 현재 화면이 언어 선택 화면이면 제품 FAIL이 아니라 `REVIEW_REQUIRED`로 기록한다.
- Space 입력은 화면을 다음 상태로 진행시킬 수 있으므로 통합 실행에서는 TC-006을 마지막에 둔다.
- 이 Sprint는 하네스 없이 일반 자동화로 상태 오염 문제가 생길 수 있음을 관찰하는 기준점이 된다.

## Sprint 5: 기본 플레이 흐름

목표: 게임 시작 후 짧은 플레이 구간이 진행 가능한지 확인한다.

후보 TC:

| TC | 대분류 | 목적 |
| --- | --- | --- |
| TC-010 새 게임 시작 확인 | 기본 플레이 흐름 | 초기 화면에서 플레이 상태 진입 |
| 신규 TC 기본 이동 흐름 | 기본 플레이 흐름 | 짧은 이동/점프 조합 수행 |

## Sprint 5.5: 플레이어 상태 분리

목표: 최초 실행 유저와 기존 플레이 유저의 초기 진입 기대결과를 분리한다.

후보 TC:

| TC | 플레이어 상태 | 목적 |
| --- | --- | --- |
| TC-014 최초 실행 상태 식별 | PLAYER-NEW | 세이브 데이터가 없는 상태에서 첫 진입 흐름 확인 |
| TC-015 기존 플레이 상태 식별 | PLAYER-RETURNING | 세이브 데이터가 있는 상태에서 Continue 또는 진행 상태 표시 확인 |
| TC-016 세이브 상태 보존 확인 | PLAYER-RETURNING | 자동화 실행 후 기존 세이브 데이터 손상 여부 확인 |

주의: 이 Sprint는 세이브 파일 위치와 백업/복원 방식을 먼저 확인한 뒤 진행한다.

## Sprint 6: 안정성 관찰

목표: 일정 시간 동안 크래시 또는 프리즈가 발생하지 않는지 확인한다.

후보 TC:

| TC | 대분류 | 목적 |
| --- | --- | --- |
| TC-007 짧은 실행 안정성 확인 | 안정성/크래시/프리즈 | 30초 동안 프로세스 유지 확인 |
| TC-012 프리즈 감지 | 안정성/크래시/프리즈 | 화면 변화가 장시간 멈추는지 확인 |

## Sprint 7: Evidence와 리포트

목표: 각 TC 실행 결과를 사람이 읽기 좋은 형태로 정리한다.

후보 TC:

| TC | 대분류 | 목적 |
| --- | --- | --- |
| TC-008 실패 evidence 저장 확인 | Evidence 및 리포트 | 실패 시 evidence 파일 저장 확인 |
| TC-013 리포트 생성 | Evidence 및 리포트 | 실행 결과 요약 리포트 생성 |

## 하네스 적용 검토 시점

다음 문제가 반복되면 하네스 도입을 검토한다.

- Steam 실행, 대기, 프로세스 확인 코드가 여러 TC에서 반복됨
- screenshot 저장 경로와 파일명이 TC마다 달라짐
- 입력 전후 화면 비교 기준이 TC마다 흩어짐
- 실패 시 evidence 저장 방식이 일관되지 않음

## 루프 엔지니어링 검토 시점

다음 문제가 생기면 루프 엔지니어링 도입을 검토한다.

- 화면 상태가 될 때까지 반복 관찰해야 함
- 프리즈 여부를 주기적으로 확인해야 함
- 입력 반응이 즉시 나타나지 않아 여러 번 확인해야 함
- 실패 재현성을 여러 attempt로 비교해야 함
