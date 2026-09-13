# 증거를 읽는 방법

과거 TC-010/019/012 예시는 [실행 이력](history/2026-09-13-before-revision.md)에 보존했다. 이전 FREEZE_NOT_DETECTED/SAVE_DATA_PRESERVED 상태명은 당시 출력이며 현재 검증 범위로 확대 해석하지 않는다.

현재 준비 기반 TC는 prepare-번호.png/json, preparation.json, judgement.json을 생성한다. 입력 TC는 idle-diff.json, input-diff.json, visual-response.json, input-log.json을 추가한다.

| 질문 | 증거 | 설명 |
| --- | --- | --- |
| 무엇을 검증했나? | TC와 judgement.expectedSignals | 제품 기능과 관찰 신호 구분 |
| 어디서 시작했나? | preparation.events, prepare 이미지 | 지원하는 상태에서 실행했는지 |
| 실제 입력했나? | input-log, actionPerformed | 호출 사실과 효과를 구분 |
| 기대와 무엇이 다른가? | visual-response, judgement | 숫자와 기준값 확인 |
| 무엇이 불확실한가? | blockingConditions, REVIEW_REQUIRED | 근거 누락·준비 실패 설명 |

현재 화면·입력 재검증 샘플은 미완료이다. 실행 전에는 placeholder 이미지를 실제 결과처럼 넣지 않는다. 실제 결과 공유 전 환경 정보와 화면을 확인하고 필요한 샘플만 공개한다.

## 실제 기동 후속 증거

새 코드의 TC-001~003 관찰은 [기동 기록](local-verification.md)에 있다. 화면 판별 정확도 검증 자료와는 구분한다.
