"""Evidence validation helpers."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceValidationResult:
    expectedFiles: list[str]
    existingFiles: list[str]
    missingFiles: list[str]
    isComplete: bool


def validateEvidenceFiles(runDir: str | Path, expectedFiles: list[str]) -> EvidenceValidationResult:
    directory = Path(runDir)
    existingFiles = [
        fileName
        for fileName in expectedFiles
        if (directory / fileName).exists() and (directory / fileName).stat().st_size > 0
    ]
    missingFiles = [fileName for fileName in expectedFiles if fileName not in existingFiles]

    return EvidenceValidationResult(
        expectedFiles=expectedFiles,
        existingFiles=existingFiles,
        missingFiles=missingFiles,
        isComplete=len(missingFiles) == 0
    )
