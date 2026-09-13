"""연속 화면 변화 관찰. 내부 게임 프리즈의 확정 판정이 아니다."""
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
    longestUnchangedSeconds: float = 0
    secondsSinceLastChange: float = 0

def summarizeFreezeObservation(
    diffs: list[ImageDiffResult],
    minVisibleChangeCount: int = 1,
    freezeThreshold: float = 0.001,
    intervalSeconds: float = 5,
    maxUnchangedSeconds: float = 10,
    sampleTimes: list[float] | None = None
) -> FreezeObservationResult:
    if intervalSeconds <= 0 or maxUnchangedSeconds <= 0:
        raise ValueError("관찰 간격과 무변화 제한 시간은 양수여야 한다.")
    if sampleTimes is not None and (len(sampleTimes) != len(diffs) + 1 or any(b <= a for a, b in zip(sampleTimes, sampleTimes[1:]))):
        raise ValueError("sampleTimes는 screenshot 수와 일치하고 증가해야 한다.")
    durations = [b - a for a, b in zip(sampleTimes, sampleTimes[1:])] if sampleTimes is not None else [intervalSeconds] * len(diffs)
    ratios = [diff.changedPixelRatio for diff in diffs]
    longest = trailing = 0
    for ratio, duration in zip(ratios, durations):
        trailing = trailing + duration if ratio < freezeThreshold else 0
        longest = max(longest, trailing)
    visible = sum(ratio >= freezeThreshold for ratio in ratios)
    observed = bool(ratios) and visible >= minVisibleChangeCount and longest < maxUnchangedSeconds
    return FreezeObservationResult(
        comparisonCount=len(ratios), visibleChangeCount=visible,
        maxChangedPixelRatio=max(ratios, default=0),
        averageChangedPixelRatio=round(sum(ratios) / len(ratios), 4) if ratios else 0,
        resultState="SCREEN_CHANGE_OBSERVED" if observed else "REVIEW_REQUIRED",
        reason="관찰 구간에서 화면 변화가 있고 연속 무변화 제한 미만이다. 내부 프리즈 부재를 보장하지 않는다." if observed else "비교 근거 부족 또는 연속 무변화 구간을 검토해야 한다. 정적 장면일 수 있어 제품 프리즈로 확정하지 않는다.",
        longestUnchangedSeconds=round(longest, 3), secondsSinceLastChange=round(trailing, 3)
    )
