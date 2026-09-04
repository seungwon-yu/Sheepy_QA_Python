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
    pytest.xfail(judgementRecord.judgementBasis)


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
        pytest.xfail(judgementRecord.judgementBasis)

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
        pytest.xfail(judgementRecord.judgementBasis)

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
        expectedResult="SAVE_DATA_PRESERVED",
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
        pytest.xfail(judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"


@pytest.mark.tc_016
def test_tc_016_basic_movement_and_jump_gameplay_flow_is_detected() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-016")
    processMatched, window = prepareSheepyWindow(writer, runDir)

    if window is None:
        writeWindowReviewRequired(writer, runDir, "BASIC_GAMEPLAY_FLOW_DETECTED", processMatched)

    beforeImagePath = captureWindowScreenshot(window, runDir / "before-gameplay-flow.png")
    beforeScreenAnalysis = analyzeImage(beforeImagePath)
    beforeLanguageAnalysis = analyzeLanguageSelectionScreen(beforeImagePath)
    beforeLobbyMenuAnalysis = analyzeLobbyMenu(beforeImagePath)
    baselineDiff = compareImages(beforeImagePath, beforeImagePath)
    beforeGameplayResult = classifyGameplayScreen(
        screenAnalysis=beforeScreenAnalysis,
        languageAnalysis=beforeLanguageAnalysis,
        lobbyMenuAnalysis=beforeLobbyMenuAnalysis,
        transitionDiff=baselineDiff
    )

    time.sleep(1)
    idleImagePath = captureWindowScreenshot(window, runDir / "idle-gameplay-flow.png")
    idleDiff = compareImages(beforeImagePath, idleImagePath)
    pressRight()
    pressLeft()
    pressSpace()
    time.sleep(1)
    afterImagePath = captureWindowScreenshot(window, runDir / "after-gameplay-flow.png")
    inputDiff = compareImages(idleImagePath, afterImagePath)
    gameplayFlowResult = summarizeGameplayFlow(
        gameplayScreenResult=beforeGameplayResult,
        idleDiff=idleDiff,
        inputDiff=inputDiff
    )
    actionPerformed = window.isForeground and window.processName.lower() == "sheepyashortadventure.exe"

    writer.writeJson(runDir, "before-screen-analysis.json", beforeScreenAnalysis)
    writer.writeJson(runDir, "before-language-screen-analysis.json", beforeLanguageAnalysis)
    writer.writeJson(runDir, "before-lobby-menu-analysis.json", beforeLobbyMenuAnalysis)
    writer.writeJson(runDir, "before-gameplay-screen.json", beforeGameplayResult)
    writer.writeJson(runDir, "idle-diff.json", idleDiff)
    writer.writeJson(runDir, "input-diff.json", inputDiff)
    writer.writeJson(
        runDir,
        "input-log.json",
        {
            "input": "RIGHT_LEFT_SPACE",
            "idleChangedPixelRatio": idleDiff.changedPixelRatio,
            "inputChangedPixelRatio": inputDiff.changedPixelRatio,
            "inputChangeDelta": gameplayFlowResult.inputChangeDelta,
            "isSheepyForeground": actionPerformed
        }
    )
    writer.writeJson(runDir, "gameplay-flow.json", gameplayFlowResult)

    judgementRecord = createJudgementRecord(
        expectedResult="BASIC_GAMEPLAY_FLOW_DETECTED",
        actualResult=gameplayFlowResult.resultState,
        actionPerformed=actionPerformed and beforeGameplayResult.isGameplayScreenCandidate,
        expectedSignals=[
            JudgementCondition(
                name="플레이 화면 후보",
                expected="GAMEPLAY_SCREEN_CANDIDATE",
                actual=beforeGameplayResult.screenState,
                passed=beforeGameplayResult.isGameplayScreenCandidate,
                evidenceKey="before-gameplay-screen.json.screenState"
            ),
            JudgementCondition(
                name="입력 후 변화량",
                expected="inputChangeDelta >= 0.005",
                actual=gameplayFlowResult.inputChangeDelta,
                passed=gameplayFlowResult.inputChangeDelta >= 0.005,
                evidenceKey="gameplay-flow.json.inputChangeDelta"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="언어 선택 화면 잔류",
                expected=False,
                actual=beforeLanguageAnalysis.isLanguageSelectionLike,
                passed=beforeLanguageAnalysis.isLanguageSelectionLike is False,
                evidenceKey="before-language-screen-analysis.json.isLanguageSelectionLike"
            ),
            JudgementCondition(
                name="로비 CTA 잔류",
                expected=False,
                actual=beforeLobbyMenuAnalysis.continueVisible or beforeLobbyMenuAnalysis.startJourneyVisible,
                passed=beforeLobbyMenuAnalysis.continueVisible is False and beforeLobbyMenuAnalysis.startJourneyVisible is False,
                evidenceKey="before-lobby-menu-analysis.json"
            ),
            JudgementCondition(
                name="검은 화면 지속",
                expected=False,
                actual=beforeScreenAnalysis.isMostlyBlack,
                passed=beforeScreenAnalysis.isMostlyBlack is False,
                evidenceKey="before-screen-analysis.json.isMostlyBlack"
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
                evidenceKey="focused-window.json"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    if judgementRecord.result == "REVIEW_REQUIRED":
        pytest.xfail(judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"
