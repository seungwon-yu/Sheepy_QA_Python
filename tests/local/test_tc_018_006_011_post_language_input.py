import time
from pathlib import Path
from typing import Callable

import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.image_analysis import analyzeImage
from sheepy_qa.image_diff import compareImages
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.keyboard_input import pressLeft, pressRight, pressSpace
from sheepy_qa.language_screen import analyzeLanguageSelectionScreen
from sheepy_qa.local_test_config import shouldRunSteamTests
from sheepy_qa.post_language_screen import classifyPostLanguageScreen
from sheepy_qa.process_check import findProcessesByName, hasRunningProcess
from sheepy_qa.screen_capture import captureWindowScreenshot
from sheepy_qa.wait import waitUntil
from sheepy_qa.window_state import clickWindowTitleArea, findWindowByProcessNameFragments, focusWindow, getForegroundWindowTitle


pytestmark = pytest.mark.local_steam


def prepareSheepyWindow(writer: EvidenceWriter, runDir: Path):
    matched, processes = waitUntil(
        supplier=lambda: findProcessesByName(["sheepy", "sheepyashortadventure"]),
        predicate=hasRunningProcess,
        timeoutSeconds=30,
        intervalSeconds=1
    )
    writer.writeJson(runDir, "process-state.json", processes)

    window = findWindowByProcessNameFragments(["sheepyashortadventure"])
    writer.writeJson(
        runDir,
        "window-search.json",
        {
            "processMatched": matched,
            "window": window
        }
    )

    if window is None:
        return matched, None

    focusWindow(window.handle)
    time.sleep(0.5)
    focusedWindow = findWindowByProcessNameFragments(["sheepyashortadventure"])

    if focusedWindow is not None and focusedWindow.isForeground is False:
        clickWindowTitleArea(focusedWindow)
        time.sleep(0.5)
        focusedWindow = findWindowByProcessNameFragments(["sheepyashortadventure"])

    writer.writeJson(runDir, "focused-window.json", focusedWindow)
    return matched, focusedWindow


