import pytest
from sheepy_qa.local_checks import prepareCheck, runVisualInputCheck
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord
from sheepy_qa.keyboard_input import pressLeft, pressRight, pressSpace

pytestmark = pytest.mark.local_steam

@pytest.mark.tc_018
def test_tc_018_post_language_observation():
    writer, runDir, session, prepared = prepareCheck("TC-018", "POST_LANGUAGE")
    record = createJudgementRecord("POST_LANGUAGE", prepared.actual, True,
        [JudgementCondition("언어 선택 이후 후보", True, prepared.ready, prepared.ready, "preparation.json")], [])
    writer.writeJson(runDir, "judgement.json", record)
    assert record.result == "PASS"

@pytest.mark.tc_006
def test_tc_006_space_visual_response():
    runVisualInputCheck("TC-006", lambda session: session.input(pressSpace))

@pytest.mark.tc_011
def test_tc_011_direction_visual_response():
    runVisualInputCheck("TC-011", lambda session: [session.input(pressRight), session.input(pressLeft)])
