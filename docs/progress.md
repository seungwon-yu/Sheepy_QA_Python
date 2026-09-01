# 진행 상황

## 목적

이 문서는 프로젝트를 이어서 작업할 때 현재 완료된 범위와 다음 작업을 빠르게 확인하기 위한 기록이다.

상세 기준은 `docs/test-basis-and-standards.md`, TC 분류는 `docs/test-classification.md`, Sprint 순서는 `docs/sprint-plan.md`를 따른다.

## 완료된 작업

### 프로젝트 초기 구조

- Python 기반 자동화 QA 프로젝트 구조를 생성했다.
- `pytest`, `Pillow`, `psutil` 기반의 기본 의존성을 설정했다.
- GitHub Actions CI를 추가해 기본 단위 테스트와 import 오류를 확인하도록 했다.
- 실제 Steam 게임 실행 테스트는 CI가 아니라 로컬 전용 테스트로 분리했다.

### 테스트 기준과 TC 분류

- ISTQB CTFL Foundation 기준으로 테스트 베이시스, 테스트 조건, 기대결과, evidence 중심의 TC 작성 방식을 정리했다.
- ISTQB CTFL Game Testing 기준으로 게임 QA 대분류를 설치/실행 환경, 실행/종료, 메인 화면, 입력 반응, 기본 플레이, 화면/그래픽, 안정성, evidence/리포트로 나누었다.
- 각 TC가 어느 대분류와 소분류에 연결되는지 추적 매트릭스로 정리했다.

### Sprint 1: 실행 환경과 초기 진입

- TC-001 Steam 실행 환경 확인을 구현했다.
- TC-002 Sheepy AppID 실행 시도를 구현했다.
- TC-003 게임 프로세스 감지를 구현했다.
- TC-004 초기 화면 스크린샷 저장을 구현했다.
- 각 TC를 개별 PowerShell 스크립트로 실행할 수 있게 분리했다.

### Sprint 2: 화면 상태 판별

- TC-005 검은 화면 여부 확인을 구현했다.
- `src/sheepy_qa/image_analysis.py`에서 screenshot의 평균 밝기, 어두운 픽셀 비율, 샘플 색상 수를 분석한다.
- `screen-state.json`에 기대결과, 실제결과, 판단 근거, 분석 값을 함께 저장한다.
- Sprint 2 전체 실행 스크립트 `scripts/run_sprint_2_screen_state.ps1`를 추가했다.

## 최근 검증 결과

기본 테스트:

```text
14 passed, 5 skipped
```

Sprint 2 로컬 테스트:

```text
1 passed
```

TC-005 실행 evidence:

```text
artifacts/evidence/2026-09-01T13-01-10.691+00-00-TC-005
```

저장된 주요 파일:

- `screenshot.png`
- `image-analysis.json`
- `screen-state.json`
- `process-state.json`
- `execution-log.json`

## 다음 작업 후보

1. TC-009 메인 메뉴 진입 확인 기준 수립
2. TC-006 기본 입력 반응 확인 구현
3. 입력 전후 screenshot 비교 기준 정의
4. TC-007 짧은 실행 안정성 확인 구현
5. 사람이 보기 좋은 Markdown 실행 요약 리포트 생성 검토

## 현재 주의할 점

- TC-005는 전체 화면 screenshot을 분석하므로 게임 창이 다른 창에 가려지면 판단이 부정확할 수 있다.
- 아직 게임 창 단독 캡처, UI 텍스트 인식, 메인 메뉴 판별은 구현하지 않았다.
- 하네스와 루프는 아직 적용하지 않는다. 반복 코드와 불안정한 대기가 누적되는 시점에 필요성을 비교한다.
