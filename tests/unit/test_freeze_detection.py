from sheepy_qa.freeze_detection import summarizeFreezeObservation
from sheepy_qa.image_diff import ImageDiffResult


def createDiff(changedPixelRatio: float) -> ImageDiffResult:
    return ImageDiffResult(
        width=100,
        height=100,
        sampledPixelCount=100,
        changedPixelRatio=changedPixelRatio,
        averageChannelDifference=1,
        hasVisibleChange=changedPixelRatio >= 0.01
    )


def test_summarize_freeze_observation_passes_when_change_is_visible() -> None:
    result = summarizeFreezeObservation([createDiff(0.0), createDiff(0.02)])

    assert result.resultState == "FREEZE_NOT_DETECTED"
    assert result.visibleChangeCount == 1


def test_summarize_freeze_observation_requires_review_when_no_change_is_visible() -> None:
    result = summarizeFreezeObservation([createDiff(0.0), createDiff(0.0005)])

    assert result.resultState == "REVIEW_REQUIRED"
    assert result.visibleChangeCount == 0


def test_summarize_freeze_observation_requires_comparisons() -> None:
    result = summarizeFreezeObservation([])

    assert result.resultState == "REVIEW_REQUIRED"
    assert result.comparisonCount == 0
