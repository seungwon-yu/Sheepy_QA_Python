# Evidence 샘플

## 목적

이 문서는 `artifacts/evidence/`에 생성되는 로컬 실행 산출물이 어떤 의미를 가지는지 빠르게 보여주기 위한 샘플 문서이다.

`artifacts/`는 실행 PC의 Steam 상태, 화면 해상도, 실행 시각에 따라 달라지는 로컬 결과물이므로 저장소에는 포함하지 않는다. 대신 이 문서에 대표 TC의 evidence 구조와 판단 근거 예시를 남긴다.

## 공통 evidence 구조

각 TC는 가능한 경우 독립 실행 폴더를 생성한다.

```text
artifacts/evidence/<timestamp>-TC-xxx/
├─ judgement.json
├─ process-state.json
├─ execution-log.json
├─ screen-analysis.json
├─ image-diff.json
├─ foreground-window.json
└─ *.png
```

모든 TC가 모든 파일을 저장하지는 않는다. 예를 들어 프리즈 감지는 `freeze-summary.json`과 연속 screenshot을 저장하고, 입력 반응 테스트는 입력 전후 screenshot과 image diff를 저장한다.

## judgement.json 기준

`judgement.json`은 자동화 결과를 단순 PASS/FAIL로만 남기지 않고 아래 조건을 분리한다.

| 항목 | 의미 |
| --- | --- |
| `actionPerformed` | 자동화가 의도한 동작을 실제로 수행했는지 |
| `expectedSignals` | 기대결과를 지지하는 관찰 신호 |
| `forbiddenSignals` | 발생하면 안 되는 이상 신호 |
| `blockingConditions` | 제품 결함 판단 전에 만족해야 하는 사전조건 |
| `judgementBasis` | 사람이 읽는 판단 근거 요약 |

사전조건이나 관찰 근거가 부족하면 제품 결함으로 단정하지 않고 `REVIEW_REQUIRED`로 기록한다.

## 대표 샘플 1: TC-010 플레이 화면 진입

목적: 로비 CTA에서 Enter 입력 후 플레이 화면 후보로 전환되는지 확인한다.

대표 evidence:

```text
before-gameplay-entry.png
after-gameplay-entry.png
before-lobby-menu-analysis.json
after-lobby-menu-analysis.json
transition-diff.json
gameplay-screen.json
entry-input-log.json
judgement.json
```

대표 판단값:

```json
{
  "result": "PASS",
  "expectedResult": "GAMEPLAY_SCREEN_CANDIDATE",
  "actualResult": "GAMEPLAY_SCREEN_CANDIDATE",
  "actionPerformed": true
}
```

핵심 근거:

| 기준 | 기대 | 실제 |
| --- | --- | --- |
| 로비 진입 CTA 표시 | Continue 또는 Start Your Journey | `LOBBY_MENU_WITH_CONTINUE_AND_START` |
| 입력 후 플레이 화면 후보 | `GAMEPLAY_SCREEN_CANDIDATE` | `GAMEPLAY_SCREEN_CANDIDATE` |
| 로비 대비 화면 변화량 | `changedPixelRatio >= 0.05` | `0.5194` |
| 언어 선택 화면 잔류 | false | false |
| 검은 화면 지속 | false | false |

해석:

```text
로비 CTA가 사라졌고 입력 전후 화면 변화와 충분한 시각 정보가 관찰되었다.
```

## 대표 샘플 2: TC-019 로비 CTA 상태

목적: 언어 선택 이후 로비 화면에서 Continue와 Start Your Journey 후보 영역이 관찰되는지 확인한다.

대표 evidence:

```text
lobby-menu.png
screen-analysis.json
language-screen-analysis.json
post-language-screen.json
lobby-menu-analysis.json
judgement.json
```

대표 판단값:

```json
{
  "result": "PASS",
  "expectedResult": "LOBBY_MENU_WITH_CONTINUE_AND_START",
  "actualResult": "LOBBY_MENU_WITH_CONTINUE_AND_START",
  "actionPerformed": true
}
```

핵심 근거:

| 기준 | 기대 | 실제 |
| --- | --- | --- |
| 언어 선택 이후 화면 상태 | `POST_LANGUAGE_SCREEN` | `POST_LANGUAGE_SCREEN` |
| Continue CTA 표시 | true | true |
| Start Your Journey CTA 표시 | true | true |
| 언어 선택 화면 잔류 | false | false |
| 검은 화면 지속 | false | false |

해석:

```text
Continue와 Start Your Journey 후보 영역에서 메뉴 텍스트 신호가 모두 관찰되었다.
```

## 대표 샘플 3: TC-012 프리즈 감지

목적: 일정 시간 동안 연속 screenshot을 비교해 화면이 멈춘 것으로 볼 근거가 있는지 확인한다.

대표 evidence:

```text
freeze-sample-00.png
freeze-sample-01.png
freeze-sample-02.png
freeze-sample-03.png
freeze-diff-00-01.json
freeze-diff-01-02.json
freeze-diff-02-03.json
freeze-summary.json
final-process-state.json
judgement.json
```

대표 판단값:

```json
{
  "comparisonCount": 3,
  "visibleChangeCount": 3,
  "maxChangedPixelRatio": 0.0062,
  "averageChangedPixelRatio": 0.0043,
  "resultState": "FREEZE_NOT_DETECTED"
}
```

핵심 근거:

| 기준 | 기대 | 실제 |
| --- | --- | --- |
| 비교 가능한 screenshot 쌍 | 1개 이상 | 3 |
| 관찰 중 화면 변화 | `visibleChangeCount >= 1` | 3 |
| 프로세스 종료 | false | false |
| Sheepy process detected | true | true |
| Sheepy window detected | true | true |

해석:

```text
연속 screenshot 비교에서 화면 변화가 관찰되어 프리즈로 판단하지 않는다.
```

## 이미지 기반 판정의 방어 논리

이 프로젝트는 실제 Steam 게임을 외부에서 관찰하는 방식이므로, 내부 좌표나 UI 텍스트를 완전히 읽지 못한다.

따라서 이미지 기반 판정은 제품 결함을 단정하는 단독 근거가 아니라, 아래 조건과 함께 해석한다.

- 게임 프로세스가 살아 있는가
- 대상 게임 창을 찾았는가
- foreground window가 테스트 대상인가
- screenshot이 저장되었는가
- 기대 신호와 이상 신호가 분리되어 기록되었는가
- 근거가 부족할 때 `REVIEW_REQUIRED`로 빠지는가

면접에서는 “픽셀 변화만으로 충분하다”가 아니라, “외부 관찰 자동화의 한계를 인정하고 오판을 줄이기 위해 사전조건, 기대 신호, 이상 신호, 검토 필요 상태를 분리했다”라고 설명하는 것이 좋다.
