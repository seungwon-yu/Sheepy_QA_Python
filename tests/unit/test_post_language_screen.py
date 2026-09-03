from sheepy_qa.image_analysis import ImageAnalysisResult
from sheepy_qa.language_screen import LanguageScreenAnalysisResult
from sheepy_qa.post_language_screen import classifyPostLanguageScreen


def createScreenAnalysis(isMostlyBlack: bool, uniqueColorCount: int) -> ImageAnalysisResult:
    return ImageAnalysisResult(
        width=100,
        height=100,
        sampledPixelCount=100,
        averageBrightness=30,
        darkPixelRatio=0.2,
        uniqueSampledColorCount=uniqueColorCount,
        isMostlyBlack=isMostlyBlack
    )


def createLanguageAnalysis(isLanguageSelectionLike: bool) -> LanguageScreenAnalysisResult:
    return LanguageScreenAnalysisResult(
        width=100,
        height=100,
        sampledPixelCount=100,
        visibleOptionCount=2 if isLanguageSelectionLike else 0,
        centralDarkPixelRatio=0.8,
        centralSaturatedPixelRatio=0.05,
        isLanguageSelectionLike=isLanguageSelectionLike
    )


def test_classify_post_language_screen_accepts_visible_non_language_screen() -> None:
    result = classifyPostLanguageScreen(
        screenAnalysis=createScreenAnalysis(isMostlyBlack=False, uniqueColorCount=20),
        languageAnalysis=createLanguageAnalysis(isLanguageSelectionLike=False)
    )

    assert result.screenState == "POST_LANGUAGE_SCREEN"
    assert result.isPostLanguageScreen is True


def test_classify_post_language_screen_rejects_language_selection_screen() -> None:
    result = classifyPostLanguageScreen(
        screenAnalysis=createScreenAnalysis(isMostlyBlack=False, uniqueColorCount=20),
        languageAnalysis=createLanguageAnalysis(isLanguageSelectionLike=True)
    )

    assert result.screenState == "LANGUAGE_SELECTION_SCREEN"
    assert result.isPostLanguageScreen is False


def test_classify_post_language_screen_rejects_black_screen() -> None:
    result = classifyPostLanguageScreen(
        screenAnalysis=createScreenAnalysis(isMostlyBlack=True, uniqueColorCount=1),
        languageAnalysis=createLanguageAnalysis(isLanguageSelectionLike=False)
    )

    assert result.screenState == "BLACK_SCREEN"
    assert result.isPostLanguageScreen is False
