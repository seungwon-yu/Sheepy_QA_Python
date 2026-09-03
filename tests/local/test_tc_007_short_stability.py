import time
from pathlib import Path

import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.local_test_config import shouldRunSteamTests
from sheepy_qa.process_check import findProcessesByName, hasRunningProcess
from sheepy_qa.screen_capture import captureWindowScreenshot
from sheepy_qa.stability import StabilitySample, summarizeStabilitySamples
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
    writer.writeJson(runDir, "initial-process-state.json", processes)

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


@pytest.mark.tc_007
def test_tc_007_game_remains_stable_for_short_observation() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-007")
    processMatched, window = prepareSheepyWindow(writer, runDir)
    durationSeconds = 30
    intervalSeconds = 5

    if window is None:
        judgementRecord = createJudgementRecord(
            expectedResult="STABLE_SHORT_RUN",
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
                    evidenceKey="initial-process-state.json"
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

    samples: list[StabilitySample] = []
    startedAt = time.monotonic()

    while True:
        elapsedSeconds = round(time.monotonic() - startedAt, 2)
        processes = findProcessesByName(["sheepy", "sheepyashortadventure"])
        processAlive = hasRunningProcess(processes)
        currentWindow = findWindowByProcessNameFragments(["sheepyashortadventure"])
        screenshotFileName = f"stability-{len(samples):02d}.png"
        screenshotSaved = False

        if processAlive and currentWindow is not None:
            screenshotPath = captureWindowScreenshot(currentWindow, runDir / screenshotFileName)
            screenshotSaved = screenshotPath.exists() and screenshotPath.stat().st_size > 0

        samples.append(
            StabilitySample(
                elapsedSeconds=elapsedSeconds,
                processAlive=processAlive,
                screenshotSaved=screenshotSaved,
                screenshotFileName=screenshotFileName if screenshotSaved else None
            )
        )

        if elapsedSeconds >= durationSeconds:
            break

        time.sleep(intervalSeconds)

    finalProcesses = findProcessesByName(["sheepy", "sheepyashortadventure"])
    stabilityResult = summarizeStabilitySamples(samples=samples, durationSeconds=durationSeconds)
    writer.writeJson(runDir, "process-timeline.json", samples)
    writer.writeJson(runDir, "final-process-state.json", finalProcesses)
    writer.writeJson(runDir, "stability-summary.json", stabilityResult)

    judgementRecord = createJudgementRecord(
        expectedResult="STABLE_SHORT_RUN",
        actualResult=stabilityResult.resultState,
        actionPerformed=stabilityResult.sampleCount > 0,
        expectedSignals=[
            JudgementCondition(
                name="관찰 샘플 수",
                expected="1보다 큼",
                actual=stabilityResult.sampleCount,
                passed=stabilityResult.sampleCount > 1,
                evidenceKey="stability-summary.json.sampleCount"
            ),
            JudgementCondition(
                name="관찰 중 프로세스 유지",
                expected=True,
                actual=stabilityResult.processAliveThroughout,
                passed=stabilityResult.processAliveThroughout,
                evidenceKey="stability-summary.json.processAliveThroughout"
            ),
            JudgementCondition(
                name="관찰 중 screenshot 저장",
                expected=True,
                actual=stabilityResult.screenshotSavedThroughout,
                passed=stabilityResult.screenshotSavedThroughout,
                evidenceKey="stability-summary.json.screenshotSavedThroughout"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="비정상 종료 샘플",
                expected=0,
                actual=stabilityResult.failedSampleCount,
                passed=stabilityResult.failedSampleCount == 0,
                evidenceKey="stability-summary.json.failedSampleCount"
            )
        ],
        blockingConditions=[
            JudgementCondition(
                name="Sheepy process detected",
                expected=True,
                actual=processMatched,
                passed=processMatched,
                evidenceKey="initial-process-state.json"
            ),
            JudgementCondition(
                name="Sheepy window detected",
                expected=True,
                actual=window is not None,
                passed=window is not None,
                evidenceKey="window-search.json"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    if judgementRecord.result == "REVIEW_REQUIRED":
        pytest.xfail(judgementRecord.judgementBasis)

    assert judgementRecord.result == "PASS"
