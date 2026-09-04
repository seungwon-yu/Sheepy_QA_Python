"""Player state classification helpers."""

from dataclasses import dataclass

from sheepy_qa.lobby_menu import LobbyMenuAnalysisResult


@dataclass(frozen=True)
class PlayerStateResult:
    playerState: str
    isFirstRunCandidate: bool
    isReturningCandidate: bool
    reason: str


def classifyPlayerStateFromLobby(lobbyMenuAnalysis: LobbyMenuAnalysisResult) -> PlayerStateResult:
    if lobbyMenuAnalysis.startJourneyVisible and not lobbyMenuAnalysis.continueVisible:
        return PlayerStateResult(
            playerState="PLAYER_NEW",
            isFirstRunCandidate=True,
            isReturningCandidate=False,
            reason="Start Your Journey만 관찰되어 최초 실행 유저 후보로 판단한다."
        )

    if lobbyMenuAnalysis.continueVisible:
        return PlayerStateResult(
            playerState="PLAYER_RETURNING",
            isFirstRunCandidate=False,
            isReturningCandidate=True,
            reason="Continue가 관찰되어 기존 플레이 유저 후보로 판단한다."
        )

    return PlayerStateResult(
        playerState="PLAYER_UNKNOWN",
        isFirstRunCandidate=False,
        isReturningCandidate=False,
        reason="로비 CTA 신호가 부족해 플레이어 상태를 판단하지 않는다."
    )
