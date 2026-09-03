"""Screen capture helpers."""

from pathlib import Path

from PIL import ImageGrab

from sheepy_qa.window_state import WindowSnapshot


def captureScreenshot(outputPath: str | Path) -> Path:
    filePath = Path(outputPath)
    filePath.parent.mkdir(parents=True, exist_ok=True)
    screenshot = ImageGrab.grab()
    screenshot.save(filePath)
    return filePath


def captureWindowScreenshot(window: WindowSnapshot, outputPath: str | Path) -> Path:
    filePath = Path(outputPath)
    filePath.parent.mkdir(parents=True, exist_ok=True)
    screenshot = ImageGrab.grab(bbox=(window.left, window.top, window.right, window.bottom))
    screenshot.save(filePath)
    return filePath
