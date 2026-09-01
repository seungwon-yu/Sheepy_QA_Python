"""Steam launch helpers for the target game."""

import os
import subprocess
from dataclasses import dataclass

from sheepy_qa.config import STEAM_RUN_URI


@dataclass(frozen=True)
class LaunchCommand:
    command: list[str]
    dryRun: bool


class SteamApp:
    def __init__(self, runUri: str = STEAM_RUN_URI) -> None:
        self.runUri = runUri

    def createLaunchCommand(self, dryRun: bool = False) -> LaunchCommand:
        if os.name == "nt":
            command = ["cmd", "/c", "start", "", self.runUri]
        else:
            command = ["xdg-open", self.runUri]

        return LaunchCommand(command=command, dryRun=dryRun)

    def launch(self, dryRun: bool = False) -> LaunchCommand:
        launchCommand = self.createLaunchCommand(dryRun=dryRun)

        if not dryRun:
            subprocess.Popen(launchCommand.command, shell=False)

        return launchCommand
