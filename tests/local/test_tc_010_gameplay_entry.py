import pytest
from sheepy_qa.local_checks import prepareCheck
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord

pytestmark = pytest.mark.local_steam

@pytest.mark.tc_010
def test_tc_010_lobby_cta_enters_gameplay_screen_candidate():
    writer, runDir, session, lobby = prepareCheck("TC-010", "LOBBY")
    writer.writeJson(runDir, "lobby-preparation.json", lobby)
    result = session.prepare("GAMEPLAY")
    performed = any(event.get("action") == "ENTER" and event.get("from") == "LOBBY" for event in result.events)
    record = createJudgementRecord("GAMEPLAY_SCREEN_CANDIDATE", result.actual, performed,
        [JudgementCondition("플레이 화면 후보 전환", True, result.ready, result.ready, "preparation.json")], [],
        [JudgementCondition("대상 창 관찰", True, result.actual != "UNKNOWN", result.actual != "UNKNOWN", "preparation.json")])
    writer.writeJson(runDir, "judgement.json", record)
    if record.result == "REVIEW_REQUIRED":
        pytest.skip("REVIEW_REQUIRED: " + record.judgementBasis)
    assert record.result == "PASS", record.judgementBasis
