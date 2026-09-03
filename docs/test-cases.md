# 테스트 케이스 목록

## 목적

이 문서는 Sheepy 자동화 QA의 개별 TC를 정리한다.

각 TC는 `docs/test-classification.md`의 대분류와 소분류에 연결된다.

## TC 작성 형식

각 TC는 다음 항목을 가진다.

| 항목 | 설명 |
| --- | --- |
| TC ID | 테스트 케이스 식별자 |
| 대분류 | TC-GROUP ID와 이름 |
| 소분류 | 소분류 ID와 이름 |
| 테스트 베이시스 | 테스트 기준이 되는 자료 또는 관찰 |
| 테스트 조건 | 검증할 조건 |
| 사전조건 | 실행 전 필요한 조건 |
| 플레이어 상태 | 최초 실행 유저, 기존 플레이 유저, 상태 불명확 중 하나 |
| 절차 | 테스트 수행 단계 |
| 기대결과 | PASS 기준 |
| Evidence | 저장해야 할 증거 |
| 실패 분류 후보 | 실패 시 우선 검토할 분류 |

각 TC는 구현 시 가능하면 `docs/judgement-basis.md`의 기준에 따라 `judgement.json`을 저장한다.

판단 근거는 다음 세 조건을 분리해서 남긴다.

- 테스트 동작이 실제로 수행됐는가
- 기대 신호가 정상적으로 발생했는가
- 발생하면 안 되는 이상 신호가 없었는가

## Sprint 1 TC

Sprint 1은 한 번에 전체 게임 진행을 검증하지 않는다.

각 TC는 독립 실행 가능한 자동화 단위로 나누며, 앞 단계가 안정적으로 확인된 뒤 다음 단계로 넘어간다.

상세 Sprint 순서는 `docs/sprint-plan.md`를 따른다.

### TC-001 Steam 실행 환경 확인

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-01 설치 및 실행 환경 |
| 소분류 | TC-01-A Steam 환경 |
| 테스트 베이시스 | Steam 클라이언트에서 Sheepy를 실행해야 함 |
| 테스트 조건 | Steam 클라이언트 실행 가능 여부를 확인한다 |
| 사전조건 | Windows에 Steam이 설치되어 있어야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | Steam 프로세스 또는 실행 경로를 확인한다 |
| 기대결과 | Steam 실행 또는 Steam 프로세스 확인이 가능해야 한다 |
| Evidence | process-state.json, judgement.json |
| 실패 분류 후보 | ENV_FAIL |
| 자동화 상태 | 로컬 전용 pytest 구현 |
| 개별 실행 | `scripts/run_tc_001_steam_environment.ps1` |

### TC-002 Sheepy AppID 실행 시도

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-02 실행/종료 |
| 소분류 | TC-02-A 게임 실행 |
| 테스트 베이시스 | Sheepy Steam AppID는 1568400 |
| 테스트 조건 | Steam AppID로 게임 실행을 시도한다 |
| 사전조건 | Steam 로그인 및 Sheepy 설치가 완료되어 있어야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | steam://run/1568400 또는 Steam 실행 명령을 호출한다 |
| 기대결과 | 실행 명령이 오류 없이 호출되어야 한다 |
| Evidence | execution-log.json, judgement.json |
| 실패 분류 후보 | ENV_FAIL, REVIEW_REQUIRED |
| 자동화 상태 | 로컬 전용 pytest 구현 |
| 개별 실행 | `scripts/run_tc_002_sheepy_launch.ps1` |

