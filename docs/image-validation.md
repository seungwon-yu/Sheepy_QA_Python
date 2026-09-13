# 이미지 판별 기준 검증 계획

현재 임계값은 초기 관찰에 기반한 휴리스틱이다. 다양한 환경에서 정확도가 검증된 수치로 제시하지 않는다.

| 항목 | 현재 코드 기준 | 검증할 반례 |
| --- | --- | --- |
| 플레이 화면 후보 | 로비 소멸, 변화량 >=0.05, 색상 수 >10 | 컷신·다른 메뉴·전환 중 화면 |
| 입력 반응 | 입력 변화량-무입력 변화량 >=0.005 | 배경 애니메이션·카메라 움직임 |
| 화면 변화 | 변화량 >=0.001, 연속 무변화 10초 미만 | 초반 변화 후 정지·정적 정상 장면 |
| 로비 CTA | 고정 상대 영역의 텍스트 후보 신호 | 배율·창 비율 변경·비슷한 무늬 |

## 자료 작성

정상·오인하기 쉬운 화면에 사람이 정답을 붙인다. 기준 조정용과 평가용을 분리한다. 파일, 정답, 자동 판정, 환경, 오탐/미탐/보류 사유를 기록한다. 평가 자료에서 틀린 결과를 삭제하지 않는다.

현재 별도 정답셋 평가와 임계값 정확도 수치는 미완료이다. 기존 evidence 예시는 정답셋이 아니다. 실제 화면 1회 PASS를 모든 장면에 일반화하지 않는다.

## 재현 가능한 입력 반응 평가

PowerShell에서 저장소 루트를 기준으로 실행한다. pytest의 pythonpath 설정은 일반 Python 명령에 적용되지 않으므로 src를 명시한다.

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m sheepy_qa.image_evaluation docs/samples/image-evaluation-manifest.json --output artifacts/results/image-evaluation.json
```

공개 manifest는 빈 표본이며 `NOT_EVALUATED`가 정상 결과이다. 실제 평가를 주장하지 않는다. 실제 자료는 다음 필드로 구성하고 이미지 경로는 manifest 기준 상대 경로로 작성한다.

```json
{"samples": [{"id": "input-001", "split": "evaluation", "captureSession": "session-001", "expected": "RESPONSE", "reviewer": "실제 검토자", "reason": "화면을 확인하고 기록할 근거", "environment": "빌드·해상도·창 모드", "preconditionsMet": true, "before": "before.png", "idle": "idle.png", "after": "after.png"}]}
```

위 행은 형식 설명이며 정답 표본이 아니다. before→idle은 무입력, idle→after는 입력 구간이며 동일 관찰 간격과 화면 영역을 사용한다. expected는 사람이 확인한 RESPONSE/NO_RESPONSE이다. preconditionsMet는 실제 준비·포커스 관찰 기록에서 가져오며 정답을 보고 바꾸지 않는다. 사전조건이 없으면 REVIEW_REQUIRED로 별도 집계한다.

동일 녹화 세션을 calibration과 evaluation에 나눠 넣는 것을 차단한다. 평가용만 참양성·참음성·오탐·미탐·보류에 집계하며 잘못된 라벨이나 누락 이미지는 오류로 처리한다. 빈 평가셋에는 정확도나 성공률을 만들지 않는다. 로컬 입력 테스트와 임계값 0.005를 공유한다. 화면 후보 인식 전체의 정확도, 점프·이동의 실제 성공 정확도를 측정하는 도구는 아니다.

인공 이미지 회귀 테스트는 평가 도구의 집계와 누출 방지 검증이며 실제 게임 정답셋과 구분한다.

2026-09-14 실제 창 외곽 656×399, 게임 표시 영역 640×360을 확인했다. 창 캡처는 제목 표시줄·테두리를 제외한 client 영역으로 변경한다. 전체 화면 캡처 TC-004는 별도 기능이며 게임 상태 판정 근거로 사용하지 않는다. 이전 외곽 이미지와 새 이미지는 직접 비교하지 않는다.
