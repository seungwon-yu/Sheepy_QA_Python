import time
from pathlib import Path

import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.image_diff import compareImages
from sheepy_qa.image_analysis import analyzeImage
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.keyboard_input import pressEnter
from sheepy_qa.language_screen import analyzeLanguageSelectionScreen
from sheepy_qa.local_test_config import shouldRunSteamTests
from sheepy_qa.process_check import findProcessesByName, hasRunningProcess
from sheepy_qa.screen_capture import captureScreenshot, captureWindowScreenshot
from sheepy_qa.steam_app import SteamApp
from sheepy_qa.wait import waitUntil
from sheepy_qa.window_state import clickWindowTitleArea, findWindowByProcessNameFragments, focusWindow, getForegroundWindowTitle


pytestmark = pytest.mark.local_steam


def launchAndWaitForSheepy(writer: EvidenceWriter, runDir: Path) -> bool:
    launchCommand = SteamApp().launch(dryRun=False)
    writer.writeJson(runDir, "execution-log.json", launchCommand)

    matched, processes = waitUntil(
        supplier=lambda: findProcessesByName(["sheepy", "sheepyashortadventure"]),
        predicate=hasRunningProcess,
        timeoutSeconds=60,
        intervalSeconds=1
    )
    writer.writeJson(runDir, "process-state.json", processes)

    time.sleep(1)
    return matched


def focusSheepyWindow(writer: EvidenceWriter, runDir: Path):
    window = findWindowByProcessNameFragments(["sheepyashortadventure"])
    writer.writeJson(
        runDir,
        "window-search.json",
        {
            "expectedTitleFragment": "sheepy",
            "actualWindow": window
        }
    )

    if window is None:
        return None

    focusWindow(window.handle)
    time.sleep(1)
    focusedWindow = findWindowByProcessNameFragments(["sheepyashortadventure"])

    if focusedWindow is not None and focusedWindow.isForeground is False:
        clickWindowTitleArea(focusedWindow)
        time.sleep(1)
        focusedWindow = findWindowByProcessNameFragments(["sheepyashortadventure"])

    writer.writeJson(runDir, "focused-window.json", focusedWindow)
    return focusedWindow