### TC-003 게임 프로세스 감지

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-02 실행/종료 |
| 소분류 | TC-02-B 프로세스 감지 |
| 테스트 베이시스 | 게임 실행 후 OS에서 프로세스를 관찰할 수 있어야 함 |
| 테스트 조건 | 지정 시간 안에 Sheepy 관련 프로세스를 감지한다 |
| 사전조건 | TC-002 실행 시도가 완료되어야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | 일정 시간 동안 프로세스 목록을 확인한다 |
| 기대결과 | 지정 시간 안에 게임 프로세스가 실행 상태로 확인되어야 한다 |
| Evidence | process-state.json, judgement.json |
| 실패 분류 후보 | ENV_FAIL, PRODUCT_FAIL, REVIEW_REQUIRED |
| 자동화 상태 | 로컬 전용 pytest 구현 |
| 개별 실행 | `scripts/run_tc_003_process_detection.ps1` |

### TC-004 초기 화면 스크린샷 저장

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-03 메인 화면 및 초기 진입 |
| 소분류 | TC-03-C 화면 캡처 |
| 테스트 베이시스 | 실행 후 화면 evidence를 저장해야 함 |
| 테스트 조건 | 게임 실행 후 초기 화면 스크린샷을 저장한다 |
| 사전조건 | 게임 창이 화면에 표시되어야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | 게임 실행 후 지정 대기 시간 뒤 screenshot을 저장한다 |
| 기대결과 | screenshot 파일이 생성되고 파일 크기가 0보다 커야 한다 |
| Evidence | screenshot.png, screen-metadata.json, judgement.json |
| 실패 분류 후보 | ENV_FAIL, TEST_FAIL |
| 자동화 상태 | 로컬 전용 pytest 구현 |
| 개별 실행 | `scripts/run_tc_004_initial_screenshot.ps1` |

### TC-005 검은 화면 여부 확인

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-06 화면/그래픽 표시 |
| 소분류 | TC-06-A 검은 화면 감지 |
| 테스트 베이시스 | 게임 실행 후 화면이 장시간 검은 상태면 진행 불가 리스크가 있음 |
| 테스트 조건 | 초기 화면 screenshot이 완전한 검은 화면인지 확인한다 |
| 사전조건 | TC-004 screenshot이 저장되어야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | screenshot의 평균 밝기 또는 픽셀 분포를 분석한다 |
| 기대결과 | 화면이 완전 검은 상태로만 유지되지 않아야 한다 |
| Evidence | screenshot.png, image-analysis.json, screen-state.json, process-state.json, execution-log.json, judgement.json |
| 실패 분류 후보 | PRODUCT_FAIL, ENV_FAIL, REVIEW_REQUIRED |
| 자동화 상태 | 로컬 전용 pytest 구현 |
| 개별 실행 | `scripts/run_tc_005_black_screen_check.ps1` |

판단 기준:

- `averageBrightness`가 검은 화면 기준값보다 높아야 한다.
- `darkPixelRatio`가 대부분의 화면이 검은 픽셀임을 나타내지 않아야 한다.
- `uniqueSampledColorCount`가 화면 변화 또는 시각 정보가 있음을 보여야 한다.
- 언어 선택 화면처럼 배경이 어둡더라도 국기나 텍스트 등 시각 정보가 있으면 검은 화면으로 단정하지 않는다.

현재 제한:

- 전체 화면 screenshot을 분석하므로, 게임 창 포커스가 다른 창에 가려진 경우 `ENV_FAIL` 또는 `REVIEW_REQUIRED` 검토가 필요하다.
- 메인 메뉴의 정확한 문구나 버튼 식별은 아직 수행하지 않는다.

### TC-006 기본 입력 반응 확인

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-04 입력 반응 |
| 소분류 | TC-04-B 점프 입력 |
| 테스트 베이시스 | 2D 플랫폼 게임은 점프 입력 반응이 핵심 조작 중 하나임 |
| 테스트 조건 | 점프 키 입력 전후 화면 변화가 있는지 확인한다 |
| 사전조건 | 게임 창이 활성화되어 있어야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | 입력 전 screenshot 저장, 점프 입력, 입력 후 screenshot 저장, 이미지 차이 비교 |
| 기대결과 | 입력 전후 화면 차이가 기준값 이상이어야 한다 |
| Evidence | before-input.png, after-input.png, image-diff.json |
| 실패 분류 후보 | PRODUCT_FAIL, TEST_FAIL, REVIEW_REQUIRED |
| 자동화 상태 | 로컬 전용 pytest 구현 |
| 개별 실행 | `scripts/run_tc_006_basic_action_input.ps1` |

