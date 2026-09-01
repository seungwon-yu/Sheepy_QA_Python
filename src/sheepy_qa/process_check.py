"""Process observation utilities for black-box game QA."""

from dataclasses import dataclass
from typing import Iterable

import psutil


@dataclass(frozen=True)
class ProcessSnapshot:
    name: str
    pid: int
    status: str | None


def findProcessesByName(nameFragments: Iterable[str]) -> list[ProcessSnapshot]:
    fragments = [fragment.lower() for fragment in nameFragments]
    snapshots: list[ProcessSnapshot] = []

    for process in psutil.process_iter(["name", "pid", "status"]):
        info = process.info
        processName = info.get("name") or ""

        if any(fragment in processName.lower() for fragment in fragments):
            snapshots.append(
                ProcessSnapshot(
                    name=processName,
                    pid=int(info.get("pid") or 0),
                    status=info.get("status")
                )
            )

    return snapshots


def hasRunningProcess(processes: Iterable[ProcessSnapshot]) -> bool:
    return any(process.pid > 0 for process in processes)
