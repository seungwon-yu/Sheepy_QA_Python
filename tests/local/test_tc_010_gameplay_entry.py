import time
from pathlib import Path

import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.gameplay_screen import classifyGameplayScreen
from sheepy_qa.image_analysis import analyzeImage
from sheepy_qa.image_diff import compareImages
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.keyboard_input import pressEnter
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


@pytest.mark.tc_010
def test_tc_010_lobby_cta_enters_gameplay_screen_candidate() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-010")
    processMatched, window = prepareSheepyWindow(writer, runDir)

    if window is None:
        judgementRecord = createJudgementRecord(
            expectedResult="GAMEPLAY_SCREEN_CANDIDATE",
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

    beforeImagePath = captureWindowScreenshot(window, runDir / "before-gameplay-entry.png")
    beforeScreenAnalysis = analyzeImage(beforeImagePath)
    beforeLanguageAnalysis = analyzeLanguageSelectionScreen(beforeImagePath)
    beforePostLanguageResult = classifyPostLanguageScreen(beforeScreenAnalysis, beforeLanguageAnalysis)
    beforeLobbyMenuAnalysis = analyzeLobbyMenu(beforeImagePath)

    writer.writeJson(runDir, "before-screen-analysis.json", beforeScreenAnalysis)
    writer.writeJson(runDir, "before-language-screen-analysis.json", beforeLanguageAnalysis)
    writer.writeJson(runDir, "before-post-language-screen.json", beforePostLanguageResult)
    writer.writeJson(runDir, "before-lobby-menu-analysis.json", beforeLobbyMenuAnalysis)

    isLobbyEntryReady = beforePostLanguageResult.isPostLanguageScreen and (
        beforeLobbyMenuAnalysis.continueVisible or beforeLobbyMenuAnalysis.startJourneyVisible
    )

    if isLobbyEntryReady:
        pressEnter()

    time.sleep(3)
    afterWindow = findWindowByProcessNameFragments(["sheepyashortadventure"]) or window
    afterImagePath = captureWindowScreenshot(afterWindow, runDir / "after-gameplay-entry.png")
    afterScreenAnalysis = analyzeImage(afterImagePath)
    afterLanguageAnalysis = analyzeLanguageSelectionScreen(afterImagePath)
    afterLobbyMenuAnalysis = analyzeLobbyMenu(afterImagePath)
    transitionDiff = compareImages(beforeImagePath, afterImagePath)
    gameplayScreenResult = classifyGameplayScreen(
        screenAnalysis=afterScreenAnalysis,
        languageAnalysis=afterLanguageAnalysis,
        lobbyMenuAnalysis=afterLobbyMenuAnalysis,
        transitionDiff=transitionDiff
    )

    writer.writeJson(runDir, "after-screen-analysis.json", afterScreenAnalysis)
    writer.writeJson(runDir, "after-language-screen-analysis.json", afterLanguageAnalysis)
    writer.writeJson(runDir, "after-lobby-menu-analysis.json", afterLobbyMenuAnalysis)
    writer.writeJson(runDir, "transition-diff.json", transitionDiff)
    writer.writeJson(runDir, "gameplay-screen.json", gameplayScreenResult)
    writer.writeJson(
        runDir,
        "entry-input-log.json",
        {
            "input": "ENTER",
            "selectedEntryHint": "Continue" if beforeLobbyMenuAnalysis.continueVisible else "Start Your Journey",
            "playerStateHint": beforeLobbyMenuAnalysis.playerStateHint,
            "isLobbyEntryReady": isLobbyEntryReady
        }
    )

    judgementRecord = createJudgementRecord(
        expectedResult="GAMEPLAY_SCREEN_CANDIDATE",
        actualResult=gameplayScreenResult.screenState,
        actionPerformed=isLobbyEntryReady,
        expectedSignals=[
            JudgementCondition(
                name="로비 진입 CTA 표시",
                expected="Continue 또는 Start Your Journey",
                actual=beforeLobbyMenuAnalysis.screenState,
                passed=isLobbyEntryReady,
                evidenceKey="before-lobby-menu-analysis.json.screenState"
            ),
            JudgementCondition(
                name="입력 후 플레이 화면 후보",
                expected="GAMEPLAY_SCREEN_CANDIDATE",
                actual=gameplayScreenResult.screenState,
                passed=gameplayScreenResult.isGameplayScreenCandidate,
                evidenceKey="gameplay-screen.json.screenState"
            ),
            JudgementCondition(
                name="로비 대비 화면 변화량",
                expected="changedPixelRatio >= 0.05",
                actual=transitionDiff.changedPixelRatio,
                passed=transitionDiff.changedPixelRatio >= 0.05,
                evidenceKey="transition-diff.json.changedPixelRatio"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="언어 선택 화면 잔류",
                expected=False,
                actual=afterLanguageAnalysis.isLanguageSelectionLike,
                passed=afterLanguageAnalysis.isLanguageSelectionLike is False,
                evidenceKey="after-language-screen-analysis.json.isLanguageSelectionLike"
            ),
            JudgementCondition(
                name="로비 CTA 잔류",
                expected=False,
                actual=afterLobbyMenuAnalysis.continueVisible or afterLobbyMenuAnalysis.startJourneyVisible,
                passed=afterLobbyMenuAnalysis.continueVisible is False and afterLobbyMenuAnalysis.startJourneyVisible is False,
                evidenceKey="after-lobby-menu-analysis.json"
            ),
            JudgementCondition(
                name="검은 화면 지속",
                expected=False,
                actual=afterScreenAnalysis.isMostlyBlack,
                passed=afterScreenAnalysis.isMostlyBlack is False,
                evidenceKey="after-screen-analysis.json.isMostlyBlack"
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
                name="언어 선택 이후 로비 사전조건",
                expected="LOBBY_MENU",
                actual=beforeLobbyMenuAnalysis.screenState,
                passed=isLobbyEntryReady,
                evidenceKey="before-lobby-menu-analysis.json.screenState"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    if judgementRecord.result == "REVIEW_REQUIRED":
        pytest.xfail(judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"
