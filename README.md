# Sheepy 실제 게임 관찰 QA 포트폴리오

게임 QA 신입 지원을 위해 Steam 게임 **Sheepy: A Short Adventure**를 외부에서 관찰하는 Python 자동화 프로젝트입니다. **검증 대상 선정 → 사전조건 확인 → 입력·화면 증거 수집 → 기대/실제 비교 → 판단 한계 설명**을 보여줍니다.

## 먼저 볼 자료

| 질문 | 자료 |
| --- | --- |
| 어떤 기준으로 테스트했는가? | [테스트 기준](docs/test-basis-and-standards.md), [TC 상세](docs/test-cases.md) |
| 무엇을 확인했고 무엇은 확정할 수 없는가? | [판단 기준](docs/judgement-basis.md), [증거 샘플](docs/evidence-samples.md) |
| 반복 실행 문제를 어떻게 다뤘는가? | [사전조건 개선 사례](docs/case-study.md) |
| 현재 완료 여부는? | [진행 상태](docs/progress.md), [완성도 판단](docs/completion-review.md) |

## 실제 구현 범위

`pytest`, `Pillow`, `psutil`, Windows `ctypes`를 사용합니다. OpenCV·OCR·AI 이미지 판정은 구현하지 않았습니다.
프로세스, 창, 시각적 반응, 저장 파일 경로를 관찰합니다. 화면 변화가 이동·점프 성공을, 파일 존재가 저장 데이터 무결성을 증명하지는 않습니다.

언어 선택→로비→플레이 화면 후보의 제한된 준비 절차를 추가했습니다. 알 수 없는 화면에서 키를 반복하지 않으며, 임의 플레이 화면에서 로비로 복귀하는 기능은 없습니다. 내부 상태를 읽는 엔진 하네스는 사용하지 않습니다.

## 게임 없이 실행

Windows PowerShell, Python 3.11 이상 기준입니다.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest
```

가상환경 활성화 없이 실행하므로 PATH 혼동을 줄입니다. `py`가 없다면 설치된 Python의 전체 경로로 가상환경을 만듭니다. [환경 설정](docs/local-environment.md)

실제 Steam 테스트는 별도 opt-in입니다. 게임 설치·로그인·입력 대상 창·유저 상태를 먼저 기록하고 [실행 순서](docs/sprint-plan.md)를 따릅니다. 기존 세이브 삭제·수정은 하지 않습니다.

## 결과 해석

단위 테스트 통과와 실제 게임 테스트 통과를 분리합니다. `REVIEW_REQUIRED`는 pytest의 skip으로 표현하고 별도 집계하며, 통과로 세지 않습니다. 최신 실행 요약은 `artifacts/results/pytest-summary.md`에 생성됩니다. 이전 게임 실행 결과는 [과거 이력](docs/history/2026-09-13-before-revision.md)에 남깁니다.

[전체 문서 지도](docs/index.md) · [추적표](docs/traceability-matrix.md) · [작업 규칙](AGENTS.md)
