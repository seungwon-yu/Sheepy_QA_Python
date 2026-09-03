import pytest

from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.local_test_config import shouldRunSteamTests
from sheepy_qa.process_check import findProcessesByName, hasRunningProcess
from sheepy_qa.screen_capture import captureScreenshot
from sheepy_qa.steam_app import SteamApp
from sheepy_qa.steam_environment import createSteamEnvironmentSnapshot, isSteamAvailable
from sheepy_qa.wait import waitUntil


pytestmark = pytest.mark.local_steam


@pytest.mark.tc_001
def test_tc_001_steam_environment_is_available() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-001")
    snapshot = createSteamEnvironmentSnapshot()
    writer.writeJson(runDir, "process-state.json", snapshot)
    steamAvailable = isSteamAvailable(snapshot)
    judgementRecord = createJudgementRecord(
        expectedResult="STEAM_AVAILABLE",
        actualResult="STEAM_AVAILABLE" if steamAvailable else "STEAM_UNAVAILABLE",
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition(
                name="Steam 실행 가능 상태",
                expected=True,
                actual=steamAvailable,
                passed=steamAvailable,
                evidenceKey="process-state.json"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="Steam 경로와 프로세스 모두 미확인",
                expected=False,
                actual=steamAvailable is False,
                passed=steamAvailable is True,
                evidenceKey="process-state.json"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    assert judgementRecord.result == "PASS"


@pytest.mark.tc_002
def test_tc_002_sheepy_appid_launch_command_is_called() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-002")
    launchCommand = SteamApp().launch(dryRun=False)
    writer.writeJson(runDir, "execution-log.json", launchCommand)
    hasExpectedUri = "steam://run/1568400" in launchCommand.command
    commandWasExecuted = launchCommand.dryRun is False
    judgementRecord = createJudgementRecord(
        expectedResult="SHEEPY_APPID_LAUNCH_COMMAND_CALLED",
        actualResult="SHEEPY_APPID_LAUNCH_COMMAND_CALLED" if commandWasExecuted and hasExpectedUri else "LAUNCH_COMMAND_INVALID",
        actionPerformed=commandWasExecuted,
        expectedSignals=[
            JudgementCondition(
                name="Sheepy AppID 실행 URI 포함",
                expected="steam://run/1568400",
                actual=launchCommand.command,
                passed=hasExpectedUri,
                evidenceKey="execution-log.json.command"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="dryRun 실행",
                expected=False,
                actual=launchCommand.dryRun,
                passed=launchCommand.dryRun is False,
                evidenceKey="execution-log.json.dryRun"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    assert judgementRecord.result == "PASS"


@pytest.mark.tc_003
def test_tc_003_sheepy_process_is_detected_after_launch() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-003")
    matched, processes = waitUntil(
        supplier=lambda: findProcessesByName(["sheepy", "sheepyashortadventure"]),
        predicate=hasRunningProcess,
        timeoutSeconds=60,
        intervalSeconds=1
    )
    writer.writeJson(runDir, "process-state.json", processes)
    judgementRecord = createJudgementRecord(
        expectedResult="SHEEPY_PROCESS_DETECTED",
        actualResult="SHEEPY_PROCESS_DETECTED" if matched else "SHEEPY_PROCESS_NOT_DETECTED",
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition(
                name="Sheepy 관련 프로세스 감지",
                expected=True,
                actual=matched,
                passed=matched,
                evidenceKey="process-state.json"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="지정 시간 내 프로세스 미감지",
                expected=False,
                actual=matched is False,
                passed=matched is True,
                evidenceKey="process-state.json"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    assert judgementRecord.result == "PASS"


@pytest.mark.tc_004
def test_tc_004_initial_screen_screenshot_is_saved() -> None:
    if not shouldRunSteamTests():
        pytest.skip("Set SHEEPY_RUN_STEAM_TESTS=1 to run local Steam QA tests.")

    writer = EvidenceWriter()
    runDir = writer.createRunDir("TC-004")
    screenshotPath = captureScreenshot(runDir / "screenshot.png")
    screenshotExists = screenshotPath.exists()
    fileSize = screenshotPath.stat().st_size if screenshotExists else 0
    writer.writeJson(
        runDir,
        "screen-metadata.json",
        {
            "screenshotPath": screenshotPath,
            "fileSize": fileSize
        }
    )
    judgementRecord = createJudgementRecord(
        expectedResult="SCREENSHOT_SAVED",
        actualResult="SCREENSHOT_SAVED" if screenshotExists and fileSize > 0 else "SCREENSHOT_NOT_SAVED",
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition(
                name="스크린샷 파일 생성",
                expected=True,
                actual=screenshotExists,
                passed=screenshotExists,
                evidenceKey="screen-metadata.json.screenshotPath"
            ),
            JudgementCondition(
                name="스크린샷 파일 크기",
                expected="0보다 큼",
                actual=fileSize,
                passed=fileSize > 0,
                evidenceKey="screen-metadata.json.fileSize"
            )
        ],
        forbiddenSignals=[
            JudgementCondition(
                name="빈 스크린샷 파일",
                expected=False,
                actual=fileSize == 0,
                passed=fileSize > 0,
                evidenceKey="screen-metadata.json.fileSize"
            )
        ]
    )
    writer.writeJson(runDir, "judgement.json", judgementRecord)

    assert judgementRecord.result == "PASS"
