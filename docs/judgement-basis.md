# 판단 근거와 실행 상태

## 판정 계약

`createJudgementRecord`는 동작 수행, 하나 이상의 필수 기대 신호, 이상 신호, 사전조건을 확인한다. 빈 expectedSignals는 REVIEW_REQUIRED이다. expectedResult/actualResult는 설명용 상태명이며 문자열 동일성 대신 TC의 명시적 신호를 평가한다.

| 결과 | 조건 | 해석 |
| --- | --- | --- |
| PASS | 동작·기대 신호·이상 신호 부재·사전조건 충족 | 해당 관찰 계약 충족 |
| FAIL | 관찰 조건은 충족했지만 기대 신호 실패 | 제품 결함 확정 전 인식/입력/환경 검토 |
| REVIEW_REQUIRED | 동작 불확실, 사전조건 부족, 필수 신호 없음 | 검증 완료가 아님 |

pytest에서는 REVIEW_REQUIRED를 `skip("REVIEW_REQUIRED: ...")`로 표현한다. 알려진 결함의 기대 실패를 의미하는 xfail과 구분한다. tests/conftest.py가 PASS/FAIL/REVIEW_REQUIRED/NOT_RUN을 별도 집계한다. 명령 종료 코드 0만 보고 전체 게임 검증 완료로 판단하지 않는다.

## 관찰 범위

| 신호 | 말할 수 있는 것 | 말할 수 없는 것 |
| --- | --- | --- |
| INPUT_VISUAL_RESPONSE | 무입력 대비 이미지 변화 | 이동/점프 성공 확정 |
| GAMEPLAY_SCREEN_CANDIDATE | 로비에서 화면 후보로 전환 | 조작·레벨 진행 정상 보장 |
| SCREEN_CHANGE_OBSERVED | 변화 및 연속 무변화 제한 미만 | 내부 프리즈 부재 보장 |
| SAVE_FILES_PRESENT | 관찰 전 파일 경로 존재 유지 | 저장 내용 무결성/복원 가능 |

임계값 변경은 [이미지 평가](image-validation.md)의 자료와 이유를 남긴 후 수행한다. 실패를 없애기 위한 완화는 하지 않는다.
