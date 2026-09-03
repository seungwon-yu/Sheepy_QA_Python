"""Freeze detection helpers."""

from dataclasses import dataclass

from sheepy_qa.image_diff import ImageDiffResult


@dataclass(frozen=True)
class FreezeObservationResult:
    comparisonCount: int
    visibleChangeCount: int
    maxChangedPixelRatio: float
    averageChangedPixelRatio: float
    resultState: str
    reason: str


def summarizeFreezeObservation(
    diffs: list[ImageDiffResult],
    minVisibleChangeCount: int = 1,
    freezeThreshold: float = 0.001
) -> FreezeObservationResult:
    if not diffs:
        return FreezeObservationResult(
            comparisonCount=0,
            visibleChangeCount=0,
            maxChangedPixelRatio=0,
            averageChangedPixelRatio=0,
            resultState="REVIEW_REQUIRED",
            reason="비교 가능한 screenshot 쌍이 없어 프리즈 여부를 판단할 수 없다."
        )

    changedPixelRatios = [diff.changedPixelRatio for diff in diffs]
    visibleChangeCount = sum(1 for ratio in changedPixelRatios if ratio >= freezeThreshold)
    maxChangedPixelRatio = max(changedPixelRatios)
    averageChangedPixelRatio = sum(changedPixelRatios) / len(changedPixelRatios)

    if visibleChangeCount >= minVisibleChangeCount:
        return FreezeObservationResult(
            comparisonCount=len(diffs),
            visibleChangeCount=visibleChangeCount,
            maxChangedPixelRatio=round(maxChangedPixelRatio, 4),
            averageChangedPixelRatio=round(averageChangedPixelRatio, 4),
            resultState="FREEZE_NOT_DETECTED",
            reason="연속 screenshot 비교에서 화면 변화가 관찰되어 프리즈로 판단하지 않는다."
        )

    return FreezeObservationResult(
        comparisonCount=len(diffs),
        visibleChangeCount=visibleChangeCount,
        maxChangedPixelRatio=round(maxChangedPixelRatio, 4),
        averageChangedPixelRatio=round(averageChangedPixelRatio, 4),
        resultState="REVIEW_REQUIRED",
        reason="연속 screenshot 변화가 거의 없지만 현재 장면이 정적 화면일 가능성이 있어 제품 프리즈로 단정하지 않는다."
    )
