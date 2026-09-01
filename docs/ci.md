# CI 구성

## 목적

CI는 GitHub에 올라간 코드가 깨끗한 환경에서도 정상적으로 설치되고 테스트되는지 확인하기 위한 자동 검증이다.

이번 프로젝트는 실제 Steam 게임을 대상으로 하지만, GitHub Actions runner에는 Steam 클라이언트와 Sheepy 게임이 설치되어 있지 않다.

따라서 CI는 실제 게임 실행 QA가 아니라 자동화 코드의 기본 안정성을 확인하는 범위로 제한한다.

## CI에서 확인하는 것

| 항목 | 설명 |
| --- | --- |
| Python 환경 | 지정한 Python 버전에서 프로젝트가 실행 가능한지 확인 |
| 의존성 설치 | `requirements.txt` 기준으로 패키지가 설치되는지 확인 |
| import 오류 | `src/sheepy_qa` 모듈을 테스트에서 정상 import할 수 있는지 확인 |
| 단위 테스트 | 실제 Steam 실행 없이 검증 가능한 유틸 테스트 실행 |
| 테스트 결과 산출물 | pytest JUnit XML 결과를 artifact로 저장 |

## CI에서 확인하지 않는 것

| 항목 | 이유 |
| --- | --- |
| Steam 실행 | GitHub Actions runner에는 Steam 클라이언트가 없음 |
| Sheepy 설치 확인 | runner에는 대상 게임이 설치되어 있지 않음 |
| 실제 게임 화면 캡처 | GUI 게임 화면과 로컬 디스플레이가 필요함 |
| 실제 입력 반응 | 키보드/마우스 입력 대상 게임 창이 필요함 |

## 실행 시점

CI는 다음 상황에서 실행된다.

- `main` 브랜치에 push
- `main` 브랜치를 대상으로 pull request 생성 또는 갱신

## 실행 흐름

```text
GitHub push 또는 pull request
↓
actions/checkout
↓
actions/setup-python
↓
python -m pip install -r requirements.txt
↓
python -m pytest
↓
pytest 결과 artifact 업로드
```

## 로컬 QA와 CI의 역할 분리

| 구분 | 역할 |
| --- | --- |
| CI | 코드 오류, import 오류, 유틸 테스트 실패 확인 |
| 로컬 QA | Steam 실행, 실제 게임 화면, 입력 반응, screenshot evidence 확인 |

기본 `pytest` 실행 시 로컬 Steam 테스트는 `SHEEPY_RUN_STEAM_TESTS=1`이 없으면 skip된다.

CI에서는 이 환경 변수를 설정하지 않으므로 실제 Steam 실행 테스트는 수행하지 않는다.

로컬 Steam 테스트는 Windows PowerShell에서 다음 스크립트로 실행한다.

```powershell
.\scripts\run_local_steam_tests.ps1
```

## 실패 해석 기준

CI 실패는 곧바로 게임 제품 버그를 의미하지 않는다.

| 실패 위치 | 우선 분류 |
| --- | --- |
| 의존성 설치 실패 | `ENV_FAIL` |
| import 실패 | `TEST_FAIL` 또는 `ENV_FAIL` |
| 순수 유틸 테스트 실패 | `TEST_FAIL` 후보 |
| artifact 업로드 실패 | `ENV_FAIL` 후보 |

실패 원인이 명확하지 않으면 `REVIEW_REQUIRED`로 남기고 로그를 확인한다.
