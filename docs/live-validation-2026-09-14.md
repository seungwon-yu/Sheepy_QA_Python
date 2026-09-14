# 실제 게임 재검증 — 2026-09-14

이번 실행은 전체 완료 검증이 아니라 실제 환경에서 사전조건·캡처·판정의 결함을 확인한 진단 실행이다. 로컬 evidence의 UTC 날짜는 2026-09-13이며 KST 기록일은 2026-09-14이다. raw 결과와 검토 결론을 구분한다.

| TC | 실제 결과 | 검토 결론 |
| --- | --- | --- |
| 001/003 | 선택 실행 2 PASS | 실행된 게임 프로세스 관찰. Steam URI 기동 3회 증명 아님 |
| 004 | sandbox FAIL → desktop PASS | 동일 Pillow 캡처가 실행 환경에 따라 달랐다. 전체 바탕화면 증거는 비공개 |
| 019 | 최초 준비 REVIEW → 로비 FAIL, 렌더링 캡처 후도 FAIL | 어두운 Start Your Journey 항목 미감지. 임계값을 낮춰 통과시키지 않음 |
| 010 | raw PASS | 0.812초 증거가 로비 전환 연출. 실제 플레이 진입 완료로 인정하지 않음 |
| 007/012 | 2 PASS | 당시 관찰 구간의 프로세스·캡처·변화 확인. 이후 캡처 수정 후 재검증과 3회 반복은 남음 |
| 006 | FAIL → REVIEW 반복 | 외곽 캡처에서는 로딩 중 입력(delta=-0.118). 렌더링 캡처 후에는 로딩 인식으로 입력 보류. 최종 준비에서 실제 플레이를 LANGUAGE로 오판 |
| 011 및 나머지 미실행 TC | NOT_RUN | 인식 결함 해결 전 입력 확대하지 않음 |

## 수정과 남은 결함

- 게임 창 외곽에는 제목 표시줄과 주변 창 일부가 섞였다. NW.js 렌더링 자식 창 640×360만 캡처하도록 수정했다. GetClientRect만으로는 사용자 지정 제목 표시줄이 남아 실제 자식 창 경계를 사용했다.
- Continue 후 로비 페이드가 GAMEPLAY 후보로 오인됐다. 로딩 BLACK 관찰 후 2초 연속 후보를 요구한다. 로딩 프레임을 놓친 경우는 보류한다.
- 실제 플레이 후보 출현 14.531초를 기록했다. 로컬 준비 대기를 30초로 설정하며 제품 성능 합격 기준과 구분한다. 최초 타임아웃은 보존한다.
- 실제 플레이 화면을 LANGUAGE로 오판했다. 로비 Enter 이후 LANGUAGE가 나타나면 추가 Enter를 보내지 않고 REVIEW로 중단하도록 수정했다. 인식 함수의 오탐 자체는 **미해결**이다.

![실제 플레이 화면인데 언어 선택 후보로 오판한 사례](samples/gameplay-language-false-positive.png)

이미지는 실제 게임 영역만 포함한다. AI가 화면을 대조한 진단 증거이며 사람이 라벨링한 평가셋으로 주장하지 않는다. centralDarkPixelRatio=0.8144, centralSaturatedPixelRatio=0.062, visibleOptionCount=3으로 기존 휴리스틱의 언어 후보 조건을 충족한다. `test_language_real_regression.py`는 실제 플레이를 언어로 분류하지 않아야 한다는 기대값으로 작성했다. 후속 오프라인 수정에서 양옆 배경 조건을 추가해 같은 기대값으로 통과했고 xfail 표시를 제거했다. 위 실제 실행 당시 결과는 보존하며 수정 후 실제 TC는 아직 재실행하지 않았다. [추가 판정 조건과 검증 범위](image-validation.md).

## 다음 실제 검증 전 조건

