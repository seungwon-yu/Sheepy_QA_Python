import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.local_test_config import shouldRunSteamTests
from sheepy_qa.process_check import findProcessesByName, hasRunningProcess
from sheepy_qa.screen_capture import captureScreenshot
from sheepy_qa.steam_app import SteamApp
from sheepy_qa.steam_environment import createSteamEnvironmentSnapshot, isSteamAvailable
from sheepy_qa.wait import waitUntil


pytestmark = pytest.mark.local_steam


def test_tc_001_steam_environment_is_available() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-001")
    snapshot = createSteamEnvironmentSnapshot()
    writer.writeJson(runDir, "process-state.json", snapshot)

    assert isSteamAvailable(snapshot) is True


def test_tc_002_sheepy_appid_launch_command_is_called() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-002")
    launchCommand = SteamApp().launch(dryRun=False)
    writer.writeJson(runDir, "execution-log.json", launchCommand)

    assert launchCommand.dryRun is False
    assert "steam://run/1568400" in launchCommand.command


def test_tc_003_sheepy_process_is_detected_after_launch() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-003")
    matched, processes = waitUntil(
        supplier=lambda: findProcessesByName(["sheepy"]),
        predicate=hasRunningProcess,
        timeoutSeconds=30,
        intervalSeconds=1
    )
    writer.writeJson(runDir, "process-state.json", processes)

    assert matched is True


def test_tc_004_initial_screen_screenshot_is_saved() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-004")
    screenshotPath = captureScreenshot(runDir / "screenshot.png")
    writer.writeJson(
        runDir,
        "screen-metadata.json",
        {
            "screenshotPath": screenshotPath,
            "fileSize": screenshotPath.stat().st_size
        }
    )

    assert screenshotPath.exists()
    assert screenshotPath.stat().st_size > 0
