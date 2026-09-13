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
    result = ensureScreen(target, observe, lambda: inputs.append("ENTER"), timeoutSeconds=4,
                          intervalSeconds=1, clock=lambda: clock[0], pause=lambda seconds: clock.__setitem__(0, clock[0] + seconds))
    return result, inputs


def test_language_lobby_gameplay_transition_is_bounded():
    result, inputs = run([ScreenObservation(s) for s in ["LANGUAGE", "LOBBY", "GAMEPLAY"]])
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
