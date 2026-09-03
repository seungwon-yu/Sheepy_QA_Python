from pathlib import Path

from PIL import Image, ImageDraw

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
