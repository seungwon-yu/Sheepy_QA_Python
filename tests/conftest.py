"""pytest 종료 코드와 별도로 미실행/판단 보류를 집계한다."""
import json
from datetime import datetime, timezone
from pathlib import Path

RESULTS = {}

def pytest_runtest_logreport(report):
    if report.when == "call" or (report.when == "setup" and (report.skipped or report.failed)):
        reason = str(report.longrepr) if report.longrepr else ""
        result = "REVIEW_REQUIRED" if report.skipped and "REVIEW_REQUIRED" in reason else (
            "NOT_RUN" if report.skipped else "FAIL" if report.failed else "PASS")
        RESULTS[report.nodeid] = {"test": report.nodeid, "result": result, "reason": reason}

def pytest_sessionfinish(session, exitstatus):
    directory = Path("artifacts/results")
    directory.mkdir(parents=True, exist_ok=True)
    counts = {key: sum(row["result"] == key for row in RESULTS.values()) for key in ["PASS", "FAIL", "REVIEW_REQUIRED", "NOT_RUN"]}
    scope = "SELECTED_TESTS_COMPLETE" if exitstatus == 0 and RESULTS and not any(counts[k] for k in ["FAIL", "REVIEW_REQUIRED", "NOT_RUN"]) else "INCOMPLETE_OR_FAILED"
    payload = {"createdAt": datetime.now(timezone.utc).isoformat(), "exitStatus": int(exitstatus), "scope": scope, "counts": counts, "tests": list(RESULTS.values())}
    (directory / "pytest-summary.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Sheepy 실행 요약", "", f"범위 판정: {scope}", "", "| 결과 | 건수 |", "| --- | --- |"]
    lines.extend(f"| {key} | {value} |" for key, value in counts.items())
    lines.extend(["", "단위 테스트 통과는 실제 게임 검증 완료를 의미하지 않는다. REVIEW_REQUIRED와 NOT_RUN을 통과율에 합산하지 않는다."])
    (directory / "pytest-summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
