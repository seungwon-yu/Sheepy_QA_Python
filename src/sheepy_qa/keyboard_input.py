"""Keyboard input helpers for local game tests."""

import ctypes
import time


KEYEVENTF_KEYUP = 0x0002
VK_SPACE = 0x20
VK_RETURN = 0x0D
VK_LEFT = 0x25
VK_RIGHT = 0x27


def pressEnter(holdSeconds: float = 0.05) -> None:
    pressKey(VK_RETURN, holdSeconds=holdSeconds)


def pressSpace(holdSeconds: float = 0.05) -> None:
    pressKey(VK_SPACE, holdSeconds=holdSeconds)


def pressLeft(holdSeconds: float = 0.15) -> None:
    pressKey(VK_LEFT, holdSeconds=holdSeconds)


def pressRight(holdSeconds: float = 0.15) -> None:
    pressKey(VK_RIGHT, holdSeconds=holdSeconds)


def pressKey(virtualKey: int, holdSeconds: float = 0.05) -> None:
    sendVirtualKey(virtualKey, isKeyUp=False)
    time.sleep(holdSeconds)
    sendVirtualKey(virtualKey, isKeyUp=True)


def sendVirtualKey(virtualKey: int, isKeyUp: bool) -> None:
    flags = KEYEVENTF_KEYUP if isKeyUp else 0
    ctypes.windll.user32.keybd_event(virtualKey, 0, flags, 0)
