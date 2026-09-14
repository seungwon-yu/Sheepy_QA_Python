from pathlib import Path

from PIL import Image, ImageDraw
import pytest

from sheepy_qa.language_screen import analyzeLanguageSelectionScreen


def test_analyze_language_selection_screen_detects_option_stack(tmp_path: Path) -> None:
    imagePath = tmp_path / "language-screen.png"
    image = Image.new("RGB", (192, 108), (0, 0, 0))
    draw = ImageDraw.Draw(image)

    for y in [22, 36, 51, 65, 79]:
        draw.rectangle((88, y, 104, y + 8), fill=(210, 30, 40))
        draw.rectangle((105, y, 121, y + 8), fill=(240, 240, 240))

    image.save(imagePath)

    result = analyzeLanguageSelectionScreen(imagePath, sampleStep=1)

    assert result.visibleOptionCount >= 2
    assert result.centralSaturatedPixelRatio >= 0.035
    assert result.isLanguageSelectionLike is True


def test_analyze_language_selection_screen_rejects_plain_black_image(tmp_path: Path) -> None:
    imagePath = tmp_path / "black.png"
    Image.new("RGB", (192, 108), (0, 0, 0)).save(imagePath)

    result = analyzeLanguageSelectionScreen(imagePath, sampleStep=1)

    assert result.visibleOptionCount == 0
    assert result.isLanguageSelectionLike is False


@pytest.mark.parametrize("size", [(192, 108), (640, 360), (1280, 720)])
@pytest.mark.parametrize("sideColor,expected", [("black", True), ((50, 70, 130), False)])
def test_option_colors_require_dark_surroundings(tmp_path, size, sideColor, expected):
    image = Image.new("RGB", size, sideColor)
    draw = ImageDraw.Draw(image)
    width, height = size
    draw.rectangle((int(width * 0.4), 0, int(width * 0.65), height), fill="black")
    for y in (0.20, 0.34, 0.48, 0.62, 0.76):
        draw.rectangle((int(width * 0.46), int(height * y),
                        int(width * 0.54), int(height * (y + 0.08))), fill=(210, 30, 40))
    path = tmp_path / "options.png"
    image.save(path)

    result = analyzeLanguageSelectionScreen(path)

    assert result.visibleOptionCount >= 2
    assert result.isLanguageSelectionLike is expected
    assert result.sideDarkPixelRatio == (1.0 if expected else 0.0)
