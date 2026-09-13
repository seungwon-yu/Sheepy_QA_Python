"""Local Steam environment checks."""

from dataclasses import dataclass
from pathlib import Path
import sys

import psutil

from sheepy_qa.process_check import findProcessesByName, hasRunningProcess


@dataclass(frozen=True)
class SteamEnvironmentSnapshot:
    steamProcessFound: bool
    steamExecutableFound: bool
    steamExecutableCandidates: list[str]
    steamProcesses: list[dict[str, object]]
    steamProtocolRegistered: bool = False
    steamProtocolCommand: str | None = None


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
    protocolCommand = getSteamProtocolCommand()

    return SteamEnvironmentSnapshot(
        steamProcessFound=hasRunningProcess(steamProcesses),
        steamExecutableFound=len(allSteamPaths) > 0,
        steamExecutableCandidates=allSteamPaths,
        steamProtocolRegistered=protocolCommand is not None,
        steamProtocolCommand=protocolCommand,
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
    return snapshot.steamProcessFound or snapshot.steamExecutableFound or snapshot.steamProtocolRegistered


def getSteamProtocolCommand() -> str | None:
    """기본 설치 경로 밖의 Steam 등록 신호. 명령을 실행하지 않는다."""
    if sys.platform != "win32":
        return None
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "steam") as key:
            winreg.QueryValueEx(key, "URL Protocol")
        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, r"steam\shell\open\command") as key:
            command, _ = winreg.QueryValueEx(key, "")
        return command if isinstance(command, str) and command.strip() else None
    except OSError:
        return None


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