판단 기준:

- 테스트 대상 창이 `SheepyAShortAdventure.exe` foreground 상태여야 한다.
- 입력 전 무입력 대기 화면 변화량과 입력 후 화면 변화량을 분리해서 비교한다.
- 입력 후 변화량이 무입력 변화량보다 충분히 커야 입력 반응으로 판단한다.
- 언어 선택 이후 화면이 아닌 상태에서 실행되면 제품 실패가 아니라 `REVIEW_REQUIRED`로 기록한다.

현재 제한:

- Space 입력은 화면을 다음 상태로 진행시킬 수 있으므로 Sprint 4 통합 실행에서는 마지막에 실행한다.
- 현재는 이미지 차이 기반 반응만 확인하며, 캐릭터 좌표나 게임 내부 상태는 읽지 않는다.

### TC-007 짧은 실행 안정성 확인

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-07 안정성/크래시/프리즈 |
| 소분류 | TC-07-C 짧은 안정성 |
| 테스트 베이시스 | 게임은 짧은 시간 동안 비정상 종료 없이 유지되어야 함 |
| 테스트 조건 | 일정 시간 동안 게임 프로세스가 유지되는지 확인한다 |
| 사전조건 | 게임 프로세스가 실행 중이어야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | 30초 동안 프로세스 상태와 화면 변화를 관찰한다 |
| 기대결과 | 프로세스가 비정상 종료되지 않아야 한다 |
| Evidence | process-timeline.json, screenshots/ |
| 실패 분류 후보 | PRODUCT_FAIL, ENV_FAIL, REVIEW_REQUIRED |

### TC-008 실패 evidence 저장 확인

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-08 Evidence 및 리포트 |
| 소분류 | TC-08-A Screenshot, TC-08-B Process State, TC-08-C Test Result |
| 테스트 베이시스 | 자동화 QA는 실패 시 판단 가능한 증거를 남겨야 함 |
| 테스트 조건 | 실패 시 screenshot, process state, log, result가 저장되는지 확인한다 |
| 사전조건 | 테스트 실행 폴더가 생성 가능해야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | 의도된 실패 또는 조건 불만족 상황에서 evidence 저장을 확인한다 |
| 기대결과 | 지정된 evidence 파일이 생성되어야 한다 |
| Evidence | screenshot.png, process-state.json, execution-log.txt, result.json |
| 실패 분류 후보 | TEST_FAIL, ENV_FAIL |

## 후속 TC 후보

| 후보 TC | 대분류 | 소분류 | 설명 |
| --- | --- | --- | --- |
| TC-009 언어 선택 화면 도달 확인 | TC-GROUP-03 | TC-03-D | 초기 진입 화면이 언어 선택 화면인지 판별 |
| TC-010 새 게임 시작 확인 | TC-GROUP-05 | TC-05-A | 새 게임 또는 Continue 진입 확인 |
| TC-011 이동 입력 반응 | TC-GROUP-04 | TC-04-A | 좌우 입력 전후 화면 변화 확인 |
| TC-012 프리즈 감지 | TC-GROUP-07 | TC-07-B | 일정 시간 화면 변화 없음 감지 |
| TC-013 리포트 생성 | TC-GROUP-08 | TC-08-D | 실행 결과 Markdown 또는 HTML 리포트 생성 |
| TC-014 최초 실행 상태 식별 | TC-GROUP-03 | TC-03-A | 세이브 데이터가 없는 첫 진입 상태 확인 |
| TC-015 기존 플레이 상태 식별 | TC-GROUP-03 | TC-03-B | 세이브 데이터가 있는 기존 진입 상태 확인 |
| TC-016 세이브 상태 보존 확인 | 저장/로드 | 후속 확장 | 테스트 후 기존 세이브 데이터가 손상되지 않았는지 확인 |
| TC-017 언어 선택 입력 반응 확인 | TC-GROUP-04 | TC-04-D | 언어 선택 화면에서 선택 입력 후 화면 전환 확인 |
| TC-018 언어 선택 이후 화면 상태 확인 | TC-GROUP-03 | TC-03-E | 언어 선택 완료 후 화면 상태 캡처와 분류 |

