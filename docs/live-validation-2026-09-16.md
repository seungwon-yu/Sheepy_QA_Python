# 로비와 게임 진입 3회 재검증

## 조건과 순서

실행 기준 커밋은 `c4911d3`이다. 테스트 코드와 판정 기준은 변경하지 않았다. 사용자가 언어 선택 화면과 포커스를 준비한 뒤 English를 선택하고 인트로가 끝나기를 기다렸다. Continue가 선택된 로비를 캡처로 확인한 시점부터 이번 반복 묶음을 시작했다.

640×360 렌더링 캡처, 기존 플레이 상태의 Continue 경로이다. build·OS 배율은 이번에 재확인하지 않았으며 [환경 프로필](environment-profile.md)의 과거 기록과 구분한다. 게임과 세이브 파일을 직접 변경하지 않았다.

각 회차는 TC-019 → TC-010 순서이다. 회차 사이에는 플레이 화면에서 Escape로 메뉴를 열고 Quit 선택을 화면으로 확인한 뒤 로비로 복귀했다. 이 준비는 관찰에 따른 수동 제어이며 테스트가 임의 화면에서 자동 복귀하는 기능이 아니다. 동일 실행 세션의 반복으로, 게임 미실행 상태부터 재기동한 3회가 아니다.

```powershell
$env:SHEEPY_RUN_STEAM_TESTS = '1'
$env:PYTHONIOENCODING = 'utf-8'
.\.venv\Scripts\python.exe -m pytest tests/local/test_tc_019_lobby_menu_options.py tests/local/test_tc_010_gameplay_entry.py -q -p no:cacheprovider
```

## 결과

| 회차 | TC-019 | TC-010 | TC-010 마지막 관찰 시각 | pytest 결과 |
| --- | --- | --- | --- | --- |
| 1 | PASS | PASS | 17.438초 | 2 passed in 18.81s |
| 2 | PASS | PASS | 15.547초 | 2 passed in 16.94s |
| 3 | PASS | PASS | 16.078초 | 2 passed in 17.46s |

이번 묶음은 총 6 PASS, FAIL·REVIEW_REQUIRED 0회다. 이전 실행 결과를 합산하지 않았다. [원본 실행 ID와 집계](samples/entry-repeat-0916.json)는 로컬 `artifacts/evidence/<id>`의 JSON과 대조했다. 6개 실행의 캡처 총 85개는 모두 640×360이다.

TC-019는 세 번 모두 Continue와 Start 텍스트 영역 후보를 검출했다. TC-010은 세 번 모두 로비 Enter 콜백 정상 반환 1회, BLACK 관찰, 이후 2초 이상 연속 GAMEPLAY 후보를 기록했다. 각 관찰 시점의 foreground는 true였다. 초기 전환 중 GAMEPLAY 후보가 먼저 나타나더라도 BLACK 이전에는 준비 완료로 인정하지 않았다. 각 회차 최종 플레이 화면도 직접 확인했다.

대표 3회차 근거: [로비](samples/entry-repeat-0916-lobby.png), [최종 플레이 화면](samples/entry-repeat-0916-gameplay.png), [준비 이벤트](samples/entry-repeat-0916-preparation.json), [판정](samples/entry-repeat-0916-judgement.json).

## 한계와 다음 작업

PASS는 정해진 화면 후보와 전환 조건 충족이다. 메뉴 문자를 OCR로 읽은 결과, 조작 성공, 세이브 무결성, 다른 해상도에서의 정확도나 기동 성능 보장이 아니다. 관찰 사이 모든 순간의 포커스를 감시한 것도 아니다. 게임 없는 단위 테스트는 이번 문서 변경에서 재실행하지 않았다(직전 기준 114 passed, 18 skipped).

묶음 시작 전 포커스·렌더링 창 준비 문제는 이번 TC의 실패나 성공으로 합산하지 않는다. 이전 로컬 진단 `2026-09-15T10-19-23.751+00-00-ENTRY-REPEAT-FOCUS-PRECHECK`와 `2026-09-16T10-22-39.649+00-00-ENTRY-RESTART-WINDOW-DIAG`를 보존하며, 사용자의 화면 준비 도움을 받은 사실을 반복 자동화 성공으로 숨기지 않는다.

다음 작은 작업은 TC-006·011 입력 시각 반응의 각 3회 검증이다. 기동 반복, 실제 오류 상황의 중단·이벤트 보존, 독립 이미지 평가는 별도로 남아 있다.
