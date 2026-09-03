import time
from pathlib import Path

import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.freeze_detection import summarizeFreezeObservation
from sheepy_qa.image_diff import compareImages
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.local_test_config import shouldRunSteamTests
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


@pytest.mark.tc_012
def test_tc_012_screen_freeze_is_not_detected_during_observation() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-012")
    processMatched, window = prepareSheepyWindow(writer, runDir)

    if window is None:
        judgementRecord = createJudgementRecord(
            expectedResult="FREEZE_NOT_DETECTED",
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

    screenshotPaths: list[Path] = []
    durationSeconds = 20
    intervalSeconds = 5
    startedAt = time.monotonic()

    while True:
        elapsedSeconds = round(time.monotonic() - startedAt, 2)
        currentWindow = findWindowByProcessNameFragments(["sheepyashortadventure"])
        processes = findProcessesByName(["sheepy", "sheepyashortadventure"])
        processAlive = hasRunningProcess(processes)

        if processAlive and currentWindow is not None:
            screenshotPath = captureWindowScreenshot(
                currentWindow,
                runDir / f"freeze-sample-{len(screenshotPaths):02d}.png"
            )
            screenshotPaths.append(screenshotPath)

        if elapsedSeconds >= durationSeconds:
            break

        time.sleep(intervalSeconds)

    diffs = []

    for index in range(1, len(screenshotPaths)):
        diff = compareImages(screenshotPaths[index - 1], screenshotPaths[index])
        diffs.append(diff)
        writer.writeJson(runDir, f"freeze-diff-{index - 1:02d}-{index:02d}.json", diff)

    finalProcesses = findProcessesByName(["sheepy", "sheepyashortadventure"])
    freezeResult = summarizeFreezeObservation(diffs)
    writer.writeJson(
        runDir,
        "freeze-samples.json",
        {
            "durationSeconds": durationSeconds,
            "intervalSeconds": intervalSeconds,
            "screenshotFiles": [path.name for path in screenshotPaths]
        }
    )
    writer.writeJson(runDir, "final-process-state.json", finalProcesses)
    writer.writeJson(runDir, "freeze-summary.json", freezeResult)

    judgementRecord = createJudgementRecord(
        expectedResult="FREEZE_NOT_DETECTED",
        actualResult=freezeResult.resultState,
        actionPerformed=len(screenshotPaths) > 1,
        expectedSignals=[
            JudgementCondition(
                name="비교 가능한 screenshot 쌍",
                expected="1개 이상",
                actual=freezeResult.comparisonCount,
                passed=freezeResult.comparisonCount > 0,
                evidenceKey="freeze-summary.json.comparisonCount"
            ),
            JudgementCondition(
                name="관찰 중 화면 변화",
                expected="visibleChangeCount >= 1",
                actual=freezeResult.visibleChangeCount,
                passed=freezeResult.visibleChangeCount >= 1,
                evidenceKey="freeze-summary.json.visibleChangeCount"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="프로세스 종료",
                expected=False,
                actual=hasRunningProcess(finalProcesses) is False,
                passed=hasRunningProcess(finalProcesses),
                evidenceKey="final-process-state.json"
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
