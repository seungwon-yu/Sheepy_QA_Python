# 실제 기동 검증 기록

2026-09-14. 사용자 지정 경로의 Steam executable, Steam protocol, Sheepy AppID 설치 manifest와 build 21288283을 읽기 전용으로 확인했다. 계정 식별자는 공개 기록에서 제외했다.

| TC | 최신 결과 | 확인 범위 |
| --- | --- | --- |
| TC-001 | PASS | STEAM_AVAILABLE |
| TC-002 | PASS | SHEEPY_APPID_LAUNCH_COMMAND_CALLED |
| TC-003 | FAIL | SHEEPY_PROCESS_NOT_DETECTED |

최초 TC-003은 실행 명령 후 60초 안에 프로세스를 찾지 못해 FAIL이었다. 이후 Steam 프로세스가 확인되어 1회 재시도했다. 명령 호출 PASS는 게임 정상 기동을 의미하지 않는다. 최초 실패를 이후 결과로 덮지 않는다.

판정 근거는 [현재 관찰 JSON](samples/local-verification.json), [프로세스 판정](samples/TC-003-judgement.json)에 있다. 원본 실행별 evidence와 local-launch-first.json은 로컬 artifacts에 보존한다.

최신 프로세스 관찰도 실패했으므로 기동 환경/로그인/Steam 상태를 확인해야 한다. 제품 버그로 단정하지 않으며 화면·입력 TC는 미실행이다.
