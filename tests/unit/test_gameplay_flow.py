from sheepy_qa.gameplay_flow import summarizeGameplayFlow
from sheepy_qa.gameplay_screen import GameplayScreenResult
from sheepy_qa.image_diff import ImageDiffResult


def createGameplayResult(isCandidate: bool = True) -> GameplayScreenResult:
    return GameplayScreenResult(
        screenState="GAMEPLAY_SCREEN_CANDIDATE" if isCandidate else "BLACK_SCREEN",
        isGameplayScreenCandidate=isCandidate,
        reason="test"
    )


def createDiff(changedPixelRatio: float) -> ImageDiffResult:
    return ImageDiffResult(
        width=100,
        height=100,
        sampledPixelCount=100,
        changedPixelRatio=changedPixelRatio,
        averageChannelDifference=10,
        hasVisibleChange=changedPixelRatio >= 0.01
    )


def test_summarize_gameplay_flow_accepts_clear_input_delta() -> None:
    result = summarizeGameplayFlow(
        gameplayScreenResult=createGameplayResult(),
        idleDiff=createDiff(0.01),
        inputDiff=createDiff(0.04)
    )

    assert result.resultState == "BASIC_GAMEPLAY_FLOW_DETECTED"
    assert result.inputChangeDelta == 0.03


def test_summarize_gameplay_flow_rejects_missing_gameplay_precondition() -> None:
    result = summarizeGameplayFlow(
        gameplayScreenResult=createGameplayResult(isCandidate=False),
        idleDiff=createDiff(0.01),
        inputDiff=createDiff(0.04)
    )

    assert result.resultState == "BLACK_SCREEN"


def test_summarize_gameplay_flow_requires_input_delta() -> None:
    result = summarizeGameplayFlow(
        gameplayScreenResult=createGameplayResult(),
        idleDiff=createDiff(0.02),
        inputDiff=createDiff(0.021)
    )

    assert result.resultState == "INPUT_RESPONSE_NOT_CLEAR"
