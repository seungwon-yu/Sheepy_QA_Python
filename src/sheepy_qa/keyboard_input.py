"""Keyboard input helpers for local game tests."""

import ctypes
import time


KEYEVENTF_KEYUP = 0x0002
VK_RETURN = 0x0D


def pressEnter(holdSeconds: float = 0.05) -> None:
    sendVirtualKey(VK_RETURN, isKeyUp=False)
    time.sleep(holdSeconds)
    sendVirtualKey(VK_RETURN, isKeyUp=True)


def sendVirtualKey(virtualKey: int, isKeyUp: bool) -> None:
    flags = KEYEVENTF_KEYUP if isKeyUp else 0
    ctypes.windll.user32.keybd_event(virtualKey, 0, flags, 0)