## 다음 Sprint 후보: 언어 선택 화면

### TC-009 언어 선택 화면 도달 확인

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-03 메인 화면 및 초기 진입 |
| 소분류 | TC-03-D 언어 선택 화면 |
| 테스트 베이시스 | 현재 관찰 결과 게임 실행 후 언어 선택 화면이 표시됨 |
| 테스트 조건 | 실행 후 초기 화면이 언어 선택 화면인지 확인한다 |
| 사전조건 | Steam 로그인 및 Sheepy 실행 가능 상태 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | 게임 실행, 프로세스 감지, screenshot 저장, 언어 선택 화면 특징 확인 |
| 기대결과 | 영어, 프랑스어, 스페인어, 중국어, 일본어 중 하나 이상의 언어 선택 UI가 보여야 한다 |
| Evidence | language-selection-screen.png, screen-analysis.json, language-screen-analysis.json, judgement.json |
| 실패 분류 후보 | PRODUCT_FAIL, ENV_FAIL, REVIEW_REQUIRED |
| 자동화 상태 | 로컬 전용 pytest 구현 |
| 개별 실행 | `scripts/run_tc_009_language_selection_screen.ps1` |

플레이어 상태 판단:

- 최초 실행 유저에게만 언어 선택 화면이 나오는지 아직 확정하지 않는다.
- 기존 플레이 유저에게도 언어 선택 화면이 반복 표시되는지는 별도 재실행 관찰이 필요하다.
- 따라서 초기 자동화에서는 `PLAYER-UNKNOWN`으로 두고, 세이브 상태 기준이 확정되면 `PLAYER-NEW`와 `PLAYER-RETURNING`으로 분리한다.

### TC-017 언어 선택 입력 반응 확인

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-04 입력 반응 |
| 소분류 | TC-04-D 언어 선택 입력 |
| 테스트 베이시스 | 언어 선택 화면에서 선택 입력을 통해 다음 화면으로 진행할 수 있어야 함 |
| 테스트 조건 | 언어 선택 화면에서 선택 입력 후 화면 변화가 발생하는지 확인한다 |
| 사전조건 | TC-009 언어 선택 화면 도달이 확인되어야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | 입력 전 screenshot 저장, 선택 입력 수행, 입력 후 screenshot 저장, 화면 변화 비교 |
| 기대결과 | 입력 전후 screenshot 차이가 발생하고 다음 화면으로 전환되어야 한다 |
| Evidence | before-language-input.png, after-language-input.png, image-diff.json, input-log.json, foreground-window.json, judgement.json |
| 실패 분류 후보 | PRODUCT_FAIL, TEST_FAIL, ENV_FAIL, REVIEW_REQUIRED |
| 자동화 상태 | 로컬 전용 pytest 구현 |
| 개별 실행 | `scripts/run_tc_017_language_selection_input.ps1` |

플레이어 상태 판단:

- 최초 실행 유저라면 언어 선택 입력은 첫 진입 흐름의 필수 단계일 가능성이 높다.
- 기존 플레이 유저라면 언어 선택 화면이 재노출되는 설계인지 먼저 확인해야 한다.
- 기존 플레이 유저에게 언어 선택 화면이 나오지 않는다면 이 TC는 `PLAYER-NEW` 전용 TC로 분리한다.

