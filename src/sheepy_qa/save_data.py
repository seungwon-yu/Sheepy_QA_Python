"""Non-destructive save data inspection helpers."""

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class SaveFileSnapshot:
    path: str
    size: int
    modifiedTime: float


@dataclass(frozen=True)
class SaveDataSnapshot:
    searchedRoots: list[str]
    files: list[SaveFileSnapshot]


@dataclass(frozen=True)
class SavePreservationResult:
    resultState: str
    beforeFileCount: int
    afterFileCount: int
    missingFiles: list[str]
    addedFiles: list[str]
    changedFiles: list[str]
    reason: str


def createSaveDataSnapshot(roots: list[str | Path] | None = None) -> SaveDataSnapshot:
    searchRoots = [Path(root) for root in (roots or getDefaultSaveSearchRoots())]
    existingRoots = [root for root in searchRoots if root.exists()]
    files: list[SaveFileSnapshot] = []

    for root in existingRoots:
        for filePath in findSheepyLikeFiles(root):
            try:
                stat = filePath.stat()
            except OSError:
                continue

            files.append(
                SaveFileSnapshot(
                    path=str(filePath),
                    size=stat.st_size,
                    modifiedTime=stat.st_mtime
                )
            )

    files.sort(key=lambda item: item.path.lower())

    return SaveDataSnapshot(
        searchedRoots=[str(root) for root in searchRoots],
        files=files
    )


def compareSaveSnapshots(before: SaveDataSnapshot, after: SaveDataSnapshot) -> SavePreservationResult:
    beforeByPath = {file.path: file for file in before.files}
    afterByPath = {file.path: file for file in after.files}
    missingFiles = sorted(path for path in beforeByPath if path not in afterByPath)
    addedFiles = sorted(path for path in afterByPath if path not in beforeByPath)
    changedFiles = sorted(
        path
        for path, beforeFile in beforeByPath.items()
        if path in afterByPath and (
            beforeFile.size != afterByPath[path].size
            or beforeFile.modifiedTime != afterByPath[path].modifiedTime
        )
    )

    if len(before.files) == 0:
        return SavePreservationResult(
            resultState="REVIEW_REQUIRED",
            beforeFileCount=0,
            afterFileCount=len(after.files),
            missingFiles=missingFiles,
            addedFiles=addedFiles,
            changedFiles=changedFiles,
            reason="관찰 가능한 Sheepy 관련 저장 파일을 찾지 못해 저장 상태 보존 여부를 판단하지 않는다."
        )

    if missingFiles:
        return SavePreservationResult(
            resultState="SAVE_DATA_MISSING",
            beforeFileCount=len(before.files),
            afterFileCount=len(after.files),
            missingFiles=missingFiles,
            addedFiles=addedFiles,
            changedFiles=changedFiles,
            reason="관찰 전 존재하던 저장 파일이 관찰 후 누락되었다."
        )

    return SavePreservationResult(
        resultState="SAVE_DATA_PRESERVED",
        beforeFileCount=len(before.files),
        afterFileCount=len(after.files),
        missingFiles=missingFiles,
        addedFiles=addedFiles,
        changedFiles=changedFiles,
        reason="관찰 전 존재하던 저장 파일 경로가 관찰 후에도 유지되었다."
    )


def getDefaultSaveSearchRoots() -> list[Path]:
    roots = []
    localAppData = os.environ.get("LOCALAPPDATA")
    roamingAppData = os.environ.get("APPDATA")

    if localAppData:
        roots.extend([
            Path(localAppData) / "SheepyAShortAdventure",
            Path(localAppData) / "Sheepy"
        ])

    if roamingAppData:
        roots.extend([
            Path(roamingAppData) / "SheepyAShortAdventure",
            Path(roamingAppData) / "Sheepy"
        ])

    return roots


def findSheepyLikeFiles(root: Path, maxDepth: int = 5) -> list[Path]:
    matchedFiles: list[Path] = []
    rootDepth = len(root.parts)

    try:
        candidates = root.rglob("*")
    except OSError:
        return matchedFiles

    for candidate in candidates:
        if len(candidate.parts) - rootDepth > maxDepth:
            continue

        loweredPath = str(candidate).lower()

        if "sheepy" not in loweredPath:
            continue

        if candidate.is_file():
            matchedFiles.append(candidate)

    return matchedFiles
