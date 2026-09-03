"""Image difference helpers for input response checks."""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass(frozen=True)
class ImageDiffResult:
    width: int
    height: int
    sampledPixelCount: int
    changedPixelRatio: float
    averageChannelDifference: float
    hasVisibleChange: bool


def compareImages(
    beforeImagePath: str | Path,
    afterImagePath: str | Path,
    changeThreshold: int = 18,
    minChangedPixelRatio: float = 0.01,
    sampleStep: int = 6
) -> ImageDiffResult:
    if sampleStep < 1:
        raise ValueError("sampleStep must be greater than 0.")

    with Image.open(beforeImagePath) as beforeImage, Image.open(afterImagePath) as afterImage:
        beforeRgb = beforeImage.convert("RGB")
        afterRgb = afterImage.convert("RGB")

        if beforeRgb.size != afterRgb.size:
            raise ValueError("Images must have the same size.")

        width, height = beforeRgb.size
        changedPixelCount = 0
        sampledPixelCount = 0
        channelDifferenceSum = 0

        for y in range(0, height, sampleStep):
            for x in range(0, width, sampleStep):
                beforeRed, beforeGreen, beforeBlue = beforeRgb.getpixel((x, y))
                afterRed, afterGreen, afterBlue = afterRgb.getpixel((x, y))
                channelDifference = (
                    abs(beforeRed - afterRed)
                    + abs(beforeGreen - afterGreen)
                    + abs(beforeBlue - afterBlue)
                ) / 3

                sampledPixelCount += 1
                channelDifferenceSum += channelDifference

                if channelDifference >= changeThreshold:
                    changedPixelCount += 1

    if sampledPixelCount == 0:
        raise ValueError("No pixels were sampled from the image.")

    changedPixelRatio = changedPixelCount / sampledPixelCount
    averageChannelDifference = channelDifferenceSum / sampledPixelCount

    return ImageDiffResult(
        width=width,
        height=height,
        sampledPixelCount=sampledPixelCount,
        changedPixelRatio=round(changedPixelRatio, 4),
        averageChannelDifference=round(averageChannelDifference, 2),
        hasVisibleChange=changedPixelRatio >= minChangedPixelRatio
    )
