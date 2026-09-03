"""Stability observation helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StabilitySample:
    elapsedSeconds: float
    processAlive: bool
    screenshotSaved: bool
    screenshotFileName: str | None


@dataclass(frozen=True)
class StabilityObservationResult:
    durationSeconds: float
    sampleCount: int
    processAliveThroughout: bool
    screenshotSavedThroughout: bool
    failedSampleCount: int
    resultState: str


def summarizeStabilitySamples(
    samples: list[StabilitySample],
    durationSeconds: float
) -> StabilityObservationResult:
    if not samples:
        return StabilityObservationResult(
            durationSeconds=durationSeconds,
            sampleCount=0,
            processAliveThroughout=False,
            screenshotSavedThroughout=False,
            failedSampleCount=0,
            resultState="REVIEW_REQUIRED"
        )

    processAliveThroughout = all(sample.processAlive for sample in samples)
    screenshotSavedThroughout = all(sample.screenshotSaved for sample in samples)
    failedSampleCount = sum(
        1 for sample in samples if sample.processAlive is False or sample.screenshotSaved is False
    )

    if processAliveThroughout and screenshotSavedThroughout:
        resultState = "STABLE_SHORT_RUN"
    elif processAliveThroughout is False:
        resultState = "PROCESS_EXITED_DURING_OBSERVATION"
    else:
        resultState = "SCREENSHOT_CAPTURE_UNSTABLE"

    return StabilityObservationResult(
        durationSeconds=durationSeconds,
        sampleCount=len(samples),
        processAliveThroughout=processAliveThroughout,
        screenshotSavedThroughout=screenshotSavedThroughout,
        failedSampleCount=failedSampleCount,
        resultState=resultState
    )
