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
    screenshot = ImageGrab.grab(bbox=getClientBounds(window))
    screenshot.save(filePath)
    return filePath


def getClientBounds(window: WindowSnapshot) -> tuple[int, int, int, int]:
    """Sheepy NW.js의 실제 렌더링 자식 창만 캡처한다."""
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    bounds = []
    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def inspect(handle, parameter):
        name = ctypes.create_unicode_buffer(256)
        user32.GetClassNameW(handle, name, len(name))
        if name.value == "Chrome_RenderWidgetHostHWND" and user32.IsWindowVisible(handle):
            rect = wintypes.RECT()
            if user32.GetWindowRect(handle, ctypes.byref(rect)):
                bounds.append((rect.left, rect.top, rect.right, rect.bottom))
        return True
    user32.EnumChildWindows(wintypes.HWND(window.handle), inspect, 0)
    if len(bounds) != 1:
        raise OSError("Expected one visible Sheepy rendering window")
    left, top, right, bottom = bounds[0]
    if not (window.left <= left < right <= window.right and window.top <= top < bottom <= window.bottom):
        raise ValueError("Rendering area is outside the game window")
    return left, top, right, bottom
