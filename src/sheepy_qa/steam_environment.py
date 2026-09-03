"""Local Steam environment checks."""

from dataclasses import dataclass
from pathlib import Path

import psutil

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
    steamProcesses = findProcessesByName(["steam", "steam.exe", "steamwebhelper", "steamwebhelper.exe"])
    steamPaths = [path for path in getDefaultSteamPaths() if path.exists()]
    processPaths = getSteamProcessPaths()
    allSteamPaths = list(dict.fromkeys([str(path) for path in steamPaths] + processPaths))

    return SteamEnvironmentSnapshot(
        steamProcessFound=hasRunningProcess(steamProcesses),
        steamExecutableFound=len(allSteamPaths) > 0,
        steamExecutableCandidates=allSteamPaths,
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


def getSteamProcessPaths() -> list[str]:
    paths: list[str] = []

    for process in psutil.process_iter(["name", "exe"]):
        info = process.info
        processName = (info.get("name") or "").lower()

        if "steam" not in processName:
            continue

        processPath = info.get("exe")

        if processPath:
            paths.append(str(processPath))

    return list(dict.fromkeys(paths))
