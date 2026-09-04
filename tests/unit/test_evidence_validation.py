from sheepy_qa.evidence import EvidenceWriter
from sheepy_qa.evidence_validation import validateEvidenceFiles
from sheepy_qa.judgement import JudgementCondition, createJudgementRecord


def test_tc_008_failure_evidence_files_are_saved(tmp_path) -> None:
    writer = EvidenceWriter(baseDir=tmp_path)
    runDir = writer.createRunDir("TC-008")
    judgementRecord = createJudgementRecord(
        expectedResult="EVIDENCE_COMPLETE",
        actualResult="REVIEW_REQUIRED",
        actionPerformed=False,
        expectedSignals=[],
        forbiddenSignals=[],
        blockingConditions=[
            JudgementCondition(
                name="의도된 evidence 검증 조건",
                expected=True,
                actual=False,
                passed=False,
                evidenceKey="simulated-state.json"
            )
        ]
    )

    writer.writeJson(runDir, "simulated-state.json", {"state": "missing-precondition"})
    writer.writeJson(runDir, "execution-log.json", {"message": "simulated evidence validation"})
    writer.writeJson(runDir, "judgement.json", judgementRecord)
    validationResult = validateEvidenceFiles(
        runDir=runDir,
        expectedFiles=[
            "simulated-state.json",
            "execution-log.json",
            "judgement.json"
        ]
    )

    assert judgementRecord.result == "REVIEW_REQUIRED"
    assert validationResult.isComplete is True
    assert validationResult.missingFiles == []


def test_validate_evidence_files_reports_missing_files(tmp_path) -> None:
    writer = EvidenceWriter(baseDir=tmp_path)
    runDir = writer.createRunDir("TC-008")
    writer.writeJson(runDir, "judgement.json", {"result": "REVIEW_REQUIRED"})

    validationResult = validateEvidenceFiles(
        runDir=runDir,
        expectedFiles=[
            "judgement.json",
            "missing-screenshot.png"
        ]
    )

    assert validationResult.isComplete is False
    assert validationResult.missingFiles == ["missing-screenshot.png"]