후속 오프라인 수정: 로비 CTA의 주변 대비를 측정해 보관된 Start 미탐 표본을 회귀 통과로 전환했다. 밝은 단색·완만한 명암 변화의 오탐도 회귀로 차단했다. 실제 실행 당시 FAIL은 유지하며 수정 후 TC-019는 미실행이다. [판정 변경·표본·남은 한계](image-validation.md#어두운-로비-cta-회귀).

1. 언어 화면/플레이/로비/로딩의 실제 표본에 독립적인 정답을 붙여 화면 분류를 보완한다.
2. Start 항목의 고정 영역·명암 조건을 실제 표본으로 평가한다. 밝은 배경을 글자로 오인하는 반례도 포함한다.
3. 안정된 로비에서 010→006/011을 각각 재준비해 수행한다. 단계별 최초 결과와 재시도를 분리한다.
4. 수정 후 정상 흐름 3회와 실패 차단 증거를 확보하기 전 최종본 완료로 표시하지 않는다.

게임 파일·세이브는 직접 수정하거나 삭제하지 않았다. 수동 메뉴 탐색 Escape→Down→Down→Enter로 Quit 후 로비 복귀를 확인했으며 이 경로를 아직 자동 복구 기능으로 구현하지 않았다.

## 주변 대비 수정 후 실제 재검증

코드 기준 `31c90e9`, 2026-09-14 19:20 KST. 사용자 실행 후 Continue 선택 로비를 캡처로 확인했다. 창 외곽 826×542, 렌더링 캡처 810×503(상하 검은 여백 포함)이다. 이전 640×360과 다른 크기이며 OS 배율·현재 build는 재확인하지 않았다. sandbox에서는 창 미감지였고 승인된 desktop 실행에서 확인했다.

| TC / 실행 ID (UTC) | 결과 | 근거 |
| --- | --- | --- |
| TC-019 / 2026-09-14T10-20-23.529+00-00-TC-019 | PASS 1회 | Continue 대비 0.2078, Start 대비 0.1029. [판정](samples/TC-019-contrast-judgement.json), [분석](samples/TC-019-contrast-analysis.json) |
| TC-010 / 2026-09-14T10-20-41.380+00-00-TC-010 | REVIEW_REQUIRED | Enter 1회, 3.750초 BLACK 관찰, 13.235초 foreground=false로 중단. [준비 로그](samples/TC-010-focus-loss-preparation.json) |

명령은 `SHEEPY_RUN_STEAM_TESTS=1`에서 `python -m pytest -m tc_019 -q`, 이어서 `python -m pytest -m tc_010 -q -p no:cacheprovider`이다. TC-019의 pytest 캐시 쓰기 경고는 검증 실패와 구분한다. TC-010은 로딩 전에 나타난 GAMEPLAY 후보를 준비 완료로 인정하지 않았고 포커스 상실 후 추가 입력을 보내지 않았다. 포커스 상실 원인과 실제 플레이 진입 완료는 확정하지 않는다. 후속 입력 TC는 실행하지 않았다.

TC-019의 이번 화면은 이전 어두운 표본보다 밝아 절대 밝기 기준도 만족할 수 있다. 이번 PASS만으로 수정 효과나 모든 배율의 안정성을 주장하지 않는다. 실제 수정 효과의 근거는 이전 미탐 표본 회귀이며, 실제 정상 흐름 3회는 아직 미완료이다.

## TC-010 렌더링 창 오류 재시도

코드 `b0212f6`, 실행 ID `2026-09-14T10-27-34.325+00-00-TC-010` (19:27 KST). 시작 시 플레이 화면을 확인하고 Escape 메뉴에서 Quit 선택을 캡처로 대조한 후 로비로 복귀했다. 준비 중 창 크기 변화가 관찰됐으나 원인은 확정하지 않았다. 게임·세이브 파일은 직접 수정하지 않았다.

`SHEEPY_RUN_STEAM_TESTS=1`, `python -m pytest -m tc_010 -q -p no:cacheprovider` 결과는 **1 skipped / REVIEW_REQUIRED**이다. 로비 준비는 0.219초에 충족했지만 GAMEPLAY 준비 첫 캡처에서 `OSError: Expected one visible Sheepy rendering window`가 발생했다. 이번 TC의 Continue 입력 수행은 확인되지 않았다. [로비 준비](samples/TC-010-render-window-lobby.json), [캡처 오류](samples/TC-010-render-window-preparation.json), [판정](samples/TC-010-render-window-judgement.json).

이후 desktop에서 게임 창을 재조회했지만 감지되지 않았다. Sheepy 프로세스 2개는 남아 있었고 MainWindowTitle은 비어 있었다. 게임 종료·충돌·리사이즈 중 상태 중 어느 원인인지 확정할 수 없다. 추가 입력과 실제 TC 재시도를 중단하고 사용자에게 화면 상태 확인을 요청했다. 19:20의 포커스 상실과 이번 렌더링 창 오류를 별개 실행으로 유지한다. TC-010 정상 전환 통과와 3회 반복은 미완료이다.

사용자가 게임이 꺼져 다시 실행했다고 확인했다. 종료 원인은 미확정이다. 새 창의 안내 화면 종료 후 640×360 Continue 로비를 캡처로 대조하고 다음 두 실행을 별도로 수행했다.

| 실행 ID (UTC), TC-010 | 결과 | 근거 |
| --- | --- | --- |
| 2026-09-14T10-30-35.885+00-00-TC-010 | REVIEW_REQUIRED | LOBBY 준비 첫 관찰 foreground=false. [로그](samples/TC-010-restart-focus-preparation.json) |
| 2026-09-14T10-31-01.514+00-00-TC-010 | REVIEW_REQUIRED | 제목 표시줄 클릭 후 foreground=true 확인, 같은 Python 프로세스의 pytest.main으로 실행. 이미지 크기 불일치 오류. [로그](samples/TC-010-size-change-preparation.json) |

마지막 실행의 prepare-000~002는 640×360, prepare-003은 1858×1057이었다. 서로 다른 크기의 이미지를 비교하는 단계에서 중단됐다. 크기 변경의 원인은 확정하지 않는다. 테스트 기대값과 이미지 비교 기준을 완화하지 않았다.

추가 결함: LocalScreenSession.prepare의 예외 처리 결과가 events=[]로 기록되어 중단 전 상태·입력 이벤트가 보존되지 않는다. 마지막 실행의 actionPerformed=false를 실제 입력 부재로 해석하면 안 된다. 다음 수정은 크기 변경을 명시적으로 감지해 입력을 중단하고, 예외 이전 이벤트와 마지막 관찰 근거를 유지하는 것이다. 임의 리사이즈로 통과시키지 않는다. 이후 실제 입력 테스트는 실행하지 않았다.
