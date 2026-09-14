# 기준→TC→구현→실행 추적

[테스트 기준](test-basis-and-standards.md), [상세 TC](test-cases.md), [최신 결과](progress.md)를 연결한다. 구현과 실제 게임 통과는 다른 상태이다.

| TC | 분류 | 관찰 목적 | 구현 | 구현 상태 | 검증 상태 |
| --- | --- | --- | --- | --- | --- |
| TC-001 | 환경 | Steam 실행/경로 신호 | [코드](../tests\local\test_tc_001_004_local_steam.py) | 구현됨 | PASS ([기동 기록](local-verification.md)) |
| TC-002 | 실행 | AppID 실행 명령 | [코드](../tests\local\test_tc_001_004_local_steam.py) | 구현됨 | PASS ([기동 기록](local-verification.md)) |
| TC-003 | 실행 | 프로세스 감지 | [코드](../tests\local\test_tc_001_004_local_steam.py) | 구현됨 | 수동 실행 후 감지 PASS / 자동 기동 이전 FAIL ([기동 기록](local-verification.md)) |
| TC-004 | 화면 | 초기 캡처 | [코드](../tests\local\test_tc_001_004_local_steam.py) | 구현됨 | PASS (desktop; sandbox FAIL 보존) ([진단](live-validation-2026-09-14.md)) |
| TC-005 | 화면 | 검은 화면 후보 | [코드](../tests\local\test_tc_005_screen_state.py) | 구현됨 | 수정 후 실제 게임 미실행 |
| TC-006 | 입력 | Space 시각 반응 | [코드](../tests\local\test_tc_018_006_011_post_language_input.py) | 구현됨 | REVIEW_REQUIRED (최초 FAIL 보존) ([진단](live-validation-2026-09-14.md)) |
| TC-007 | 안정성 | 짧은 실행 관찰 | [코드](../tests\local\test_tc_007_short_stability.py) | 구현됨 | PASS (수정 전 관찰; 최신 캡처 재검증 필요) ([진단](live-validation-2026-09-14.md)) |
| TC-008 | 도구 | evidence 파일 저장 | [코드](../tests\local\..\unit\test_evidence_validation.py) | 구현됨 | 도구 검증 통과 |
| TC-009 | 화면 | 언어 선택 후보 | [코드](../tests\local\test_tc_009_017_language_selection.py) | 구현됨 | 수정 후 실제 게임 미실행 |
| TC-010 | 진입 | 플레이 화면 후보 전환 | [코드](../tests\local\test_tc_010_gameplay_entry.py) | 구현됨 | 최신 REVIEW_REQUIRED: 실행 중 캡처 크기 변경, 예외 전 이벤트 유실 확인 ([진단](live-validation-2026-09-14.md)) |
| TC-011 | 입력 | 방향키 시각 반응 | [코드](../tests\local\test_tc_018_006_011_post_language_input.py) | 구현됨 | 수정 후 실제 게임 미실행 |
| TC-012 | 안정성 | 연속 화면 변화 관찰 | [코드](../tests\local\test_tc_012_freeze_detection.py) | 구현됨 | PASS (수정 전 관찰; 최신 캡처 재검증 필요) ([진단](live-validation-2026-09-14.md)) |
| TC-013 | 유저 상태 | 최초 실행 후보 | [코드](../tests\local\test_tc_013_014_015_016_player_save_gameplay.py) | 구현됨 | 수정 후 실제 게임 미실행 |
| TC-014 | 유저 상태 | 기존 플레이 후보 | [코드](../tests\local\test_tc_013_014_015_016_player_save_gameplay.py) | 구현됨 | 수정 후 실제 게임 미실행 |
| TC-015 | 저장 | 파일 경로 유지 | [코드](../tests\local\test_tc_013_014_015_016_player_save_gameplay.py) | 구현됨 | 수정 후 실제 게임 미실행 |
| TC-016 | 입력 | 복합 입력 시각 반응 | [코드](../tests\local\test_tc_013_014_015_016_player_save_gameplay.py) | 구현됨 | 수정 후 실제 게임 미실행 |
| TC-017 | 입력 | 언어 선택 입력 반응 | [코드](../tests\local\test_tc_009_017_language_selection.py) | 구현됨 | 수정 후 실제 게임 미실행 |
| TC-018 | 화면 | 언어 이후 후보 | [코드](../tests\local\test_tc_018_006_011_post_language_input.py) | 구현됨 | 수정 후 실제 게임 미실행 |
| TC-019 | 화면 | 기존 유저 로비 CTA 후보 | [코드](../tests\local\test_tc_019_lobby_menu_options.py) | 주변 대비 판정 보완 | 수정 후 실제 PASS 1회, 3회 반복 미완료 ([진단](live-validation-2026-09-14.md)) |

자동화 상태 준비/판정 함수의 단위 테스트는 제품 TC 통과로 합산하지 않는다. 최신 실제 실행이 추가되면 이 표의 실행 상태와 progress를 함께 갱신한다.
