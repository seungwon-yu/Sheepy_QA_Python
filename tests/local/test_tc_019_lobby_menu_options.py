import pytest
from sheepy_qa.local_checks import prepareCheck
from sheepy_qa.lobby_menu import analyzeLobbyMenu
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord

pytestmark = pytest.mark.local_steam

@pytest.mark.tc_019
def test_tc_019_lobby_continue_and_start_journey_options_are_detected():
    writer, runDir, session, prepared = prepareCheck("TC-019", "LOBBY")
    menu = analyzeLobbyMenu(session.lastImage)
    writer.writeJson(runDir, "lobby-menu-analysis.json", menu)
    record = createJudgementRecord("LOBBY_MENU_WITH_CONTINUE_AND_START", menu.screenState, True, [
        JudgementCondition("Continue 후보", True, menu.continueVisible, menu.continueVisible, "lobby-menu-analysis.json"),
        JudgementCondition("Start 후보", True, menu.startJourneyVisible, menu.startJourneyVisible, "lobby-menu-analysis.json")
    ], [])
    writer.writeJson(runDir, "judgement.json", record)
    assert record.result == "PASS", record.judgementBasis
