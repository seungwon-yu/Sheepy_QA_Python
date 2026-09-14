"""보관 이미지와 실제 판정 함수를 연결한다. 실제 게임 실행 검증은 아니다."""
from pathlib import Path
from types import SimpleNamespace

from PIL import Image
import pytest
import json
from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.screen_preparation import ScreenObservation

import sheepy_qa.local_screen_session as sessionModule
from sheepy_qa.local_screen_session import LocalScreenSession
from sheepy_qa.screen_preparation import ensureScreen


def replay(monkeypatch, tmp_path, frames):
    samples = Path(__file__).resolve().parents[2] / "docs/samples"
    black = tmp_path / "black.png"
    Image.new("RGB", (640, 360), "black").save(black)
    resized = tmp_path / "resized.png"
    Image.new("RGB", (1858, 1057), "black").save(resized)
    images = {"LOBBY": samples / "lobby-dim-start.png",
              "GAMEPLAY": samples / "gameplay-language-false-positive.png", "BLACK": black,
              "RESIZED": resized}
    records = {}
    inputs = []
    elapsed = [0.0]
    index = [0]

    def findWindow(fragments):
        return SimpleNamespace(isForeground=frames[min(index[0], len(frames) - 1)] != "UNFOCUSED")

    def capture(window, output):
        frame = frames[min(index[0], len(frames) - 1)]
        index[0] += 1
        return images[frame]

    monkeypatch.setattr(sessionModule, "findWindowByProcessNameFragments", findWindow)
    monkeypatch.setattr(sessionModule, "captureWindowScreenshot", capture)
    monkeypatch.setattr(sessionModule, "pressEnter", lambda: inputs.append(elapsed[0]))
    writer = SimpleNamespace(writeJson=lambda directory, name, data: records.__setitem__(name, data))
    session = LocalScreenSession(writer, tmp_path)
    result = ensureScreen("GAMEPLAY", session.observe, session.enter, timeoutSeconds=4,
                          intervalSeconds=0.5, clock=lambda: elapsed[0],
                          pause=lambda seconds: elapsed.__setitem__(0, elapsed[0] + seconds))
    return result, inputs, records


def test_real_image_classifiers_connect_lobby_loading_and_gameplay(monkeypatch, tmp_path):
    result, inputs, records = replay(monkeypatch, tmp_path, ["LOBBY", "BLACK", "GAMEPLAY"])
    assert result.ready
    assert inputs == [0.0]
    assert result.events[-1]["elapsed"] == 3.0
    assert records["prepare-000.json"]["lobby"].startJourneyVisible
    assert records["prepare-001.json"]["state"] == "BLACK"
    assert records["prepare-002.json"]["state"] == "GAMEPLAY"
    assert not records["prepare-002.json"]["language"].isLanguageSelectionLike


def test_replay_without_loading_never_completes(monkeypatch, tmp_path):
    result, inputs, _ = replay(monkeypatch, tmp_path, ["LOBBY", "GAMEPLAY"])
    assert not result.ready
    assert inputs == [0.0]


def test_gameplay_image_without_lobby_reference_never_receives_enter(monkeypatch, tmp_path):
    result, inputs, _ = replay(monkeypatch, tmp_path, ["GAMEPLAY"])
    assert not result.ready
    assert result.actual == "POST_LANGUAGE"
    assert inputs == []


def test_focus_loss_after_loading_stops_replay(monkeypatch, tmp_path):
    result, inputs, records = replay(monkeypatch, tmp_path, ["LOBBY", "BLACK", "UNFOCUSED"])
    assert not result.ready
    assert inputs == [0.0]
    assert result.events[-1]["foreground"] is False
    assert len(records) == 2


@pytest.mark.parametrize("frames,expectedInputs", [
    (["LOBBY", "RESIZED"], [0.0]),
    (["BLACK", "RESIZED"], []),
    (["LOBBY", "BLACK", "RESIZED"], [0.0]),
])
def test_size_change_stops_before_comparison_and_keeps_input_history(monkeypatch, tmp_path, frames, expectedInputs):
    monkeypatch.setattr(sessionModule, "compareImages", lambda *args: pytest.fail("크기 변경 후 비교 금지"))
    result, inputs, records = replay(monkeypatch, tmp_path, frames)
    assert not result.ready
    assert result.actual == "UNKNOWN"
    assert "화면 크기 변경" in result.reason
    assert inputs == expectedInputs
    completed = [event for event in result.events if event.get("action") == "ENTER"]
    assert len(completed) == len(expectedInputs)
    assert result.events[-1]["phase"] == "observe"
    last = records[f"prepare-{len(frames) - 1:03d}.json"]
    assert last["state"] == "SCREEN_SIZE_CHANGED"
    assert last["expectedSize"] == (640, 360)
    assert last["actualSize"] == (1858, 1057)


def test_prepare_json_keeps_completed_enter_when_next_capture_fails(monkeypatch, tmp_path):
    session = LocalScreenSession(EvidenceWriter(tmp_path), tmp_path)
    observations = iter([ScreenObservation("LOBBY")])

    def observe():
        try:
            return next(observations)
        except StopIteration:
            raise OSError("rendering window lost")

    monkeypatch.setattr(sessionModule, "findWindowByProcessNameFragments", lambda fragments: None)
    monkeypatch.setattr(session, "observe", observe)
    monkeypatch.setattr(session, "enter", lambda: None)
    result = session.prepare("GAMEPLAY")
    saved = json.loads((tmp_path / "preparation.json").read_text(encoding="utf-8"))
    assert not result.ready
    assert saved["actual"] == "UNKNOWN"
    assert saved["events"] == result.events
    assert any(event.get("action") == "ENTER" for event in saved["events"])
    assert saved["events"][-1]["error"] == "OSError"
