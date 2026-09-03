"""Image analysis helpers for screen state checks."""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass(frozen=True)
class ImageAnalysisResult:
    width: int
    height: int
    sampledPixelCount: int
    averageBrightness: float
    darkPixelRatio: float
    uniqueSampledColorCount: int
    isMostlyBlack: bool


def analyzeImage(
    imagePath: str | Path,
    blackBrightnessThreshold: int = 12,
    darkPixelThreshold: int = 25,
    maxDarkPixelRatio: float = 0.98,
    sampleStep: int = 8
) -> ImageAnalysisResult:
    if sampleStep < 1:
        raise ValueError("sampleStep must be greater than 0.")

    filePath = Path(imagePath)

    with Image.open(filePath) as image:
        rgbImage = image.convert("RGB")
        width, height = rgbImage.size
        brightnessValues: list[int] = []
        sampledColors: set[tuple[int, int, int]] = set()

        for y in range(0, height, sampleStep):
            for x in range(0, width, sampleStep):
                red, green, blue = rgbImage.getpixel((x, y))
                brightness = round((red + green + blue) / 3)
                brightnessValues.append(brightness)
                sampledColors.add((red, green, blue))

    if not brightnessValues:
        raise ValueError("No pixels were sampled from the image.")

    sampledPixelCount = len(brightnessValues)
    averageBrightness = sum(brightnessValues) / sampledPixelCount
    darkPixelCount = sum(1 for brightness in brightnessValues if brightness <= darkPixelThreshold)
    darkPixelRatio = darkPixelCount / sampledPixelCount
    isMostlyBlack = averageBrightness <= blackBrightnessThreshold and darkPixelRatio >= maxDarkPixelRatio

    return ImageAnalysisResult(
        width=width,
        height=height,
        sampledPixelCount=sampledPixelCount,
        averageBrightness=round(averageBrightness, 2),
        darkPixelRatio=round(darkPixelRatio, 4),
        uniqueSampledColorCount=len(sampledColors),
        isMostlyBlack=isMostlyBlack
    )


def classifyScreenState(result: ImageAnalysisResult) -> str:
    if result.isMostlyBlack:
        return "BLACK_SCREEN"

    if result.averageBrightness > 12 or result.uniqueSampledColorCount > 1:
        return "VISIBLE_SCREEN"

    return "REVIEW_REQUIRED"
