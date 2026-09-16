from PIL import Image, ImageDraw
from pathlib import Path
import pytest

from sheepy_qa.lobby_menu import analyzeLobbyMenu


def test_analyze_lobby_menu_detects_continue_and_start(tmp_path) -> None:
    imagePath = tmp_path / "lobby.png"
    image = Image.new("RGB", (1920, 1080), (5, 8, 12))
    draw = ImageDraw.Draw(image)
    draw.rectangle((230, 720, 360, 756), fill=(170, 170, 170))
    draw.rectangle((230, 782, 560, 810), fill=(45, 45, 45))
    image.save(imagePath)

    result = analyzeLobbyMenu(imagePath)

    assert result.screenState == "LOBBY_MENU_WITH_CONTINUE_AND_START"
    assert result.continueVisible is True
    assert result.startJourneyVisible is True
    assert result.playerStateHint == "PLAYER-RETURNING"


def test_analyze_lobby_menu_detects_start_only(tmp_path) -> None:
    imagePath = tmp_path / "lobby.png"
    image = Image.new("RGB", (1920, 1080), (5, 8, 12))
    draw = ImageDraw.Draw(image)
    draw.rectangle((230, 782, 560, 810), fill=(45, 45, 45))
    image.save(imagePath)

    result = analyzeLobbyMenu(imagePath)

    assert result.screenState == "LOBBY_MENU_WITH_START_ONLY"
    assert result.continueVisible is False
    assert result.startJourneyVisible is True
    assert result.playerStateHint == "PLAYER-NEW"


def test_analyze_lobby_menu_returns_review_when_no_cta_is_visible(tmp_path) -> None:
    imagePath = tmp_path / "empty.png"
    image = Image.new("RGB", (1920, 1080), (5, 8, 12))
    image.save(imagePath)

    result = analyzeLobbyMenu(imagePath)

    assert result.screenState == "REVIEW_REQUIRED"
    assert result.continueVisible is False
    assert result.startJourneyVisible is False


def test_real_dim_start_remains_visible():
    path = Path(__file__).resolve().parents[2] / "docs/samples/lobby-dim-start.png"
    result = analyzeLobbyMenu(path)
    assert result.continueVisible is True
    assert result.startJourneyVisible is True


@pytest.mark.parametrize("brightness", [30, 80, 200])
def test_uniform_bright_background_is_not_menu_text(tmp_path, brightness):
    path = tmp_path / "uniform.png"
    Image.new("RGB", (640, 360), (brightness,) * 3).save(path)
    result = analyzeLobbyMenu(path)
    assert result.screenState == "REVIEW_REQUIRED"


def test_smooth_bright_gradient_is_not_menu_text(tmp_path):
    image = Image.new("RGB", (640, 360))
    draw = ImageDraw.Draw(image)
    for x in range(640):
        brightness = int(255 * x / 639)
        draw.line((x, 0, x, 359), fill=(brightness,) * 3)
    path = tmp_path / "gradient.png"
    image.save(path)
    assert analyzeLobbyMenu(path).screenState == "REVIEW_REQUIRED"


def test_real_gameplay_is_not_lobby():
    path = Path(__file__).resolve().parents[2] / "docs/samples/gameplay-language-false-positive.png"
    assert analyzeLobbyMenu(path).screenState == "REVIEW_REQUIRED"
