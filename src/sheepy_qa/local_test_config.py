"""Runtime flags for local-only QA tests."""

import os


def shouldRunSteamTests() -> bool:
    return os.environ.get("SHEEPY_RUN_STEAM_TESTS") == "1"
