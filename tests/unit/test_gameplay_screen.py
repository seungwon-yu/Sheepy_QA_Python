from sheepy_qa.gameplay_screen import classifyGameplayScreen
from sheepy_qa.image_analysis import ImageAnalysisResult
from sheepy_qa.image_diff import ImageDiffResult
from sheepy_qa.language_screen import LanguageScreenAnalysisResult
from sheepy_qa.lobby_menu import LobbyMenuAnalysisResult


def createScreenAnalysis(isMostlyBlack: bool = False) -> ImageAnalysisResult:
    return ImageAnalysisResult(
        width=100,
        height=100,
        sampledPixelCount=100,
        averageBrightness=40,
        darkPixelRatio=0.2,
        uniqueSampledColorCount=20,
        isMostlyBlack=isMostlyBlack
    )


def createLanguageAnalysis(isLanguageSelectionLike: bool = False) -> LanguageScreenAnalysisResult:
    return LanguageScreenAnalysisResult(
        width=100,
        height=100,
        sampledPixelCount=100,
        visibleOptionCount=0,
        centralDarkPixelRatio=0.1,
        centralSaturatedPixelRatio=0.01,
        isLanguageSelectionLike=isLanguageSelectionLike
    )


def createLobbyAnalysis(hasCta: bool = False) -> LobbyMenuAnalysisResult:
    return LobbyMenuAnalysisResult(
        screenState="LOBBY_MENU_WITH_CONTINUE_ONLY" if hasCta else "REVIEW_REQUIRED",
        continueVisible=hasCta,
        startJourneyVisible=False,
        playerStateHint="PLAYER-RETURNING" if hasCta else "PLAYER-UNKNOWN",
        optionSignals=[],
        reason="test"
    )


def createDiff(changedPixelRatio: float = 0.12) -> ImageDiffResult:
    return ImageDiffResult(
        width=100,
        height=100,
        sampledPixelCount=100,
        changedPixelRatio=changedPixelRatio,
        averageChannelDifference=20,
        hasVisibleChange=changedPixelRatio >= 0.01
    )


def test_classify_gameplay_screen_accepts_changed_non_lobby_screen() -> None:
    result = classifyGameplayScreen(
        screenAnalysis=createScreenAnalysis(),
        languageAnalysis=createLanguageAnalysis(),
        lobbyMenuAnalysis=createLobbyAnalysis(),
        transitionDiff=createDiff()
    )

    assert result.screenState == "GAMEPLAY_SCREEN_CANDIDATE"
    assert result.isGameplayScreenCandidate is True


def test_classify_gameplay_screen_rejects_remaining_lobby_menu() -> None:
    result = classifyGameplayScreen(
        screenAnalysis=createScreenAnalysis(),
        languageAnalysis=createLanguageAnalysis(),
        lobbyMenuAnalysis=createLobbyAnalysis(hasCta=True),
        transitionDiff=createDiff()
    )

    assert result.screenState == "LOBBY_MENU_SCREEN"
    assert result.isGameplayScreenCandidate is False


def test_classify_gameplay_screen_requires_visible_transition() -> None:
    result = classifyGameplayScreen(
        screenAnalysis=createScreenAnalysis(),
        languageAnalysis=createLanguageAnalysis(),
        lobbyMenuAnalysis=createLobbyAnalysis(),
        transitionDiff=createDiff(changedPixelRatio=0.01)
    )

    assert result.screenState == "REVIEW_REQUIRED"
    assert result.isGameplayScreenCandidate is False
