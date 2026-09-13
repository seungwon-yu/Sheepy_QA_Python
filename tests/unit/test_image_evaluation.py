import pytest
from PIL import Image
from sheepy_qa.image_evaluation import evaluateSamples


def sample(tmp_path, **changes):
    for name, color in [("before", "black"), ("idle", "black"), ("after", "white")]:
        Image.new("RGB", (12, 12), color).save(tmp_path / (name + ".png"))
    row = dict(id="synthetic-1", split="evaluation", captureSession="synthetic-session",
               expected="RESPONSE", reviewer="synthetic-fixture", reason="집계 회귀 검증용 인공 이미지",
               environment="unit-test", preconditionsMet=True,
               before="before.png", idle="idle.png", after="after.png")
    row.update(changes)
    return row


def test_empty_samples_do_not_claim_accuracy(tmp_path):
    result = evaluateSamples([], tmp_path)
    assert result["status"] == "NOT_EVALUATED"
    assert result["evaluationCount"] == 0


@pytest.mark.parametrize("expected,after,key", [("RESPONSE", "after.png", "truePositive"),
    ("NO_RESPONSE", "idle.png", "trueNegative"), ("NO_RESPONSE", "after.png", "falsePositive"),
    ("RESPONSE", "idle.png", "falseNegative")])
def test_confusion_counts_from_synthetic_images(tmp_path, expected, after, key):
    result = evaluateSamples([sample(tmp_path, expected=expected, after=after)], tmp_path)
    assert result["counts"][key] == 1
    assert sum(result["counts"].values()) == 1


def test_precondition_failure_is_review_not_success(tmp_path):
    result = evaluateSamples([sample(tmp_path, preconditionsMet=False)], tmp_path)
    assert result["counts"]["reviewRequired"] == 1
    assert result["counts"]["truePositive"] == 0


def test_calibration_samples_are_not_evaluation_results(tmp_path):
    result = evaluateSamples([sample(tmp_path, split="calibration")], tmp_path)
    assert result["status"] == "NOT_EVALUATED"


def test_same_recording_cannot_leak_across_splits(tmp_path):
    row = sample(tmp_path)
    with pytest.raises(ValueError, match="cross splits"):
        evaluateSamples([row, dict(row, id="another", split="calibration")], tmp_path)


def test_unreviewed_samples_rejected(tmp_path):
    with pytest.raises(ValueError, match="reviewer"):
        evaluateSamples([sample(tmp_path, reviewer="")], tmp_path)
