from sheepy_qa.judgement import JudgementCondition, createJudgementRecord


def test_create_judgement_record_returns_pass_when_all_conditions_pass() -> None:
    record = createJudgementRecord(
        expectedResult="VISIBLE_SCREEN",
        actualResult="VISIBLE_SCREEN",
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition("기대 신호", True, True, True, "signal.json")
        ],
        forbiddenSignals=[
            JudgementCondition("이상 신호", False, False, True, "signal.json")
        ]
    )

    assert record.result == "PASS"


def test_create_judgement_record_returns_fail_when_expected_signal_is_missing() -> None:
    record = createJudgementRecord(
        expectedResult="LANGUAGE_SELECTION_SCREEN",
        actualResult="REVIEW_REQUIRED",
        actionPerformed=True,
        expectedSignals=[
            JudgementCondition("언어 선택 항목", "3개 이상", 0, False, "analysis.json")
        ],
        forbiddenSignals=[]
    )

    assert record.result == "FAIL"


def test_create_judgement_record_returns_review_required_when_action_is_not_performed() -> None:
    record = createJudgementRecord(
        expectedResult="INPUT_RESPONSE",
        actualResult="REVIEW_REQUIRED",
        actionPerformed=False,
        expectedSignals=[],
        forbiddenSignals=[]
    )

    assert record.result == "REVIEW_REQUIRED"
