# Windows 실행 환경

Python 3.11 이상, Steam 설치/로그인, Sheepy 설치, 대화형 데스크톱이 실제 게임 테스트에 필요하다. 게임 없는 단위 테스트는 Linux에서도 실행한다. 실제 환경값은 [환경 프로필](environment-profile.md)에 기록한다.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest tests/unit
```

가상환경 Python을 직접 사용하므로 Activate.ps1과 실행 정책 변경이 필수가 아니다. py가 없으면 설치한 python.exe 전체 경로를 사용한다. `pytest` 단독 명령의 PATH 오류를 제품 문제로 보지 않는다.

게임 창 크기·디스플레이 배율·창 가림·foreground는 이미지 기준에 영향을 준다. 창 캡처는 화면 영역을 캡처하므로 다른 창에 가려지면 영향을 받을 수 있다. TC-004/005의 전체 화면 관찰도 별도 제한이다.

로컬 결과는 artifacts/evidence, 집계는 artifacts/results에 있다. 창 탐지 실패는 프로세스 이름·window-search·preparation을 함께 검토한다. 기본 Steam 경로 외 설치와 실행 감지는 TC-001의 환경 관찰 범위이며 게임 설치/로그인 성공을 자동 확정하지 않는다.

Steam 환경 snapshot은 기본 경로·프로세스 외 steam:// protocol 등록 명령도 읽는다. 등록 신호가 로그인·실제 실행 성공을 보장하지 않으며 해당 명령을 실행하는 검사도 아니다.
