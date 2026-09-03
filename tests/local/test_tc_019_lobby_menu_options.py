import time
from pathlib import Path

import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.image_analysis import analyzeImage
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.language_screen import analyzeLanguageSelectionScreen
from sheepy_qa.lobby_menu import analyzeLobbyMenu
from sheepy_qa.local_test_config import shouldRunSteamTests
from sheepy_qa.post_language_screen import classifyPostLanguageScreen
from sheepy_qa.process_check import findProcessesByName, hasRunningProcess
from sheepy_qa.screen_capture import captureWindowScreenshot
from sheepy_qa.wait import waitUntil
from sheepy_qa.window_state import clickWindowTitleArea, findWindowByProcessNameFragments, focusWindow


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


@pytest.mark.tc_019
def test_tc_019_lobby_continue_and_start_journey_options_are_detected() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-019")
    processMatched, window = prepareSheepyWindow(writer, runDir)

    if window is None:
        judgementRecord = createJudgementRecord(
            expectedResult="LOBBY_MENU_WITH_CONTINUE_AND_START",
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

    screenshotPath = captureWindowScreenshot(window, runDir / "lobby-menu.png")
    screenAnalysis = analyzeImage(screenshotPath)
    languageAnalysis = analyzeLanguageSelectionScreen(screenshotPath)
    postLanguageResult = classifyPostLanguageScreen(screenAnalysis, languageAnalysis)
    lobbyMenuAnalysis = analyzeLobbyMenu(screenshotPath)

    writer.writeJson(runDir, "screen-analysis.json", screenAnalysis)
    writer.writeJson(runDir, "language-screen-analysis.json", languageAnalysis)
    writer.writeJson(runDir, "post-language-screen.json", postLanguageResult)
    writer.writeJson(runDir, "lobby-menu-analysis.json", lobbyMenuAnalysis)

    judgementRecord = createJudgementRecord(
        expectedResult="LOBBY_MENU_WITH_CONTINUE_AND_START",
        actualResult=lobbyMenuAnalysis.screenState,
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
                name="Continue CTA 표시",
                expected=True,
                actual=lobbyMenuAnalysis.continueVisible,
                passed=lobbyMenuAnalysis.continueVisible,
                evidenceKey="lobby-menu-analysis.json.continueVisible"
            ),
            JudgementCondition(
                name="Start Your Journey CTA 표시",
                expected=True,
                actual=lobbyMenuAnalysis.startJourneyVisible,
                passed=lobbyMenuAnalysis.startJourneyVisible,
                evidenceKey="lobby-menu-analysis.json.startJourneyVisible"
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
                name="언어 선택 이후 화면 사전조건",
                expected="POST_LANGUAGE_SCREEN",
                actual=postLanguageResult.screenState,
                passed=postLanguageResult.isPostLanguageScreen,
                evidenceKey="post-language-screen.json.screenState"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    if judgementRecord.result == "REVIEW_REQUIRED":
        pytest.xfail(judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"
