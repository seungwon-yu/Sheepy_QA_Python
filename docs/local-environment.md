# 로컬 Python 실행 환경

## 목적

이 문서는 `pytest` 또는 `python` 명령이 PC마다 다르게 동작하는 문제를 줄이기 위한 실행 기준을 정리한다.

Windows에서는 Python이 설치되어 있어도 `python`, `py`, `pytest` 명령이 모두 같은 방식으로 등록되지 않을 수 있다. 따라서 이 프로젝트는 가상환경을 만들고 `python -m pytest`로 실행하는 방식을 권장한다.

## 권장 환경

| 항목 | 기준 |
| --- | --- |
| OS | Windows 10 이상 |
| Python | 3.11 이상 |
| Shell | Windows PowerShell |
| 대상 게임 | Steam 버전 `Sheepy: A Short Adventure` |
| 로컬 게임 테스트 | Steam 로그인, 게임 설치, GUI 세션 필요 |

## 처음 실행

PowerShell에서 프로젝트 폴더로 이동한 뒤 실행한다.

```powershell
cd .\Sheepy_QA_Python
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest
```

`py` 런처가 없다면 설치된 Python 실행 파일로 가상환경을 만든다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest
```

## pytest를 직접 실행하지 않는 이유

아래 명령은 환경에 따라 실패할 수 있다.

```powershell
pytest
```

이유:

- `pytest.exe`가 PATH에 등록되지 않았을 수 있다.
- 전역 Python과 가상환경 Python이 다를 수 있다.
- Microsoft Store용 `python.exe` 별칭이 먼저 잡힐 수 있다.

그래서 아래 명령을 기본으로 사용한다.

```powershell
python -m pytest
```

이 방식은 현재 활성화된 가상환경의 Python이 설치된 pytest 모듈을 실행하게 한다.

## 로컬 Steam 테스트

실제 Steam 게임 실행이 필요한 테스트는 기본 pytest에서는 skip된다.

실행 조건:

- Steam 설치
- Steam 로그인
- Sheepy 설치
- 게임 창을 띄울 수 있는 Windows GUI 세션
- 테스트 중 게임 창이 다른 창에 가려지지 않는 상태

실행:

```powershell
$env:SHEEPY_RUN_STEAM_TESTS = "1"
python -m pytest tests/local
```

개별 TC는 `scripts/` 아래 PowerShell 스크립트로 실행할 수 있다.

```powershell
.\scripts\run_tc_010_gameplay_entry.ps1
.\scripts\run_tc_012_freeze_detection.ps1
.\scripts\run_tc_019_lobby_menu_options.ps1
```

## CI와 다른 점

GitHub Actions CI는 실제 Steam 테스트를 실행하지 않는다.

CI는 다음 범위만 확인한다.

- 의존성 설치
- import 오류
- 실제 Steam 없이 실행 가능한 unit test
- pytest 결과 artifact 생성

실제 게임 실행, 화면 캡처, 키보드 입력, 프리즈 관찰은 로컬 QA 범위이다.

## 문제 해결

### python 명령이 Microsoft Store로 연결되는 경우

Windows 설정에서 App execution aliases의 `python.exe`, `python3.exe` 별칭을 끄거나, Python 공식 설치 경로의 실행 파일을 직접 사용한다.

예:

```powershell
C:\Users\<user>\AppData\Local\Programs\Python\Python312\python.exe -m venv .venv
```

### Activate.ps1 실행이 막히는 경우

현재 PowerShell 세션에만 실행 정책을 완화한다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 로컬 Steam 테스트가 REVIEW_REQUIRED로 끝나는 경우

우선 아래 evidence를 확인한다.

```text
window-search.json
focused-window.json
foreground-window.json
judgement.json
```

게임 창을 찾지 못했거나 foreground가 아니면 제품 결함이 아니라 테스트 환경 또는 관찰 조건 문제일 수 있다.
