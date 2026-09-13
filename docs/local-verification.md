# 실제 기동 검증 기록

2026-09-14. 사용자 지정 경로의 Steam executable, Steam protocol, Sheepy AppID 설치 manifest와 build 21288283을 읽기 전용으로 확인했다. 계정 식별자는 공개 기록에서 제외했다.

| TC | 최신 결과 | 확인 범위 |
| --- | --- | --- |
| TC-001 | PASS | STEAM_AVAILABLE |
| TC-002 | PASS | SHEEPY_APPID_LAUNCH_COMMAND_CALLED |
| TC-003 | PASS (수동 실행 후 관찰) | 최초 샘플부터 프로세스 존재; 자동 기동 검증 아님 |

최초 TC-003은 실행 명령 후 60초 안에 프로세스를 찾지 못해 FAIL이었다. 이후 Steam 프로세스가 확인되어 1회 재시도했다. 명령 호출 PASS는 게임 정상 기동을 의미하지 않는다. 최초 실패를 이후 결과로 덮지 않는다.

판정 근거는 [이전 실패 관찰 JSON](samples/local-verification.json), [이전 실패 판정](samples/TC-003-judgement.json)에 있다. 원본 실행별 evidence와 local-launch-first.json은 로컬 artifacts에 보존한다.

이전 자동 기동 관찰은 실패했다. 수동 실행 후 감지는 아래에 분리한다. 제품 버그로 단정하지 않으며 화면·입력 TC는 미실행이다.

## 기동 진단 증거 보완

TC-003은 `process-observation.json`에 각 감지 시각과 프로세스 목록을 기록한다. `initialProcessPresent=true`는 관찰 시작부터 게임이 있었다는 뜻이며 새 기동 성공으로 세지 않는다. false에서 감지로 바뀌어도 프로세스 출현만 증명하며 창 준비나 게임 플레이 성공을 보장하지 않는다. `process-state.json`은 최종 샘플로 호환 유지한다. 과거 60초 FAIL은 그대로 보존한다.

## 수동 실행 후 재관찰 — 2026-09-14

사용자가 직접 실행한 뒤 `pytest tests/local/test_tc_001_004_local_steam.py -m "tc_001 or tc_003" -q`를 opt-in으로 실행했다. **2 passed, 2 deselected**. 이번 실행은 게임을 새로 시작하거나 키를 입력하지 않았다.

[식별 정보를 제외한 시간별 관찰](samples/TC-003-manual-process-observation.json), [판정](samples/TC-003-manual-judgement.json). 첫 샘플부터 SheepyAShortAdventure.exe 7개가 관찰됐고 `initialProcessPresent=true`이다. elapsedSeconds=2.0은 관찰 비용을 포함한 시간이며 게임 기동 시간으로 해석하지 않는다. 다중 프로세스 이유는 미확인이고 임의 종료하지 않았다.

Computer Use의 창 목록에서 SheepyAShortAdventure 창 1개를 찾았으나 캡처는 `SetIsBorderRequired failed: 해당 인터페이스를 지원하지 않습니다. (0x80004002)`로 실패했다. 창을 재선택해 한 번 재시도했지만 동일했다. 이는 관찰 도구 오류이며 Sheepy 게임 결함으로 분류하지 않는다. 화면 미확인 상태에서 게임 입력을 하지 않았다.

TC-003의 프로세스 감지 계약은 통과했지만 자동 기동 3회 반복, 로비 화면, 입력 반응, 정답셋 평가는 여전히 미완료이다.
