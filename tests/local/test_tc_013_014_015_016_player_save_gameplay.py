import time
from pathlib import Path

import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.gameplay_flow import summarizeGameplayFlow
from sheepy_qa.gameplay_screen import classifyGameplayScreen
from sheepy_qa.image_analysis import analyzeImage
from sheepy_qa.image_diff import compareImages
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.keyboard_input import pressLeft, pressRight, pressSpace
from sheepy_qa.language_screen import analyzeLanguageSelectionScreen
from sheepy_qa.lobby_menu import analyzeLobbyMenu
from sheepy_qa.local_test_config import shouldRunSteamTests
from sheepy_qa.player_state import classifyPlayerStateFromLobby
from sheepy_qa.post_language_screen import classifyPostLanguageScreen
from sheepy_qa.process_check import findProcessesByName, hasRunningProcess
from sheepy_qa.save_data import compareSaveSnapshots, createSaveDataSnapshot
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


def writeWindowReviewRequired(writer: EvidenceWriter, runDir: Path, expectedResult: str, processMatched: bool) -> None:
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
    pytest.skip("REVIEW_REQUIRED: " + judgementRecord.judgementBasis)


def captureLobbyEvidence(writer: EvidenceWriter, runDir: Path, fileName: str):
    processMatched, window = prepareSheepyWindow(writer, runDir)

    if window is None:
        writeWindowReviewRequired(writer, runDir, "LOBBY_MENU", processMatched)

    screenshotPath = captureWindowScreenshot(window, runDir / fileName)
    screenAnalysis = analyzeImage(screenshotPath)
    languageAnalysis = analyzeLanguageSelectionScreen(screenshotPath)
    postLanguageResult = classifyPostLanguageScreen(screenAnalysis, languageAnalysis)
    lobbyMenuAnalysis = analyzeLobbyMenu(screenshotPath)
    playerStateResult = classifyPlayerStateFromLobby(lobbyMenuAnalysis)

    writer.writeJson(runDir, "screen-analysis.json", screenAnalysis)
    writer.writeJson(runDir, "language-screen-analysis.json", languageAnalysis)
    writer.writeJson(runDir, "post-language-screen.json", postLanguageResult)
    writer.writeJson(runDir, "lobby-menu-analysis.json", lobbyMenuAnalysis)
    writer.writeJson(runDir, "player-state.json", playerStateResult)

    return processMatched, window, screenshotPath, screenAnalysis, languageAnalysis, postLanguageResult, lobbyMenuAnalysis, playerStateResult


@pytest.mark.tc_013
def test_tc_013_first_run_player_state_is_identified() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-013")
    processMatched, window, screenshotPath, screenAnalysis, languageAnalysis, postLanguageResult, lobbyMenuAnalysis, playerStateResult = captureLobbyEvidence(
        writer=writer,
        runDir=runDir,
        fileName="first-run-state.png"
    )
    judgementRecord = createJudgementRecord(
        expectedResult="PLAYER_NEW",
        actualResult=playerStateResult.playerState,
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition(
                name="Start Your Journey 단독 표시",
                expected=True,
                actual=lobbyMenuAnalysis.startJourneyVisible and not lobbyMenuAnalysis.continueVisible,
                passed=playerStateResult.isFirstRunCandidate,
                evidenceKey="player-state.json.isFirstRunCandidate"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="Continue 표시",
                expected=False,
                actual=lobbyMenuAnalysis.continueVisible,
                passed=lobbyMenuAnalysis.continueVisible is False,
                evidenceKey="lobby-menu-analysis.json.continueVisible"
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
                evidenceKey="first-run-state.png"
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
        pytest.skip("REVIEW_REQUIRED: " + judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"


@pytest.mark.tc_014
def test_tc_014_returning_player_state_is_identified() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-014")
    processMatched, window, screenshotPath, screenAnalysis, languageAnalysis, postLanguageResult, lobbyMenuAnalysis, playerStateResult = captureLobbyEvidence(
        writer=writer,
        runDir=runDir,
        fileName="returning-state.png"
    )
    judgementRecord = createJudgementRecord(
        expectedResult="PLAYER_RETURNING",
        actualResult=playerStateResult.playerState,
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition(
                name="Continue 표시",
                expected=True,
                actual=lobbyMenuAnalysis.continueVisible,
                passed=playerStateResult.isReturningCandidate,
                evidenceKey="player-state.json.isReturningCandidate"
            )
        ],
        forbiddenSignals=[
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
                evidenceKey="returning-state.png"
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
        pytest.skip("REVIEW_REQUIRED: " + judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"


@pytest.mark.tc_015
def test_tc_015_save_data_paths_are_preserved_during_observation() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-015")
    beforeSnapshot = createSaveDataSnapshot()
    time.sleep(2)
    afterSnapshot = createSaveDataSnapshot()
    preservationResult = compareSaveSnapshots(beforeSnapshot, afterSnapshot)

    writer.writeJson(runDir, "save-before.json", beforeSnapshot)
    writer.writeJson(runDir, "save-after.json", afterSnapshot)
    writer.writeJson(runDir, "save-preservation.json", preservationResult)

    judgementRecord = createJudgementRecord(
        expectedResult="SAVE_FILES_PRESENT",
        actualResult=preservationResult.resultState,
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition(
                name="관찰 가능한 저장 파일",
                expected="1개 이상",
                actual=preservationResult.beforeFileCount,
                passed=preservationResult.beforeFileCount > 0,
                evidenceKey="save-before.json.files"
            ),
            JudgementCondition(
                name="기존 저장 파일 경로 유지",
                expected=[],
                actual=preservationResult.missingFiles,
                passed=len(preservationResult.missingFiles) == 0,
                evidenceKey="save-preservation.json.missingFiles"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="저장 파일 누락",
                expected=False,
                actual=len(preservationResult.missingFiles) > 0,
                passed=len(preservationResult.missingFiles) == 0,
                evidenceKey="save-preservation.json.missingFiles"
            )
        ],
        blockingConditions=[
            JudgementCondition(
                name="저장 파일 후보 발견",
                expected=True,
                actual=preservationResult.beforeFileCount > 0,
                passed=preservationResult.beforeFileCount > 0,
                evidenceKey="save-before.json.files"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    if judgementRecord.result == "REVIEW_REQUIRED":
        pytest.skip("REVIEW_REQUIRED: " + judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"


@pytest.mark.tc_016
def test_tc_016_basic_movement_and_jump_gameplay_flow_is_detected():
    from sheepy_qa.local_checks import runVisualInputCheck
    runVisualInputCheck("TC-016", lambda session: [session.input(pressRight), session.input(pressLeft), session.input(pressSpace)])
