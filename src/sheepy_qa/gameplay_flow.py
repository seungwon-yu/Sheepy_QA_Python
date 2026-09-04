"""Gameplay flow judgement helpers."""

from dataclasses import dataclass

from sheepy_qa.gameplay_screen import GameplayScreenResult
from sheepy_qa.image_diff import ImageDiffResult


@dataclass(frozen=True)
class GameplayFlowResult:
    resultState: str
    inputChangeDelta: float
    reason: str


def summarizeGameplayFlow(
    gameplayScreenResult: GameplayScreenResult,
    idleDiff: ImageDiffResult,
    inputDiff: ImageDiffResult,
    minInputChangeDelta: float = 0.005
) -> GameplayFlowResult:
    inputChangeDelta = round(inputDiff.changedPixelRatio - idleDiff.changedPixelRatio, 4)

    if not gameplayScreenResult.isGameplayScreenCandidate:
        return GameplayFlowResult(
            resultState=gameplayScreenResult.screenState,
            inputChangeDelta=inputChangeDelta,
            reason="플레이 화면 후보 사전조건을 충족하지 못해 기본 플레이 흐름을 판단하지 않는다."
        )

    if inputChangeDelta >= minInputChangeDelta:
        return GameplayFlowResult(
            resultState="BASIC_GAMEPLAY_FLOW_DETECTED",
            inputChangeDelta=inputChangeDelta,
            reason="플레이 화면 후보에서 입력 후 변화량이 무입력 변화량보다 충분히 크게 관찰되었다."
        )

    return GameplayFlowResult(
        resultState="INPUT_RESPONSE_NOT_CLEAR",
        inputChangeDelta=inputChangeDelta,
        reason="입력 후 변화량이 무입력 변화량보다 충분히 크지 않아 기본 플레이 흐름으로 판단하지 않는다."
    )
