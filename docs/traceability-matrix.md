# 추적 매트릭스

## 목적

이 문서는 테스트 기준, 대분류, 소분류, TC가 어떻게 연결되는지 보여준다.

새 TC를 추가할 때는 반드시 이 문서에 연결 관계를 갱신한다.

## 기준별 대분류 연결

| 기준 | 적용 대분류 |
| --- | --- |
| ISTQB Foundation - 테스트 베이시스 | 전체 대분류 |
| ISTQB Foundation - 테스트 조건 | 전체 대분류 |
| ISTQB Foundation - 기대결과 | 전체 TC |
| ISTQB Foundation - 리스크 기반 우선순위 | TC-GROUP-01, TC-GROUP-02, TC-GROUP-07 |
| ISTQB Foundation - 결함 보고와 evidence | TC-GROUP-08 |
| ISTQB Game Testing - Game Product Risks | TC-GROUP-01, TC-GROUP-02, TC-GROUP-07 |
| ISTQB Game Testing - Game Mechanics Testing | TC-GROUP-04, TC-GROUP-05 |
| ISTQB Game Testing - Graphics Testing | TC-GROUP-03, TC-GROUP-06 |
| ISTQB Game Testing - Game Level Testing | TC-GROUP-05 |
| ISTQB Game Testing - Game Controllers Testing | TC-GROUP-04 |
| ISTQB Game Testing - Save Data and Player Progression Risk | TC-GROUP-03, TC-GROUP-05, 저장/로드 |

## TC 추적표

| TC ID | 대분류 | 소분류 | 주요 기준 | 우선순위 | 자동화 방식 |
| --- | --- | --- | --- | --- | --- |
| TC-001 | 설치 및 실행 환경 | TC-01-A Steam 환경 | 테스트 환경, 플랫폼 리스크 | High | 프로세스/경로 확인 |
| TC-002 | 실행/종료 | TC-02-A 게임 실행 | 기능 테스트, 실행 리스크 | High | Steam AppID 실행 |
| TC-003 | 실행/종료 | TC-02-B 프로세스 감지 | 기대결과, 프로세스 evidence | High | psutil 프로세스 확인 |
| TC-004 | 메인 화면 및 초기 진입 | TC-03-C 화면 캡처 | 관찰 가능한 결과, 그래픽 evidence | High | screenshot 저장 |
| TC-005 | 화면/그래픽 표시 | TC-06-A 검은 화면 감지 | Graphics Testing, 진행 불가 리스크 | High | screenshot 밝기와 픽셀 분포 분석 |
| TC-006 | 입력 반응 | TC-04-B 점프 입력 | Controller Testing, 게임 메커닉 | Medium | 입력 전후 이미지 비교 |
| TC-007 | 안정성/크래시/프리즈 | TC-07-C 짧은 안정성 | 신뢰성, 크래시 리스크 | High | 프로세스 타임라인 |
| TC-008 | Evidence 및 리포트 | TC-08-A/B/C | 결함 보고, evidence | High | 파일 생성 확인 |
| TC-009 | 메인 화면 및 초기 진입 | TC-03-D 언어 선택 화면 | 초기 진입 화면, 관찰 가능한 결과 | High | 창 캡처와 언어 선택 UI 이미지 분석 |
| TC-011 | 입력 반응 | TC-04-A 이동 입력 | Controller Testing, 게임 메커닉 | Medium | 무입력 변화량과 입력 후 이미지 변화량 비교 |
| TC-014 | 메인 화면 및 초기 진입 | TC-03-A 초기 화면 도달 | 최초 실행 상태, 테스트 데이터 | Medium | 후속 구현 |
| TC-015 | 메인 화면 및 초기 진입 | TC-03-B 메뉴 표시 | 기존 플레이 상태, 저장 상태 복구 | Medium | 후속 구현 |
| TC-016 | 저장/로드 | 후속 확장 | 세이브 데이터 보존, 리그레션 리스크 | High | 후속 구현 |
| TC-017 | 입력 반응 | TC-04-D 언어 선택 입력 | Controller Testing, 상태 전이 | High | foreground 확인 후 Enter 입력과 이미지 차이 분석 |
| TC-018 | 메인 화면 및 초기 진입 | TC-03-E 언어 선택 이후 화면 | 상태 전이 후 화면 확인, 그래픽 evidence | High | 창 캡처와 언어 선택 이후 화면 분류 |

## 대분류에서 TC로 내려가는 방식

```text
기준
↓
대분류
↓
소분류
↓
테스트 조건
↓
TC
↓
기대결과
↓
Evidence
```

예시:

```text
ISTQB Game Testing - Game Controllers Testing
↓
TC-GROUP-04 입력 반응
↓
TC-04-B 점프 입력
↓
점프 키 입력 전후 화면 변화 확인
↓
TC-006 기본 입력 반응 확인
↓
입력 전후 화면 차이가 기준값 이상이어야 함
↓
before-input.png, after-input.png, image-diff.json
```
