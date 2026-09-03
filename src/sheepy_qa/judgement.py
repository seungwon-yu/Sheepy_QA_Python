"""Judgement basis helpers for evidence records."""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class JudgementCondition:
    name: str
    expected: Any
    actual: Any
    passed: bool
    evidenceKey: str


@dataclass(frozen=True)
class JudgementRecord:
    result: str
    expectedResult: str
    actualResult: str
    actionPerformed: bool
    expectedSignals: list[JudgementCondition]
    forbiddenSignals: list[JudgementCondition]
    blockingConditions: list[JudgementCondition]
    judgementBasis: str


def createJudgementRecord(
    expectedResult: str,
    actualResult: str,
    actionPerformed: bool,
    expectedSignals: list[JudgementCondition],
    forbiddenSignals: list[JudgementCondition],
    blockingConditions: list[JudgementCondition] | None = None
) -> JudgementRecord:
    blockingConditions = blockingConditions or []
    hasBlockingCondition = any(condition.passed is False for condition in blockingConditions)
    hasExpectedSignalFailure = any(condition.passed is False for condition in expectedSignals)
    hasForbiddenSignalFailure = any(condition.passed is False for condition in forbiddenSignals)

    if hasBlockingCondition or actionPerformed is False:
        result = "REVIEW_REQUIRED"
    elif hasExpectedSignalFailure or hasForbiddenSignalFailure:
        result = "FAIL"
    else:
        result = "PASS"

    return JudgementRecord(
        result=result,
        expectedResult=expectedResult,
        actualResult=actualResult,
        actionPerformed=actionPerformed,
        expectedSignals=expectedSignals,
        forbiddenSignals=forbiddenSignals,
        blockingConditions=blockingConditions,
        judgementBasis=createJudgementBasis(
            result=result,
            actionPerformed=actionPerformed,
            expectedSignals=expectedSignals,
            forbiddenSignals=forbiddenSignals,
            blockingConditions=blockingConditions
        )
    )


def createJudgementBasis(
    result: str,
    actionPerformed: bool,
    expectedSignals: list[JudgementCondition],
    forbiddenSignals: list[JudgementCondition],
    blockingConditions: list[JudgementCondition]
) -> str:
    failedExpectedSignals = [condition.name for condition in expectedSignals if condition.passed is False]
    failedForbiddenSignals = [condition.name for condition in forbiddenSignals if condition.passed is False]
    failedBlockingConditions = [condition.name for condition in blockingConditions if condition.passed is False]

    if result == "PASS":
        return "테스트 동작이 수행되었고, 기대 신호가 확인되었으며, 발생하면 안 되는 이상 신호가 검출되지 않았다."

    if actionPerformed is False:
        return "테스트 동작 수행 여부가 확인되지 않아 제품 결함으로 단정하지 않고 검토가 필요하다."

    if failedBlockingConditions:
        return f"사전조건 또는 관찰 조건을 충족하지 못해 검토가 필요하다: {', '.join(failedBlockingConditions)}"

    failedSignals = failedExpectedSignals + failedForbiddenSignals
    return f"테스트 동작은 수행되었으나 판정 조건을 충족하지 못했다: {', '.join(failedSignals)}"
