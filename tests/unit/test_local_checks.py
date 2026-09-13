from types import SimpleNamespace
import pytest
from sheepy_qa import local_checks
from sheepy_qa.evidence import EvidenceWriter


def test_blocked_preparation_stops_before_input_and_writes_judgement(monkeypatch, tmp_path):
    monkeypatch.setattr(local_checks, "shouldRunSteamTests", lambda: True)
    monkeypatch.setattr(local_checks, "EvidenceWriter", lambda: EvidenceWriter(tmp_path))
    class BlockedSession:
        def __init__(self, writer, runDir):
            pass
        def prepare(self, target):
            return SimpleNamespace(ready=False, actual="UNKNOWN", reason="지원하지 않는 화면")
    monkeypatch.setattr(local_checks, "LocalScreenSession", BlockedSession)
    with pytest.raises(pytest.skip.Exception, match="REVIEW_REQUIRED"):
        local_checks.runVisualInputCheck("TC-006", lambda session: pytest.fail("입력이 실행되면 안 됨"))
    import json
    record = json.loads(next(tmp_path.rglob("judgement.json")).read_text(encoding="utf-8"))
    assert record["result"] == "REVIEW_REQUIRED"
    assert record["actionPerformed"] is False


def test_local_input_rechecks_foreground(monkeypatch, tmp_path):
    from sheepy_qa import local_screen_session
    session = local_screen_session.LocalScreenSession(EvidenceWriter(tmp_path), tmp_path)
    monkeypatch.setattr(local_screen_session, "findWindowByProcessNameFragments", lambda fragments: None)
    with pytest.raises(RuntimeError, match="foreground"):
        session.input(lambda: pytest.fail("입력하면 안 됨"))


@pytest.mark.parametrize("afterState", ["GAMEPLAY", "LOBBY"])
def test_screen_transition_is_not_mistaken_for_input_success(monkeypatch, tmp_path, afterState):
    import json
    writer = EvidenceWriter(tmp_path)
    runDir = writer.createRunDir("TC-006")
    observations = iter(["GAMEPLAY", afterState])
    session = SimpleNamespace(lastImage="mock-image", observe=lambda: SimpleNamespace(foreground=True, state=next(observations)))
    monkeypatch.setattr(local_checks, "prepareCheck", lambda *args: (writer, runDir, session, SimpleNamespace(ready=True)))
    monkeypatch.setattr(local_checks.time, "sleep", lambda seconds: None)
    diffs = iter([0.01, 0.1])
    from sheepy_qa.image_diff import ImageDiffResult
    monkeypatch.setattr(local_checks, "compareImages", lambda *args: ImageDiffResult(10, 10, 100, next(diffs), 1, True))
    if afterState == "LOBBY":
        with pytest.raises(pytest.skip.Exception, match="REVIEW_REQUIRED"):
            local_checks.runVisualInputCheck("TC-006", lambda session: None)
    else:
        local_checks.runVisualInputCheck("TC-006", lambda session: None)
    record = json.loads((runDir / "judgement.json").read_text(encoding="utf-8"))
    assert record["result"] == ("PASS" if afterState == "GAMEPLAY" else "REVIEW_REQUIRED")
