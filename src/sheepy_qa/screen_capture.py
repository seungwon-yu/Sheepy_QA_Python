"""Screen capture helpers."""

from pathlib import Path

from PIL import ImageGrab


def captureScreenshot(outputPath: str | Path) -> Path:
    filePath = Path(outputPath)
    filePath.parent.mkdir(parents=True, exist_ok=True)
    screenshot = ImageGrab.grab()
    screenshot.save(filePath)
    return filePath
