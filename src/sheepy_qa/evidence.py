"""Evidence file helpers for test execution results."""

import json
from dataclasses import asdict, is_dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class EvidenceWriter:
    def __init__(self, baseDir: str | Path = "artifacts/evidence") -> None:
        self.baseDir = Path(baseDir)

    def createRunDir(self, testId: str) -> Path:
        timestamp = datetime.now(UTC).isoformat(timespec="milliseconds").replace(":", "-")
        safeTestId = sanitizeFileName(testId)
        runDir = self.baseDir / f"{timestamp}-{safeTestId}"
        runDir.mkdir(parents=True, exist_ok=False)
        return runDir

    def writeJson(self, runDir: str | Path, fileName: str, value: Any) -> Path:
        filePath = Path(runDir) / fileName
        filePath.write_text(f"{json.dumps(toJsonValue(value), ensure_ascii=False, indent=2)}\n", encoding="utf-8")
        return filePath


def sanitizeFileName(value: str) -> str:
    safeValue = "".join(character if character.isalnum() or character in ("-", "_") else "_" for character in value)
    return safeValue.strip("_") or "test"


def toJsonValue(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)

    if isinstance(value, Path):
        return str(value)

    if isinstance(value, list):
        return [toJsonValue(item) for item in value]

    if isinstance(value, dict):
        return {key: toJsonValue(nextValue) for key, nextValue in value.items()}

    return value