def writeReviewRequired(writer: EvidenceWriter, runDir: Path, expectedResult: str, processMatched: bool) -> None:
    judgementRecord = createJudgementRecord(
        expectedResult=expectedResult,
        actualResult="REVIEW_REQUIRED",
        actionPerformed=False,
        expectedSignals=[],
        forbiddenSignals=[],
        blockingConditions=[
            JudgementCondition(
                name="Sheepy process detected",
                expected=True,
                actual=processMatched,
                passed=processMatched,
                evidenceKey="process-state.json"
            ),
            JudgementCondition(
                name="Sheepy window detected",
                expected=True,
                actual=False,
                passed=False,
                evidenceKey="window-search.json"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)
    pytest.xfail(judgementRecord.judgementBasis)


def capturePostLanguageState(writer: EvidenceWriter, runDir: Path, fileName: str):
    processMatched, window = prepareSheepyWindow(writer, runDir)

    if window is None:
        writeReviewRequired(writer, runDir, "POST_LANGUAGE_SCREEN", processMatched)

    screenshotPath = captureWindowScreenshot(window, runDir / fileName)
    screenAnalysis = analyzeImage(screenshotPath)
    languageAnalysis = analyzeLanguageSelectionScreen(screenshotPath)
    postLanguageResult = classifyPostLanguageScreen(screenAnalysis, languageAnalysis)
    writer.writeJson(runDir, "screen-analysis.json", screenAnalysis)
    writer.writeJson(runDir, "language-screen-analysis.json", languageAnalysis)
    writer.writeJson(runDir, "post-language-screen.json", postLanguageResult)

    return processMatched, window, screenshotPath, screenAnalysis, languageAnalysis, postLanguageResult


def runInputResponseCheck(
    testId: str,
    expectedResult: str,
    beforeFileName: str,
    idleFileName: str,
    afterFileName: str,
    inputName: str,
    action: Callable[[], None]
) -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir(testId)
    processMatched, window, beforeImagePath, screenAnalysis, languageAnalysis, postLanguageResult = capturePostLanguageState(
        writer=writer,
        runDir=runDir,
        fileName=beforeFileName
    )

    if postLanguageResult.isPostLanguageScreen is False:
        judgementRecord = createJudgementRecord(
            expectedResult=expectedResult,
            actualResult=postLanguageResult.screenState,
            actionPerformed=False,
            expectedSignals=[],
            forbiddenSignals=[],
            blockingConditions=[
                JudgementCondition(
                    name="언어 선택 이후 화면 상태",
                    expected="POST_LANGUAGE_SCREEN",
                    actual=postLanguageResult.screenState,
                    passed=False,
                    evidenceKey="post-language-screen.json.screenState"
                )
            ]
        )
        writer.writeJson(runDir, "judgement.json", judgementRecord)
        pytest.xfail(judgementRecord.judgementBasis)

    time.sleep(1)
    idleImagePath = captureWindowScreenshot(window, runDir / idleFileName)
    idleDiff = compareImages(beforeImagePath, idleImagePath)
    beforeWindowTitle = getForegroundWindowTitle()
    action()
    time.sleep(1)
    afterImagePath = captureWindowScreenshot(window, runDir / afterFileName)
    afterWindowTitle = getForegroundWindowTitle()
    inputDiff = compareImages(idleImagePath, afterImagePath)
    inputChangeDelta = round(inputDiff.changedPixelRatio - idleDiff.changedPixelRatio, 4)
    actionPerformed = window.isForeground and window.processName.lower() == "sheepyashortadventure.exe"

    writer.writeJson(
        runDir,
        "foreground-window.json",
        {
            "beforeWindowTitle": beforeWindowTitle,
            "afterWindowTitle": afterWindowTitle,
            "sheepyWindowTitle": window.title,
            "sheepyProcessName": window.processName,
            "isSheepyForeground": window.isForeground
        }
    )
    writer.writeJson(
        runDir,
        "input-log.json",
        {
            "input": inputName,
            "playerState": "PLAYER-UNKNOWN",
            "expectedResult": expectedResult,
            "idleChangedPixelRatio": idleDiff.changedPixelRatio,
            "inputChangedPixelRatio": inputDiff.changedPixelRatio,
            "inputChangeDelta": inputChangeDelta
        }
    )
    writer.writeJson(runDir, "idle-diff.json", idleDiff)
    writer.writeJson(runDir, "input-diff.json", inputDiff)

    judgementRecord = createJudgementRecord(
        expectedResult=expectedResult,
        actualResult="INPUT_RESPONSE" if inputChangeDelta >= 0.005 else "INPUT_RESPONSE_NOT_CLEAR",
        actionPerformed=actionPerformed,
        expectedSignals=[
            JudgementCondition(
                name="언어 선택 이후 화면 상태",
                expected="POST_LANGUAGE_SCREEN",
                actual=postLanguageResult.screenState,
                passed=postLanguageResult.isPostLanguageScreen,
                evidenceKey="post-language-screen.json.screenState"
            ),
            JudgementCondition(
                name="입력 후 변화량이 무입력 변화량보다 큼",
                expected="inputChangeDelta >= 0.005",
                actual=inputChangeDelta,
                passed=inputChangeDelta >= 0.005,
                evidenceKey="input-log.json.inputChangeDelta"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="입력 후 완전 동일 화면",
                expected=False,
                actual=inputDiff.changedPixelRatio == 0,
                passed=inputDiff.changedPixelRatio > 0,
                evidenceKey="input-diff.json.changedPixelRatio"
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
                name="입력 대상 foreground window",
                expected="SheepyAShortAdventure.exe",
                actual=window.processName,
                passed=actionPerformed,
                evidenceKey="foreground-window.json"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    if judgementRecord.result == "REVIEW_REQUIRED":
        pytest.xfail(judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"


@pytest.mark.tc_018
def test_tc_018_post_language_lobby_screen_is_classified() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-018")
    processMatched, window, screenshotPath, screenAnalysis, languageAnalysis, postLanguageResult = capturePostLanguageState(
        writer=writer,
        runDir=runDir,
        fileName="post-language-screen.png"
    )
    isPostLanguagePreconditionMet = postLanguageResult.isPostLanguageScreen
    judgementRecord = createJudgementRecord(
        expectedResult="POST_LANGUAGE_SCREEN",
        actualResult=postLanguageResult.screenState,
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition(
                name="언어 선택 이후 화면 상태",
                expected="POST_LANGUAGE_SCREEN",
                actual=postLanguageResult.screenState,
                passed=postLanguageResult.isPostLanguageScreen,
                evidenceKey="post-language-screen.json.screenState"
            ),
            JudgementCondition(
                name="시각 정보 색상 수",
                expected="10보다 큼",
                actual=screenAnalysis.uniqueSampledColorCount,
                passed=screenAnalysis.uniqueSampledColorCount > 10,
                evidenceKey="screen-analysis.json.uniqueSampledColorCount"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="언어 선택 화면 잔류",
                expected=False,
                actual=languageAnalysis.isLanguageSelectionLike,
                passed=languageAnalysis.isLanguageSelectionLike is False,
                evidenceKey="language-screen-analysis.json.isLanguageSelectionLike"
            ),
            JudgementCondition(
                name="검은 화면 지속",
                expected=False,
                actual=screenAnalysis.isMostlyBlack,
                passed=screenAnalysis.isMostlyBlack is False,
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
                name="Sheepy window screenshot saved",
                expected=True,
                actual=screenshotPath.exists(),
                passed=screenshotPath.exists(),
                evidenceKey="post-language-screen.png"
            ),
            JudgementCondition(
                name="언어 선택 이후 화면 사전조건",
                expected="POST_LANGUAGE_SCREEN",
                actual=postLanguageResult.screenState,
                passed=isPostLanguagePreconditionMet,
                evidenceKey="post-language-screen.json.screenState"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    if judgementRecord.result == "REVIEW_REQUIRED":
        pytest.xfail(judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"


@pytest.mark.tc_006
def test_tc_006_basic_action_input_response_is_detected() -> None:
    runInputResponseCheck(
        testId="TC-006",
        expectedResult="BASIC_ACTION_INPUT_RESPONSE",
        beforeFileName="before-action-input.png",
        idleFileName="idle-action-input.png",
        afterFileName="after-action-input.png",
        inputName="SPACE",
        action=pressSpace
    )


@pytest.mark.tc_011
def test_tc_011_movement_input_response_is_detected() -> None:
    runInputResponseCheck(
        testId="TC-011",
        expectedResult="MOVEMENT_INPUT_RESPONSE",
        beforeFileName="before-movement-input.png",
        idleFileName="idle-movement-input.png",
        afterFileName="after-movement-input.png",
        inputName="RIGHT_AND_LEFT",
        action=lambda: [pressRight(), pressLeft()]
    )
