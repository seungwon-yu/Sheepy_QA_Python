from pathlib import Path

import pytest
from PIL import Image

from sheepy_qa.image_analysis import analyzeImage, classifyScreenState


def saveImage(path: Path, color: tuple[int, int, int]) -> Path:
    image = Image.new("RGB", (16, 16), color)
    image.save(path)
    return path


def test_analyze_image_detects_black_screen(tmp_path: Path) -> None:
    imagePath = saveImage(tmp_path / "black.png", (0, 0, 0))

    result = analyzeImage(imagePath)

    assert result.width == 16
    assert result.height == 16
    assert result.averageBrightness == 0
    assert result.darkPixelRatio == 1
    assert result.isMostlyBlack is True
    assert classifyScreenState(result) == "BLACK_SCREEN"


def test_analyze_image_detects_visible_screen(tmp_path: Path) -> None:
    imagePath = saveImage(tmp_path / "visible.png", (120, 80, 40))

    result = analyzeImage(imagePath)

    assert result.averageBrightness > 12
    assert result.isMostlyBlack is False
    assert classifyScreenState(result) == "VISIBLE_SCREEN"


def test_analyze_image_detects_dark_screen_with_visible_ui(tmp_path: Path) -> None:
    imagePath = tmp_path / "dark-visible.png"
    image = Image.new("RGB", (64, 64), (0, 0, 0))

    for x in range(24, 40):
        for y in range(24, 40):
            image.putpixel((x, y), (255, 0, 0))

    image.save(imagePath)

    result = analyzeImage(imagePath, sampleStep=1)

    assert result.averageBrightness < 12
    assert result.isMostlyBlack is False
    assert classifyScreenState(result) == "VISIBLE_SCREEN"


def test_analyze_image_rejects_invalid_sample_step(tmp_path: Path) -> None:
    imagePath = saveImage(tmp_path / "sample.png", (255, 255, 255))

    with pytest.raises(ValueError):
        analyzeImage(imagePath, sampleStep=0)
