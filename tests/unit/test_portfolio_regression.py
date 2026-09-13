from types import SimpleNamespace
from sheepy_qa.judgement import createJudgementRecord
from sheepy_qa.freeze_detection import summarizeFreezeObservation

def test_empty_observation_must_not_pass():
    record = createJudgementRecord("EXPECTED", "DIFFERENT", True, [], [])
    assert record.result == "REVIEW_REQUIRED"
    assert "기대 신호" in record.judgementBasis

def test_early_change_does_not_hide_later_stationary_period():
    result = summarizeFreezeObservation([SimpleNamespace(changedPixelRatio=r) for r in [0.1, 0, 0]])
    assert result.resultState == "REVIEW_REQUIRED"
    assert result.longestUnchangedSeconds == 10
    assert result.secondsSinceLastChange == 10

def test_observation_uses_real_sample_times():
    result = summarizeFreezeObservation([SimpleNamespace(changedPixelRatio=r) for r in [0.1, 0]], sampleTimes=[0, 2, 14])
    assert result.resultState == "REVIEW_REQUIRED"
    assert result.longestUnchangedSeconds == 12

def test_middle_stationary_period_is_not_hidden_by_final_change():
    result = summarizeFreezeObservation([SimpleNamespace(changedPixelRatio=r) for r in [0, 0, 0.1]])
    assert result.resultState == "REVIEW_REQUIRED"
    assert result.secondsSinceLastChange == 0
