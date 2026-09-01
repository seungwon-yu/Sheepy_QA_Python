"""Local Steam environment checks."""

from dataclasses import dataclass
from pathlib import Path

from sheepy_qa.process_check import findProcessesByName, hasRunningProcess


@dataclass(frozen=True)
class SteamEnvironmentSnapshot:
    steamProcessFound: bool
    steamExecutableFound: bool
    steamExecutableCandidates: list[str]
    steamProcesses: list[dict[str, object]]


def getDefaultSteamPaths() -> list[Path]:
    return [
        Path("C:/Program Files (x86)/Steam/steam.exe"),
        Path("C:/Program Files/Steam/steam.exe")
    ]


def createSteamEnvironmentSnapshot() -> SteamEnvironmentSnapshot:
    steamProcesses = findProcessesByName(["steam.exe", "steamwebhelper.exe"])
    steamPaths = [path for path in getDefaultSteamPaths() if path.exists()]

    return SteamEnvironmentSnapshot(
        steamProcessFound=hasRunningProcess(steamProcesses),
        steamExecutableFound=len(steamPaths) > 0,
        steamExecutableCandidates=[str(path) for path in steamPaths],
        steamProcesses=[
            {
                "name": process.name,
                "pid": process.pid,
                "status": process.status
            }
            for process in steamProcesses
        ]
    )


def isSteamAvailable(snapshot: SteamEnvironmentSnapshot) -> bool:
    return snapshot.steamProcessFound or snapshot.steamExecutableFound
