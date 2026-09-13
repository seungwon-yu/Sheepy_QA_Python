# 실제 실행 순서와 재검증 계획

## 게임 없는 검증

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## 실제 게임 검증

[환경 프로필](environment-profile.md)을 기록하고 Steam 로그인·게임 설치·입력 가능 상태를 확인한다. 다음 명령은 실제 입력과 화면 전환을 수행한다.

```powershell
$env:SHEEPY_RUN_STEAM_TESTS = "1"
.\.venv\Scripts\python.exe -m pytest tests/local/test_tc_001_004_local_steam.py
.\.venv\Scripts\python.exe -m pytest -m tc_019
.\.venv\Scripts\python.exe -m pytest -m tc_010
```

로비 표시→진입을 순서대로 확인한다. 입력 TC-006/011/016은 각각 **사람이 로비로 준비한 뒤** 개별 실행한다. helper는 이미 플레이 중인 화면에서 로비로 돌아오지 못하므로 무작위 전체 실행 성공을 보장하지 않는다. TC-018은 언어 이후 후보 관찰이며 플레이 상태 증명이 아니다.

최초 실행 TC-013과 기존 플레이 TC-014는 같은 저장 상태에서 동시에 필수 통과시키지 않는다. TC-015는 파일 후보가 있어야 하며 찾지 못하면 보류한다.

## 반복 검증 완료 기준

각각 같은 기록된 시작 상태로 준비한 3회 실행에 대해 최초 결과·준비 실패·실행 시간·증거를 기록한다. 실패 후 재시도로 얻은 PASS를 최초 PASS와 합치지 않는다. 현재 환경에서 확인하지 못한 항목은 미실행이다.

기존 scripts/run_tc_*.ps1은 개별 진입점으로 유지한다. run_sprint_* 전체 실행은 이력 재현용이며 상태 준비 없이 모두 통과할 것으로 기대하지 않는다.

최종본 작업 범위와 단계별 완료 조건은 [최종본 계획](finalization-plan.md)을 따른다.

GAMEPLAY 후보는 2초 연속 관찰 후 준비 완료로 인정한다. 중간에 로비·검은 화면이 보이면 연속 시간을 초기화한다. 이는 순간 전환 오판 완화이며 실제 플레이 판정의 정확도 보장은 아니다.
