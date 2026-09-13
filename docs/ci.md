# CI와 실제 게임 검증 분리

GitHub Actions는 Python 의존성 설치와 기본 pytest를 수행한다. 실제 게임 플래그가 없으므로 local_steam 테스트는 NOT_RUN이다. pytest 종료 0과 게임 전체 통과를 구분한다.

`tests/conftest.py`는 artifacts/results/pytest-summary.json과 Markdown을 생성한다. PASS/FAIL/REVIEW_REQUIRED/NOT_RUN을 분리하고 누락 범위가 있으면 INCOMPLETE_OR_FAILED로 표시한다. Unit만 선택한 실행의 SELECTED_TESTS_COMPLETE는 선택된 테스트만 완료했다는 의미이다.

workflow는 JUnit과 artifacts 전체를 실패 시에도 업로드한다. 원격 실행을 확인하지 않았다면 workflow 파일 구성만 완료로 기록한다. 화면 관찰은 Windows 로컬에서 별도로 수행한다.

현재 문서의 실행 수치와 원격 검증 여부는 [진행 상태](progress.md), [완성도](completion-review.md)를 참조한다.
