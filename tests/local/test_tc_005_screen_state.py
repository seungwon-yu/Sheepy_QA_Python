import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.image_analysis import analyzeImage, classifyScreenState
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.local_test_config import shouldRunSteamTests
from sheepy_qa.process_check import findProcessesByName, hasRunningProcess
from sheepy_qa.screen_capture import captureScreenshot, captureWindowScreenshot
from sheepy_qa.steam_app import SteamApp
from sheepy_qa.wait import waitUntil
from sheepy_qa.window_state import findWindowByProcessNameFragments


pytestmark = pytest.mark.local_steam


@pytest.mark.tc_005
def test_tc_005_initial_screen_is_not_black_screen() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-005")

    launchCommand = SteamApp().launch(dryRun=False)
    writer.writeJson(runDir, "execution-log.json", launchCommand)

    matched, processes = waitUntil(
        supplier=lambda: findProcessesByName(["sheepy", "sheepyashortadventure"]),
        predicate=hasRunningProcess,
        timeoutSeconds=60,
        intervalSeconds=1
    )
    writer.writeJson(runDir, "process-state.json", processes)

    window = findWindowByProcessNameFragments(["sheepyashortadventure"])

    if window is None:
        captureTarget = "FULL_SCREEN_FALLBACK"
        screenshotPath = captureScreenshot(runDir / "screenshot.png")
    else:
        captureTarget = "SHEEPY_WINDOW"
        screenshotPath = captureWindowScreenshot(window, runDir / "screenshot.png")

    writer.writeJson(
        runDir,
        "capture-target.json",
        {
            "captureTarget": captureTarget,
            "window": window
        }
    )
    analysisResult = analyzeImage(screenshotPath)
    screenState = classifyScreenState(analysisResult)
    writer.writeJson(runDir, "image-analysis.json", analysisResult)

    writer.writeJson(
        runDir,
        "screen-state.json",
        {
            "screenState": screenState,
            "expectedResult": "VISIBLE_SCREEN",
            "actualResult": screenState,
            "judgementBasis": [
                "averageBrightness가 검은 화면 기준값보다 높아야 한다.",
                "darkPixelRatio가 대부분의 화면이 검은 픽셀임을 나타내지 않아야 한다.",
                "uniqueSampledColorCount가 화면에 시각 정보가 있음을 보여야 한다."
            ],
            "analysis": analysisResult
        }
    )
    judgementRecord = createJudgementRecord(
        expectedResult="VISIBLE_SCREEN",
        actualResult=screenState,
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition(
                name="Sheepy 관련 프로세스 감지",
                expected=True,
                actual=matched,
                passed=matched,
                evidenceKey="process-state.json"
            ),
            JudgementCondition(
                name="화면 상태 판별 결과",
                expected="VISIBLE_SCREEN",
                actual=screenState,
                passed=screenState == "VISIBLE_SCREEN",
                evidenceKey="screen-state.json.screenState"
            ),
            JudgementCondition(
                name="시각 정보 색상 수",
                expected="1보다 큼",
                actual=analysisResult.uniqueSampledColorCount,
                passed=analysisResult.uniqueSampledColorCount > 1,
                evidenceKey="image-analysis.json.uniqueSampledColorCount"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="검은 화면 지속",
                expected=False,
                actual=analysisResult.isMostlyBlack,
                passed=analysisResult.isMostlyBlack is False,
                evidenceKey="image-analysis.json.isMostlyBlack"
            )
        ],
        blockingConditions=[
            JudgementCondition(
                name="screenshot capture target",
                expected="SHEEPY_WINDOW 또는 FULL_SCREEN_FALLBACK",
                actual=captureTarget,
                passed=captureTarget in ("SHEEPY_WINDOW", "FULL_SCREEN_FALLBACK"),
                evidenceKey="capture-target.json"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    assert judgementRecord.result == "PASS"