@pytest.mark.tc_009
def test_tc_009_language_selection_screen_is_visible() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-009")
    processMatched = launchAndWaitForSheepy(writer, runDir)
    window = focusSheepyWindow(writer, runDir)

    if window is None:
        captureTarget = "FULL_SCREEN_FALLBACK"
        screenshotPath = captureScreenshot(runDir / "language-selection-screen.png")
    else:
        captureTarget = "SHEEPY_WINDOW"
        screenshotPath = captureWindowScreenshot(window, runDir / "language-selection-screen.png")

    screenAnalysisResult = analyzeImage(screenshotPath)
    analysisResult = analyzeLanguageSelectionScreen(screenshotPath)
    writer.writeJson(runDir, "screen-analysis.json", screenAnalysisResult)
    writer.writeJson(runDir, "language-screen-analysis.json", analysisResult)

    judgementRecord = createJudgementRecord(
        expectedResult="LANGUAGE_SELECTION_SCREEN",
        actualResult="LANGUAGE_SELECTION_SCREEN" if analysisResult.isLanguageSelectionLike else "REVIEW_REQUIRED",
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition(
                name="언어 선택 항목 후보 개수",
                expected="2개 이상",
                actual=analysisResult.visibleOptionCount,
                passed=analysisResult.visibleOptionCount >= 2,
                evidenceKey="language-screen-analysis.json.visibleOptionCount"
            ),
            JudgementCondition(
                name="언어 선택 UI 채도 픽셀 비율",
                expected="0.035 이상",
                actual=analysisResult.centralSaturatedPixelRatio,
                passed=analysisResult.centralSaturatedPixelRatio >= 0.035,
                evidenceKey="language-screen-analysis.json.centralSaturatedPixelRatio"
            ),
            JudgementCondition(
                name="언어 선택 화면의 어두운 배경 비율",
                expected="0.5 이상",
                actual=analysisResult.centralDarkPixelRatio,
                passed=analysisResult.centralDarkPixelRatio >= 0.5,
                evidenceKey="language-screen-analysis.json.centralDarkPixelRatio"
            ),
            JudgementCondition(
                name="전체 화면의 어두운 배경 비율",
                expected="0.7 이상",
                actual=screenAnalysisResult.darkPixelRatio,
                passed=screenAnalysisResult.darkPixelRatio >= 0.7,
                evidenceKey="screen-analysis.json.darkPixelRatio"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="검은 화면 지속",
                expected=False,
                actual=screenAnalysisResult.isMostlyBlack,
                passed=screenAnalysisResult.isMostlyBlack is False,
                evidenceKey="screen-analysis.json.isMostlyBlack"
            )
        ],
        blockingConditions=[
            JudgementCondition(
                name="Sheepy process detected",
                expected=True,
                actual=processMatched,
                passed=processMatched,
                evidenceKey="process-state.json"
            ),
            JudgementCondition(
                name="screenshot capture target",
                expected="SheepyAShortAdventure.exe window",
                actual=captureTarget,
                passed=captureTarget == "SHEEPY_WINDOW" and window.processName.lower() == "sheepyashortadventure.exe",
                evidenceKey="language-selection-screen.png"
            ),
            JudgementCondition(
                name="PLAYER-UNKNOWN 언어 선택 화면 적용 가능성",
                expected="언어 선택 화면이 표시되는 상태",
                actual=analysisResult.isLanguageSelectionLike,
                passed=analysisResult.isLanguageSelectionLike,
                evidenceKey="language-screen-analysis.json.isLanguageSelectionLike"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    if judgementRecord.result == "REVIEW_REQUIRED":
        pytest.xfail(judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"


@pytest.mark.tc_017
def test_tc_017_language_selection_enter_input_changes_screen() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-017")
    processMatched = launchAndWaitForSheepy(writer, runDir)
    window = focusSheepyWindow(writer, runDir)

    if window is None:
        captureTarget = "FULL_SCREEN_FALLBACK"
        beforeImagePath = captureScreenshot(runDir / "before-language-input.png")
    else:
        captureTarget = "SHEEPY_WINDOW"
    beforeImagePath = captureWindowScreenshot(window, runDir / "before-language-input.png")

    beforeLanguageAnalysis = analyzeLanguageSelectionScreen(beforeImagePath)
    beforeWindowTitle = getForegroundWindowTitle()
    inputTargetConfirmed = window.isForeground and window.processName.lower() == "sheepyashortadventure.exe"

    if inputTargetConfirmed:
        pressEnter()
        actionPerformed = True
    else:
        actionPerformed = False

    time.sleep(2)

    if window is None:
        afterImagePath = captureScreenshot(runDir / "after-language-input.png")
    else:
        afterImagePath = captureWindowScreenshot(window, runDir / "after-language-input.png")

    afterWindowTitle = getForegroundWindowTitle()
    diffResult = compareImages(beforeImagePath, afterImagePath)

    writer.writeJson(
        runDir,
        "foreground-window.json",
        {
            "beforeWindowTitle": beforeWindowTitle,
            "afterWindowTitle": afterWindowTitle
        }
    )
    writer.writeJson(
        runDir,
        "input-log.json",
        {
            "input": "ENTER",
            "playerState": "PLAYER-UNKNOWN",
            "expectedResult": "화면 전환 또는 명확한 화면 변화",
            "actualResult": "화면 변화 있음" if diffResult.hasVisibleChange else "화면 변화 부족",
            "actionPerformed": actionPerformed,
            "captureTarget": captureTarget,
            "judgementBasis": [
                "입력 전후 screenshot의 픽셀 차이 비율이 기준값 이상이어야 한다.",
                "입력은 현재 foreground window에 전달되므로 foreground-window.json을 함께 확인한다.",
                "언어 선택 화면이 기존 플레이 유저에게도 재노출되는지는 별도 확인이 필요하다."
            ]
        }
    )
    writer.writeJson(runDir, "before-language-screen-analysis.json", beforeLanguageAnalysis)
    writer.writeJson(runDir, "image-diff.json", diffResult)
    judgementRecord = createJudgementRecord(
        expectedResult="LANGUAGE_SELECTION_INPUT_RESPONSE",
        actualResult="화면 변화 있음" if diffResult.hasVisibleChange else "화면 변화 부족",
        actionPerformed=actionPerformed,
        expectedSignals=[
            JudgementCondition(
                name="입력 전후 화면 변화",
                expected="changedPixelRatio >= 0.01",
                actual=diffResult.changedPixelRatio,
                passed=diffResult.hasVisibleChange,
                evidenceKey="image-diff.json.changedPixelRatio"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="입력 전후 완전 동일 화면",
                expected=False,
                actual=diffResult.changedPixelRatio == 0,
                passed=diffResult.changedPixelRatio > 0,
                evidenceKey="image-diff.json.changedPixelRatio"
            )
        ],
        blockingConditions=[
            JudgementCondition(
                name="Sheepy process detected",
                expected=True,
                actual=processMatched,
                passed=processMatched,
                evidenceKey="process-state.json"
            ),
            JudgementCondition(
                name="입력 대상 확인",
                expected="Sheepy foreground window",
                actual={
                    "beforeWindowTitle": beforeWindowTitle,
                    "sheepyWindowTitle": window.title,
                    "sheepyProcessName": window.processName,
                    "isSheepyForeground": window.isForeground,
                    "isLanguageSelectionLike": beforeLanguageAnalysis.isLanguageSelectionLike
                },
                passed=inputTargetConfirmed,
                evidenceKey="foreground-window.json, before-language-screen-analysis.json"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    if judgementRecord.result == "REVIEW_REQUIRED":
        pytest.xfail(judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"
