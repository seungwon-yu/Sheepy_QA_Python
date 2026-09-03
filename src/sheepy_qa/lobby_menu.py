"""Lobby menu analysis helpers."""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass(frozen=True)
class MenuOptionSignal:
    name: str
    region: tuple[float, float, float, float]
    averageBrightness: float
    topBrightness: float
    textPixelRatio: float
    isVisible: bool


@dataclass(frozen=True)
class LobbyMenuAnalysisResult:
    screenState: str
    continueVisible: bool
    startJourneyVisible: bool
    playerStateHint: str
    optionSignals: list[MenuOptionSignal]
    reason: str


def analyzeLobbyMenu(imagePath: str | Path) -> LobbyMenuAnalysisResult:
    filePath = Path(imagePath)

    with Image.open(filePath) as image:
        rgbImage = image.convert("RGB")
        optionSignals = [
            analyzeMenuOption(rgbImage, "Continue", (0.12, 0.66, 0.19, 0.70), textThreshold=45),
            analyzeMenuOption(rgbImage, "Start Your Journey", (0.12, 0.72, 0.29, 0.76), textThreshold=25)
        ]

    continueSignal = optionSignals[0]
    startJourneySignal = optionSignals[1]

    if continueSignal.isVisible and startJourneySignal.isVisible:
        return LobbyMenuAnalysisResult(
            screenState="LOBBY_MENU_WITH_CONTINUE_AND_START",
            continueVisible=True,
            startJourneyVisible=True,
            playerStateHint="PLAYER-RETURNING",
            optionSignals=optionSignals,
            reason="Continue와 Start Your Journey 후보 영역에서 메뉴 텍스트 신호가 모두 관찰되었다."
        )

    if startJourneySignal.isVisible:
        return LobbyMenuAnalysisResult(
            screenState="LOBBY_MENU_WITH_START_ONLY",
            continueVisible=False,
            startJourneyVisible=True,
            playerStateHint="PLAYER-NEW",
            optionSignals=optionSignals,
            reason="Start Your Journey 후보 영역에서 메뉴 텍스트 신호가 관찰되었다."
        )

    if continueSignal.isVisible:
        return LobbyMenuAnalysisResult(
            screenState="LOBBY_MENU_WITH_CONTINUE_ONLY",
            continueVisible=True,
            startJourneyVisible=False,
            playerStateHint="PLAYER-RETURNING",
            optionSignals=optionSignals,
            reason="Continue 후보 영역에서 메뉴 텍스트 신호가 관찰되었다."
        )

    return LobbyMenuAnalysisResult(
        screenState="REVIEW_REQUIRED",
        continueVisible=False,
        startJourneyVisible=False,
        playerStateHint="PLAYER-UNKNOWN",
        optionSignals=optionSignals,
        reason="로비 CTA 후보 영역에서 충분한 메뉴 텍스트 신호를 찾지 못했다."
    )


def analyzeMenuOption(
    image: Image.Image,
    name: str,
    region: tuple[float, float, float, float],
    textThreshold: int
) -> MenuOptionSignal:
    width, height = image.size
    leftRatio, topRatio, rightRatio, bottomRatio = region
    left = int(width * leftRatio)
    top = int(height * topRatio)
    right = int(width * rightRatio)
    bottom = int(height * bottomRatio)
    brightnessValues: list[float] = []

    for y in range(top, bottom, 2):
        for x in range(left, right, 2):
            red, green, blue = image.getpixel((x, y))
            brightnessValues.append((red + green + blue) / 3)

    if not brightnessValues:
        raise ValueError("No pixels were sampled from the menu option region.")

    sortedBrightness = sorted(brightnessValues)
    topBrightness = sortedBrightness[int(len(sortedBrightness) * 0.95)]
    textPixelRatio = sum(value >= textThreshold for value in brightnessValues) / len(brightnessValues)
    isVisible = topBrightness >= textThreshold and textPixelRatio >= 0.08

    return MenuOptionSignal(
        name=name,
        region=region,
        averageBrightness=round(sum(brightnessValues) / len(brightnessValues), 2),
        topBrightness=round(topBrightness, 2),
        textPixelRatio=round(textPixelRatio, 4),
        isVisible=isVisible
    )
