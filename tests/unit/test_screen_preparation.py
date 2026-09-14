import pytest
from sheepy_qa.screen_preparation import ScreenObservation, ensureScreen


def run(states, target="GAMEPLAY"):
    sequence = iter(states)
    current = [states[-1]]
    clock = [0.0]
    inputs = []
    def observe():
        current[0] = next(sequence, current[0])
        return current[0]
    result = ensureScreen(target, observe, lambda: inputs.append("ENTER"), timeoutSeconds=6,
                          intervalSeconds=1, clock=lambda: clock[0], pause=lambda seconds: clock.__setitem__(0, clock[0] + seconds))
    return result, inputs


def test_language_lobby_gameplay_transition_is_bounded():
    result, inputs = run([ScreenObservation(s) for s in ["LANGUAGE", "LOBBY", "BLACK", "GAMEPLAY"]])
    assert result.ready
    assert inputs == ["ENTER", "ENTER"]


def test_ready_lobby_does_not_receive_input():
    result, inputs = run([ScreenObservation("LOBBY")], "LOBBY")
    assert result.ready and inputs == []


def test_stuck_language_is_not_repeatedly_pressed():
    result, inputs = run([ScreenObservation("LANGUAGE")])
    assert not result.ready and inputs == ["ENTER"]
    assert "시간 초과" in result.reason


@pytest.mark.parametrize("state,foreground", [("UNKNOWN", True), ("LOBBY", False)])
def test_unknown_or_unfocused_screen_is_not_operated(state, foreground):
    result, inputs = run([ScreenObservation(state, foreground)])
    assert not result.ready and inputs == []


def test_black_transition_can_recover_without_input():
    result, inputs = run([ScreenObservation("BLACK"), ScreenObservation("LOBBY")], "LOBBY")
    assert result.ready and inputs == []


def test_static_unknown_gameplay_is_not_assumed_to_be_gameplay():
    result, inputs = run([ScreenObservation("POST_LANGUAGE")])
    assert not result.ready and inputs == []


def test_transient_gameplay_candidate_does_not_complete_preparation():
    result, inputs = run([ScreenObservation(s) for s in ["LOBBY", "GAMEPLAY", "BLACK", "BLACK", "BLACK"]])
    assert not result.ready
    assert inputs == ["ENTER"]

def test_gameplay_candidate_must_persist_for_two_seconds():
    result, inputs = run([ScreenObservation("GAMEPLAY")])
    assert result.ready
    assert result.events[-1]["elapsed"] == 2
    assert inputs == []


def test_lobby_fade_without_loading_is_not_gameplay_ready():
    result, inputs = run([ScreenObservation(s) for s in ["LOBBY", "GAMEPLAY"]])
    assert not result.ready
    assert inputs == ["ENTER"]


def test_false_language_candidate_after_lobby_never_sends_second_enter():
    result, inputs = run([ScreenObservation(s) for s in ["LOBBY", "BLACK", "GAMEPLAY", "LANGUAGE"]])
    assert not result.ready
    assert inputs == ["ENTER"]
    assert "추가 입력 중단" in result.reason


@pytest.mark.parametrize("phase", ["observe", "enter", "pause"])
def test_callback_error_keeps_prior_observation_and_input_status(phase):
    observations = [0]
    inputs = []

    def observe():
        observations[0] += 1
        if phase == "observe" and observations[0] == 2:
            raise OSError("capture unavailable")
        return ScreenObservation("LOBBY")

    def enter():
        if phase == "enter":
            raise RuntimeError("input incomplete")
        inputs.append("ENTER")

    def pause(seconds):
        if phase == "pause":
            raise RuntimeError("wait interrupted")

    result = ensureScreen("GAMEPLAY", observe, enter, clock=lambda: 0, pause=pause)
    assert not result.ready
    assert result.actual == "UNKNOWN"
    assert result.events[0]["state"] == "LOBBY"
    assert result.events[-1]["phase"] == phase
    assert result.events[-1]["lastState"] == "LOBBY"
    actions = [event.get("action") for event in result.events if "action" in event]
    assert actions == (["ENTER_ATTEMPT"] if phase == "enter" else ["ENTER_ATTEMPT", "ENTER"])
    assert inputs == ([] if phase == "enter" else ["ENTER"])
