from sheepy_qa.stability import StabilitySample, summarizeStabilitySamples


def test_summarize_stability_samples_passes_when_all_samples_are_valid() -> None:
    result = summarizeStabilitySamples(
        samples=[
            StabilitySample(
                elapsedSeconds=0,
                processAlive=True,
                screenshotSaved=True,
                screenshotFileName="sample-0.png"
            ),
            StabilitySample(
                elapsedSeconds=5,
                processAlive=True,
                screenshotSaved=True,
                screenshotFileName="sample-5.png"
            )
        ],
        durationSeconds=5
    )

    assert result.resultState == "STABLE_SHORT_RUN"
    assert result.failedSampleCount == 0


def test_summarize_stability_samples_detects_process_exit() -> None:
    result = summarizeStabilitySamples(
        samples=[
            StabilitySample(
                elapsedSeconds=0,
                processAlive=True,
                screenshotSaved=True,
                screenshotFileName="sample-0.png"
            ),
            StabilitySample(
                elapsedSeconds=5,
                processAlive=False,
                screenshotSaved=False,
                screenshotFileName=None
            )
        ],
        durationSeconds=5
    )

    assert result.resultState == "PROCESS_EXITED_DURING_OBSERVATION"
    assert result.failedSampleCount == 1


def test_summarize_stability_samples_requires_observation_samples() -> None:
    result = summarizeStabilitySamples(samples=[], durationSeconds=5)

    assert result.resultState == "REVIEW_REQUIRED"
    assert result.sampleCount == 0
