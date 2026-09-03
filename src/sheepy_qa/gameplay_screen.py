"""Gameplay screen classification helpers."""

from dataclasses import dataclass

from sheepy_qa.image_analysis import ImageAnalysisResult
from sheepy_qa.image_diff import ImageDiffResult
from sheepy_qa.language_screen import LanguageScreenAnalysisResult
from sheepy_qa.lobby_menu import LobbyMenuAnalysisResult


@dataclass(frozen=True)
class GameplayScreenResult:
    screenState: str
    isGameplayScreenCandidate: bool
    reason: str


def classifyGameplayScreen(
    screenAnalysis: ImageAnalysisResult,
    languageAnalysis: LanguageScreenAnalysisResult,
    lobbyMenuAnalysis: LobbyMenuAnalysisResult,
    transitionDiff: ImageDiffResult
) -> GameplayScreenResult:
    if screenAnalysis.isMostlyBlack:
        return GameplayScreenResult(
            screenState="BLACK_SCREEN",
            isGameplayScreenCandidate=False,
            reason="화면이 검은 화면으로 분석되어 플레이 화면으로 판단할 수 없다."
        )

    if languageAnalysis.isLanguageSelectionLike:
        return GameplayScreenResult(
            screenState="LANGUAGE_SELECTION_SCREEN",
            isGameplayScreenCandidate=False,
            reason="언어 선택 화면 특징이 남아 있어 플레이 화면으로 판단하지 않는다."
        )

    if lobbyMenuAnalysis.continueVisible or lobbyMenuAnalysis.startJourneyVisible:
        return GameplayScreenResult(
            screenState="LOBBY_MENU_SCREEN",
            isGameplayScreenCandidate=False,
            reason="로비 CTA가 아직 관찰되어 플레이 화면으로 전환되었다고 판단하지 않는다."
        )

    if transitionDiff.changedPixelRatio >= 0.05 and screenAnalysis.uniqueSampledColorCount > 10:
        return GameplayScreenResult(
            screenState="GAMEPLAY_SCREEN_CANDIDATE",
            isGameplayScreenCandidate=True,
            reason="로비 CTA가 사라졌고 입력 전후 화면 변화와 충분한 시각 정보가 관찰되었다."
        )

    return GameplayScreenResult(
        screenState="REVIEW_REQUIRED",
        isGameplayScreenCandidate=False,
        reason="화면은 보이지만 플레이 화면 전환이라고 판단할 근거가 부족하다."
    )
