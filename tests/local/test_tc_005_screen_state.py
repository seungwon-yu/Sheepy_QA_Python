import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.image_analysis import analyzeImage, classifyScreenState
from sheepy_qa.local_test_config import shouldRunSteamTests
from sheepy_qa.process_check import findProcessesByName, hasRunningProcess
from sheepy_qa.screen_capture import captureScreenshot
from sheepy_qa.steam_app import SteamApp
from sheepy_qa.wait import waitUntil


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
        supplier=lambda: findProcessesByName(["sheepy"]),
        predicate=hasRunningProcess,
        timeoutSeconds=30,
        intervalSeconds=1
    )
    writer.writeJson(runDir, "process-state.json", processes)

    screenshotPath = captureScreenshot(runDir / "screenshot.png")
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

    assert matched is True
    assert screenState == "VISIBLE_SCREEN"
