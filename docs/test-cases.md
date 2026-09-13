# 테스트 케이스: 관찰 계약

모든 TC는 관찰한 신호의 범위에서만 판정한다. 실제 게임 버전/환경/결과는 [진행 상태](progress.md)에 별도로 기록한다. TC-008은 제품 TC가 아닌 도구 검증이다.

## TC-001 Steam 실행/경로 신호

| 항목 | 기준 |
| --- | --- |
| 분류 | 환경 |
| 베이시스 | Steam 실행/경로 신호 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | Steam 설치 환경 |
| 절차 | snapshot 수집 |
| 기대결과 | Steam 경로 또는 프로세스 신호 |
| 한계 | 프로세스/경로는 로그인·게임 설치 성공을 보장하지 않음 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_001_004_local_steam.py) |

## TC-002 AppID 실행 명령

| 항목 | 기준 |
| --- | --- |
| 분류 | 실행 |
| 베이시스 | AppID 실행 명령 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | Steam 실행 가능 |
| 절차 | Steam URI 호출 |
| 기대결과 | AppID 1568400 명령 실행 |
| 한계 | 게임 정상 기동은 TC-003/004 별도 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_001_004_local_steam.py) |

## TC-003 프로세스 감지

| 항목 | 기준 |
| --- | --- |
| 분류 | 실행 |
| 베이시스 | 프로세스 감지 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 게임 실행 시도 후 |
| 절차 | 제한 시간 프로세스 탐색 |
| 기대결과 | Sheepy 프로세스 발견 |
| 한계 | 응답성은 별도 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_001_004_local_steam.py) |

## TC-004 초기 캡처

| 항목 | 기준 |
| --- | --- |
| 분류 | 화면 |
| 베이시스 | 초기 캡처 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 게임 화면을 볼 수 있음 |
| 절차 | screenshot 저장 |
| 기대결과 | 파일 생성 |
| 한계 | 전체 화면 캡처이며 게임 내용 정상성은 별도 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_001_004_local_steam.py) |

## TC-005 검은 화면 후보

| 항목 | 기준 |
| --- | --- |
| 분류 | 화면 |
| 베이시스 | 검은 화면 후보 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 게임 표시·가림 없음 |
| 절차 | 밝기/픽셀 분포 분석 |
| 기대결과 | 검은 화면 기준 미해당 |
| 한계 | 어두운 정상 장면/다른 창 오탐 가능 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_005_screen_state.py) |

## TC-006 Space 시각 반응

| 항목 | 기준 |
| --- | --- |
| 분류 | 입력 |
| 베이시스 | Space 시각 반응 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 로비에서 준비 가능한 게임 |
| 절차 | GAMEPLAY 후보 준비→무입력→Space→비교 |
| 기대결과 | 변화량 차이 >=0.005 |
| 한계 | 점프 자체 확정 아님 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_018_006_011_post_language_input.py) |

## TC-007 짧은 실행 관찰

| 항목 | 기준 |
| --- | --- |
| 분류 | 안정성 |
| 베이시스 | 짧은 실행 관찰 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 게임 실행·창 관찰 |
| 절차 | 30초 프로세스/캡처 관찰 |
| 기대결과 | 프로세스 유지·캡처 성공 |
| 한계 | 장시간 안정성 보장 아님 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_007_short_stability.py) |

## TC-008 evidence 파일 저장

| 항목 | 기준 |
| --- | --- |
| 분류 | 도구 |
| 베이시스 | evidence 파일 저장 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 임시 evidence 디렉터리 |
| 절차 | 필수 파일 존재/크기 검사 |
| 기대결과 | 파일 존재·비어 있지 않음 |
| 한계 | 제품 TC가 아닌 도구 검증 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\..\unit\test_evidence_validation.py) |

## TC-009 언어 선택 후보

| 항목 | 기준 |
| --- | --- |
| 분류 | 화면 |
| 베이시스 | 언어 선택 후보 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 언어 화면이 표시되는 실행 상태 |
| 절차 | 창 캡처·언어 UI 후보 분석 |
| 기대결과 | 언어 화면 특징 충족 |
| 한계 | 문구를 OCR로 읽는 것이 아님 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_009_017_language_selection.py) |

## TC-010 플레이 화면 후보 전환

| 항목 | 기준 |
| --- | --- |
| 분류 | 진입 |
| 베이시스 | 플레이 화면 후보 전환 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 지원 가능한 로비 |
| 절차 | 로비 확인→Enter→변화 관찰 |
| 기대결과 | 로비 CTA 소멸·플레이 후보 |
| 한계 | 실제 조작 가능은 별도 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_010_gameplay_entry.py) |

