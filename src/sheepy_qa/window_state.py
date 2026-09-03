"""Window helpers for local input tests."""

import ctypes
from dataclasses import dataclass
from ctypes import wintypes

import psutil


SW_RESTORE = 9
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


@dataclass(frozen=True)
class WindowSnapshot:
    handle: int
    processId: int
    processName: str
    title: str
    left: int
    top: int
    right: int
    bottom: int
    width: int
    height: int
    isForeground: bool


def getForegroundWindowTitle() -> str:
    user32 = ctypes.windll.user32
    windowHandle = user32.GetForegroundWindow()
    titleLength = user32.GetWindowTextLengthW(windowHandle)
    buffer = ctypes.create_unicode_buffer(titleLength + 1)
    user32.GetWindowTextW(windowHandle, buffer, titleLength + 1)
    return buffer.value


def findWindowByTitleFragments(titleFragments: list[str]) -> WindowSnapshot | None:
    user32 = ctypes.windll.user32
    matchedHandles: list[int] = []
    loweredFragments = [fragment.lower() for fragment in titleFragments]

    def enumWindow(windowHandle: int, lparam: int) -> bool:
        if not user32.IsWindowVisible(windowHandle):
            return True

        titleLength = user32.GetWindowTextLengthW(windowHandle)

        if titleLength == 0:
            return True

        buffer = ctypes.create_unicode_buffer(titleLength + 1)
        user32.GetWindowTextW(windowHandle, buffer, titleLength + 1)
        title = buffer.value.lower()

        if all(fragment in title for fragment in loweredFragments):
            matchedHandles.append(windowHandle)
            return False

        return True

    enumWindowProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(enumWindow)
    user32.EnumWindows(enumWindowProc, 0)

    if not matchedHandles:
        return None

    return createWindowSnapshot(matchedHandles[0])


def findWindowByProcessNameFragments(processNameFragments: list[str]) -> WindowSnapshot | None:
    user32 = ctypes.windll.user32
    matchedHandles: list[int] = []
    loweredFragments = [fragment.lower() for fragment in processNameFragments]

    def enumWindow(windowHandle: int, lparam: int) -> bool:
        if not user32.IsWindowVisible(windowHandle):
            return True

        snapshot = createWindowSnapshot(windowHandle)

        if snapshot.width == 0 or snapshot.height == 0:
            return True

        processName = snapshot.processName.lower()

        if any(fragment in processName for fragment in loweredFragments):
            matchedHandles.append(windowHandle)
            return False

        return True

    enumWindowProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)(enumWindow)
    user32.EnumWindows(enumWindowProc, 0)

    if not matchedHandles:
        return None

    return createWindowSnapshot(matchedHandles[0])


def focusWindow(windowHandle: int) -> None:
    user32 = ctypes.windll.user32
    user32.ShowWindow(windowHandle, SW_RESTORE)
    user32.SetForegroundWindow(windowHandle)


def clickWindowTitleArea(window: WindowSnapshot) -> None:
    clickX = window.left + max(window.width // 2, 1)
    clickY = window.top + 10
    user32 = ctypes.windll.user32
    user32.SetCursorPos(clickX, clickY)
    user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def createWindowSnapshot(windowHandle: int) -> WindowSnapshot:
    user32 = ctypes.windll.user32
    rect = wintypes.RECT()
    user32.GetWindowRect(windowHandle, ctypes.byref(rect))
    foregroundHandle = user32.GetForegroundWindow()
    processId = wintypes.DWORD()
    user32.GetWindowThreadProcessId(windowHandle, ctypes.byref(processId))
    processName = getProcessName(processId.value)
    width = max(rect.right - rect.left, 0)
    height = max(rect.bottom - rect.top, 0)
    titleLength = user32.GetWindowTextLengthW(windowHandle)
    buffer = ctypes.create_unicode_buffer(titleLength + 1)
    user32.GetWindowTextW(windowHandle, buffer, titleLength + 1)

    return WindowSnapshot(
        handle=windowHandle,
        processId=processId.value,
        processName=processName,
        title=buffer.value,
        left=rect.left,
        top=rect.top,
        right=rect.right,
        bottom=rect.bottom,
        width=width,
        height=height,
        isForeground=windowHandle == foregroundHandle
    )


def getProcessName(processId: int) -> str:
    try:
        return psutil.Process(processId).name()
    except psutil.Error:
        return ""
