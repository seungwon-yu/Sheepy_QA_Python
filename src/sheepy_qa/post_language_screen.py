"""Post-language screen classification helpers."""

from dataclasses import dataclass

from sheepy_qa.image_analysis import ImageAnalysisResult
from sheepy_qa.language_screen import LanguageScreenAnalysisResult


@dataclass(frozen=True)
class PostLanguageScreenResult:
    screenState: str
    isPostLanguageScreen: bool
    reason: str


def classifyPostLanguageScreen(
    screenAnalysis: ImageAnalysisResult,
    languageAnalysis: LanguageScreenAnalysisResult
) -> PostLanguageScreenResult:
    if screenAnalysis.isMostlyBlack:
        return PostLanguageScreenResult(
            screenState="BLACK_SCREEN",
            isPostLanguageScreen=False,
            reason="화면이 검은 화면으로 분석되어 언어 선택 이후 화면으로 판단할 수 없다."
        )

    if languageAnalysis.isLanguageSelectionLike:
        return PostLanguageScreenResult(
            screenState="LANGUAGE_SELECTION_SCREEN",
            isPostLanguageScreen=False,
            reason="언어 선택 화면 특징이 남아 있어 언어 선택 이후 화면으로 판단하지 않는다."
        )

    if screenAnalysis.uniqueSampledColorCount > 10:
        return PostLanguageScreenResult(
            screenState="POST_LANGUAGE_SCREEN",
            isPostLanguageScreen=True,
            reason="검은 화면이 아니고 언어 선택 화면 특징이 없으며 충분한 시각 정보가 있다."
        )

    return PostLanguageScreenResult(
        screenState="REVIEW_REQUIRED",
        isPostLanguageScreen=False,
        reason="화면은 보이지만 언어 선택 이후 화면이라고 판단할 근거가 부족하다."
    )
