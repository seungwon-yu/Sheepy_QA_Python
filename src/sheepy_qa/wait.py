"""Bounded waiting utilities for local automation checks."""

import time
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def waitUntil(
    supplier: Callable[[], T],
    predicate: Callable[[T], bool],
    timeoutSeconds: float,
    intervalSeconds: float = 1.0
) -> tuple[bool, T]:
    deadline = time.monotonic() + timeoutSeconds
    lastValue = supplier()

    while time.monotonic() <= deadline:
        if predicate(lastValue):
            return True, lastValue

        time.sleep(intervalSeconds)
        lastValue = supplier()

    return predicate(lastValue), lastValue
