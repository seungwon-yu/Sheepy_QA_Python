from types import SimpleNamespace
import pytest
from PIL import Image
from sheepy_qa import screen_capture


def test_window_capture_uses_client_area_not_outer_frame(monkeypatch, tmp_path):
    window = SimpleNamespace(left=0, top=0, right=656, bottom=399)
    monkeypatch.setattr(screen_capture, "getClientBounds", lambda actual: (8, 31, 648, 391))
    seen = []
    def grab(*, bbox):
        seen.append(bbox)
        return Image.new("RGB", (640, 360), "black")
    monkeypatch.setattr(screen_capture.ImageGrab, "grab", grab)
    path = screen_capture.captureWindowScreenshot(window, tmp_path / "game.png")
    assert seen == [(8, 31, 648, 391)]
    from sheepy_qa.image_analysis import analyzeImage
    assert analyzeImage(path).isMostlyBlack


def test_invalid_client_area_does_not_fall_back_to_desktop(monkeypatch, tmp_path):
    def fail(window):
        raise OSError("invalid window")
    monkeypatch.setattr(screen_capture, "getClientBounds", fail)
    monkeypatch.setattr(screen_capture.ImageGrab, "grab", lambda **kwargs: pytest.fail("capture must stop"))
    with pytest.raises(OSError):
        screen_capture.captureWindowScreenshot(None, tmp_path / "game.png")
