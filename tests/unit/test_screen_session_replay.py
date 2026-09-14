"""보관 이미지와 실제 판정 함수를 연결한다. 실제 게임 실행 검증은 아니다."""
from pathlib import Path
from types import SimpleNamespace

from PIL import Image

import sheepy_qa.local_screen_session as sessionModule
from sheepy_qa.local_screen_session import LocalScreenSession
from sheepy_qa.screen_preparation import ensureScreen


def replay(monkeypatch, tmp_path, frames):
    samples = Path(__file__).resolve().parents[2] / "docs/samples"
    black = tmp_path / "black.png"
    Image.new("RGB", (640, 360), "black").save(black)
    images = {"LOBBY": samples / "lobby-dim-start.png",
              "GAMEPLAY": samples / "gameplay-language-false-positive.png", "BLACK": black}
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
