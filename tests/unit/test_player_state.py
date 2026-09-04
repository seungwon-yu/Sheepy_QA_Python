from sheepy_qa.lobby_menu import LobbyMenuAnalysisResult
from sheepy_qa.player_state import classifyPlayerStateFromLobby


def createLobbyAnalysis(continueVisible: bool, startJourneyVisible: bool) -> LobbyMenuAnalysisResult:
    return LobbyMenuAnalysisResult(
        screenState="test",
        continueVisible=continueVisible,
        startJourneyVisible=startJourneyVisible,
        playerStateHint="PLAYER-UNKNOWN",
        optionSignals=[],
        reason="test"
    )


def test_classify_player_state_detects_first_run_candidate() -> None:
    result = classifyPlayerStateFromLobby(createLobbyAnalysis(continueVisible=False, startJourneyVisible=True))

    assert result.playerState == "PLAYER_NEW"
    assert result.isFirstRunCandidate is True
    assert result.isReturningCandidate is False


def test_classify_player_state_detects_returning_candidate() -> None:
    result = classifyPlayerStateFromLobby(createLobbyAnalysis(continueVisible=True, startJourneyVisible=True))

    assert result.playerState == "PLAYER_RETURNING"
    assert result.isFirstRunCandidate is False
    assert result.isReturningCandidate is True


def test_classify_player_state_returns_unknown_without_lobby_signals() -> None:
    result = classifyPlayerStateFromLobby(createLobbyAnalysis(continueVisible=False, startJourneyVisible=False))

    assert result.playerState == "PLAYER_UNKNOWN"
    assert result.isFirstRunCandidate is False
    assert result.isReturningCandidate is False
