"""사람이 라벨링한 화면 3장의 입력 반응 평가. 실제 이동/점프 판정이 아니다."""
import argparse
import json
from pathlib import Path

from sheepy_qa.image_diff import compareImages

INPUT_RESPONSE_THRESHOLD = 0.005


def evaluateSamples(samples, baseDir):
    ids = set()
    groups = {}
    rows = []
    for sample in samples:
        sampleId = sample["id"]
        split = sample["split"]
        group = sample["captureSession"]
        if sampleId in ids or not sampleId or not group:
            raise ValueError("sample id must be unique; captureSession is required")
        ids.add(sampleId)
        if split not in ("calibration", "evaluation"):
            raise ValueError("split must be calibration or evaluation")
        if group in groups and groups[group] != split:
            raise ValueError("same captureSession cannot cross splits")
        groups[group] = split
        expected = sample["expected"]
        if expected not in ("RESPONSE", "NO_RESPONSE"):
            raise ValueError("expected must be RESPONSE or NO_RESPONSE")
        if not sample.get("reviewer") or not sample.get("reason") or not sample.get("environment"):
            raise ValueError("human reviewer, reason and environment are required")
        if type(sample["preconditionsMet"]) is not bool:
            raise ValueError("preconditionsMet must be boolean")
        delta = None
        predicted = "REVIEW_REQUIRED"
        if sample["preconditionsMet"]:
            before, idle, after = [Path(baseDir) / sample[key] for key in ("before", "idle", "after")]
            idleDiff = compareImages(before, idle)
            inputDiff = compareImages(idle, after)
            delta = round(inputDiff.changedPixelRatio - idleDiff.changedPixelRatio, 4)
            predicted = "RESPONSE" if delta >= INPUT_RESPONSE_THRESHOLD else "NO_RESPONSE"
        rows.append({"id": sampleId, "split": split, "expected": expected,
                     "predicted": predicted, "delta": delta})
    selected = [row for row in rows if row["split"] == "evaluation"]
    counts = {key: 0 for key in ("truePositive", "trueNegative", "falsePositive", "falseNegative", "reviewRequired")}
    for row in selected:
        if row["predicted"] == "REVIEW_REQUIRED":
            counts["reviewRequired"] += 1
        else:
            key = {("RESPONSE", "RESPONSE"): "truePositive", ("NO_RESPONSE", "NO_RESPONSE"): "trueNegative",
                   ("NO_RESPONSE", "RESPONSE"): "falsePositive", ("RESPONSE", "NO_RESPONSE"): "falseNegative"}
            counts[key[(row["expected"], row["predicted"])]] += 1
    return {"status": "EVALUATED" if selected else "NOT_EVALUATED", "threshold": INPUT_RESPONSE_THRESHOLD,
            "evaluationCount": len(selected), "counts": counts, "samples": rows,
            "scope": "사람이 확인한 입력 시각 반응만 평가; 게임 동작 성공 정확도가 아님"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = evaluateSamples(data["samples"], args.manifest.parent)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(result["status"])


if __name__ == "__main__":
    main()