## TC-011 방향키 시각 반응

| 항목 | 기준 |
| --- | --- |
| 분류 | 입력 |
| 베이시스 | 방향키 시각 반응 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 로비에서 준비 가능한 게임 |
| 절차 | GAMEPLAY 준비→무입력→Right/Left→비교 |
| 기대결과 | 변화량 차이 >=0.005 |
| 한계 | 실제 좌표 이동 확정 아님 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_018_006_011_post_language_input.py) |

## TC-012 연속 화면 변화 관찰

| 항목 | 기준 |
| --- | --- |
| 분류 | 안정성 |
| 베이시스 | 연속 화면 변화 관찰 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 관찰 가능한 게임 창 |
| 절차 | 20초·5초 간격 캡처·실제 시각 기록 |
| 기대결과 | 화면 변화 및 연속 무변화 10초 미만 |
| 한계 | 정적 장면이면 보류; 내부 프리즈 부재 확정 아님 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_012_freeze_detection.py) |

## TC-013 최초 실행 후보

| 항목 | 기준 |
| --- | --- |
| 분류 | 유저 상태 |
| 베이시스 | 최초 실행 후보 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 사람이 준비한 NEW 로비 |
| 절차 | CTA 관찰 |
| 기대결과 | Start 후보 있음·Continue 없음 |
| 한계 | 기존 세이브 삭제로 준비하지 않음 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_013_014_015_016_player_save_gameplay.py) |

## TC-014 기존 플레이 후보

| 항목 | 기준 |
| --- | --- |
| 분류 | 유저 상태 |
| 베이시스 | 기존 플레이 후보 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 사람이 준비한 RETURNING 로비 |
| 절차 | CTA 관찰 |
| 기대결과 | Continue 후보 있음 |
| 한계 | 저장 내용 복원 성공은 별도 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_013_014_015_016_player_save_gameplay.py) |

## TC-015 파일 경로 유지

| 항목 | 기준 |
| --- | --- |
| 분류 | 저장 |
| 베이시스 | 파일 경로 유지 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 관찰 가능한 저장 후보 파일 |
| 절차 | 전후 파일 목록 비교 |
| 기대결과 | SAVE_FILES_PRESENT |
| 한계 | 내용 무결성·진행 복원 미검증 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_013_014_015_016_player_save_gameplay.py) |

## TC-016 복합 입력 시각 반응

| 항목 | 기준 |
| --- | --- |
| 분류 | 입력 |
| 베이시스 | 복합 입력 시각 반응 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 로비에서 준비 가능한 게임 |
| 절차 | GAMEPLAY 준비→무입력→방향키/Space |
| 기대결과 | 변화량 차이 >=0.005 |
| 한계 | 이동/점프 각각의 성공은 별도 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_013_014_015_016_player_save_gameplay.py) |

## TC-017 언어 선택 입력 반응

| 항목 | 기준 |
| --- | --- |
| 분류 | 입력 |
| 베이시스 | 언어 선택 입력 반응 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 언어 화면과 foreground 확인 |
| 절차 | Enter 전후 이미지 비교 |
| 기대결과 | 화면 변화 |
| 한계 | 다음 화면 정상성은 별도 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_009_017_language_selection.py) |

## TC-018 언어 이후 후보

| 항목 | 기준 |
| --- | --- |
| 분류 | 화면 |
| 베이시스 | 언어 이후 후보 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | 게임 창 관찰 |
| 절차 | POST_LANGUAGE 준비·관찰 |
| 기대결과 | 검은 화면·언어 특징 없음 |
| 한계 | 로비/플레이를 확정하지 않음 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_018_006_011_post_language_input.py) |

## TC-019 기존 유저 로비 CTA 후보

| 항목 | 기준 |
| --- | --- |
| 분류 | 화면 |
| 베이시스 | 기존 유저 로비 CTA 후보 관련 관찰 가능한 신호; 내부 공식 요구사항 아님 |
| 사전조건 | RETURNING 로비 |
| 절차 | LOBBY 준비·영역 분석 |
| 기대결과 | Continue/Start 후보 둘 다 있음 |
| 한계 | 문구 OCR·선택 CTA 확정 아님 |
| Evidence | judgement.json과 해당 분석/입력/프로세스 기록; 준비 TC는 preparation.json |
| 실패 처리 | 사전조건 부족=REVIEW_REQUIRED, 신호 실패=FAIL 후 사람 원인 검토 |
| 구현 | [코드](../tests\local\test_tc_019_lobby_menu_options.py) |
