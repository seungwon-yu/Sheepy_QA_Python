import pytest
from sheepy_qa.process_check import ProcessSnapshot
from sheepy_qa.process_observation import observeProcessUntil


class Clock:
    now = 0
    def read(self):
        return self.now
    def sleep(self, seconds):
        self.now += seconds


def test_initial_process_is_not_reported_as_new_launch():
    clock = Clock()
    result = observeProcessUntil(lambda: [ProcessSnapshot("Sheepy.exe", 123, "running")],
                                 clock=clock.read, sleep=clock.sleep)
    assert result.detected and result.initialProcessPresent
    assert result.elapsedSeconds == 0
    assert len(result.samples) == 1


def test_process_detected_at_deadline_preserves_prior_absence():
    clock = Clock()
    result = observeProcessUntil(lambda: [] if clock.now < 2 else [ProcessSnapshot("Sheepy.exe", 1, "running")],
                                 2, 1, clock.read, clock.sleep)
    assert result.detected and not result.initialProcessPresent
    assert [row["detected"] for row in result.samples] == [False, False, True]
    assert result.elapsedSeconds == 2


def test_timeout_preserves_samples_without_oversleep():
    clock = Clock()
    result = observeProcessUntil(lambda: [], 2.5, 2, clock.read, clock.sleep)
    assert not result.detected
    assert [row["elapsedSeconds"] for row in result.samples] == [0, 2, 2.5]


@pytest.mark.parametrize("timeout,interval", [(-1, 1), (1, 0), (1, -1), (float("inf"), 1), (1, float("nan"))])
def test_invalid_polling_limits_rejected(timeout, interval):
    with pytest.raises(ValueError):
        observeProcessUntil(lambda: [], timeout, interval)