## Sprint 4 TC: 언어 선택 이후 화면과 입력 반응

### TC-018 언어 선택 이후 화면 상태 확인

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-03 메인 화면 및 초기 진입 |
| 소분류 | TC-03-E 언어 선택 이후 화면 |
| 테스트 베이시스 | 언어 선택 입력 이후 다음 화면이 표시되어야 함 |
| 테스트 조건 | 현재 게임 화면이 언어 선택 이후 화면인지 캡처하고 분류한다 |
| 사전조건 | Sheepy가 실행 중이고 언어 선택이 완료된 상태여야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | 게임 창 탐지, 창 단독 screenshot 저장, 이미지 분석, 언어 선택 화면 특징 재검사, 이후 화면 분류 |
| 기대결과 | 화면이 검은 화면이 아니고 언어 선택 화면 특징이 남아 있지 않으며, 충분한 시각 정보가 있어야 한다 |
| Evidence | post-language-screen.png, screen-analysis.json, language-screen-analysis.json, post-language-screen.json, judgement.json |
| 실패 분류 후보 | PRODUCT_FAIL, TEST_FAIL, ENV_FAIL, REVIEW_REQUIRED |
| 자동화 상태 | 로컬 전용 pytest 구현 |
| 개별 실행 | `scripts/run_tc_018_post_language_screen.ps1` |

판단 기준:

- `post-language-screen.json.screenState`가 `POST_LANGUAGE_SCREEN`이어야 한다.
- `screen-analysis.json.uniqueSampledColorCount`가 10보다 커야 한다.
- `language-screen-analysis.json.isLanguageSelectionLike`가 `false`여야 한다.
- `screen-analysis.json.isMostlyBlack`이 `false`여야 한다.
- 언어 선택 화면이 다시 감지되면 사전조건 불충족 가능성이 있으므로 `REVIEW_REQUIRED`로 남긴다.

### TC-011 이동 입력 반응

| 항목 | 내용 |
| --- | --- |
| 대분류 | TC-GROUP-04 입력 반응 |
| 소분류 | TC-04-A 이동 입력 |
| 테스트 베이시스 | 2D 플랫폼 게임은 좌우 이동 입력 반응이 핵심 조작 중 하나임 |
| 테스트 조건 | 좌우 입력 전후 화면 변화가 무입력 상태 변화보다 명확한지 확인한다 |
| 사전조건 | Sheepy가 실행 중이고 언어 선택 이후 화면이 표시되어야 한다 |
| 플레이어 상태 | PLAYER-UNKNOWN |
| 절차 | 입력 전 screenshot 저장, 무입력 대기 screenshot 저장, 좌우 입력, 입력 후 screenshot 저장, 이미지 차이 비교 |
| 기대결과 | 입력 후 변화량이 무입력 변화량보다 기준값 이상 커야 한다 |
| Evidence | before-movement-input.png, idle-movement-input.png, after-movement-input.png, idle-diff.json, input-diff.json, input-log.json, foreground-window.json, judgement.json |
| 실패 분류 후보 | PRODUCT_FAIL, TEST_FAIL, ENV_FAIL, REVIEW_REQUIRED |
| 자동화 상태 | 로컬 전용 pytest 구현 |
| 개별 실행 | `scripts/run_tc_011_movement_input.ps1` |

판단 기준:

- 테스트 대상 창이 `SheepyAShortAdventure.exe` foreground 상태여야 한다.
- 사전 화면은 `POST_LANGUAGE_SCREEN`으로 분류되어야 한다.
- `input-log.json.inputChangeDelta`가 `0.005` 이상이어야 한다.
- 입력 후 화면이 완전히 동일하면 이상 신호로 기록한다.
- 사전 화면이 언어 선택 화면 또는 검은 화면이면 제품 실패로 단정하지 않고 `REVIEW_REQUIRED`로 남긴다.
