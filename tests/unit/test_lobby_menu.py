from PIL import Image, ImageDraw

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
