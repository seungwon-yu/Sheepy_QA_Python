"""Language selection screen analysis helpers."""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass(frozen=True)
class LanguageScreenAnalysisResult:
    width: int
    height: int
    sampledPixelCount: int
    visibleOptionCount: int
    centralDarkPixelRatio: float
    centralSaturatedPixelRatio: float
    isLanguageSelectionLike: bool


def analyzeLanguageSelectionScreen(imagePath: str | Path, sampleStep: int = 4) -> LanguageScreenAnalysisResult:
    if sampleStep < 1:
        raise ValueError("sampleStep must be greater than 0.")

    filePath = Path(imagePath)

    with Image.open(filePath) as image:
        rgbImage = image.convert("RGB")
        width, height = rgbImage.size
        xStart = int(width * 0.42)
        xEnd = int(width * 0.62)
        yStart = int(height * 0.15)
        yEnd = int(height * 0.88)
        slotCount = 5
        slotHeight = max((yEnd - yStart) // slotCount, 1)
        saturatedCounts = [0 for _ in range(slotCount)]
        sampledCounts = [0 for _ in range(slotCount)]
        darkPixelCount = 0
        saturatedPixelCount = 0
        sampledPixelCount = 0

        for y in range(yStart, yEnd, sampleStep):
            slotIndex = min((y - yStart) // slotHeight, slotCount - 1)

            for x in range(xStart, xEnd, sampleStep):
                red, green, blue = rgbImage.getpixel((x, y))
                brightness = round((red + green + blue) / 3)
                saturation = max(red, green, blue) - min(red, green, blue)
                isDark = brightness <= 35
                isSaturated = brightness >= 45 and saturation >= 35

                sampledPixelCount += 1
                sampledCounts[slotIndex] += 1

                if isDark:
                    darkPixelCount += 1

                if isSaturated:
                    saturatedPixelCount += 1
                    saturatedCounts[slotIndex] += 1

    if sampledPixelCount == 0:
        raise ValueError("No pixels were sampled from the image.")

    visibleOptionCount = sum(
        1
        for index, count in enumerate(saturatedCounts)
        if sampledCounts[index] > 0 and count / sampledCounts[index] >= 0.015
    )
    centralDarkPixelRatio = darkPixelCount / sampledPixelCount
    centralSaturatedPixelRatio = saturatedPixelCount / sampledPixelCount
    hasVisibleLanguageOptions = visibleOptionCount >= 2
    hasColorBlocksOnDarkBackground = centralSaturatedPixelRatio >= 0.035 and centralDarkPixelRatio >= 0.5
    isLanguageSelectionLike = hasVisibleLanguageOptions and hasColorBlocksOnDarkBackground

    return LanguageScreenAnalysisResult(
        width=width,
        height=height,
        sampledPixelCount=sampledPixelCount,
        visibleOptionCount=visibleOptionCount,
        centralDarkPixelRatio=round(centralDarkPixelRatio, 4),
        centralSaturatedPixelRatio=round(centralSaturatedPixelRatio, 4),
        isLanguageSelectionLike=isLanguageSelectionLike
    )
