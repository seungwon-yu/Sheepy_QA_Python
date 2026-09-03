from pathlib import Path

import pytest
from PIL import Image

from sheepy_qa.image_diff import compareImages


def saveSolidImage(path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> Path:
    Image.new("RGB", size, color).save(path)
    return path


def test_compare_images_detects_visible_change(tmp_path: Path) -> None:
    beforeImagePath = saveSolidImage(tmp_path / "before.png", (20, 20), (0, 0, 0))
    afterImagePath = saveSolidImage(tmp_path / "after.png", (20, 20), (255, 255, 255))

    result = compareImages(beforeImagePath, afterImagePath, sampleStep=1)

    assert result.changedPixelRatio == 1
    assert result.averageChannelDifference == 255
    assert result.hasVisibleChange is True


def test_compare_images_detects_no_change(tmp_path: Path) -> None:
    beforeImagePath = saveSolidImage(tmp_path / "before.png", (20, 20), (10, 10, 10))
    afterImagePath = saveSolidImage(tmp_path / "after.png", (20, 20), (10, 10, 10))

    result = compareImages(beforeImagePath, afterImagePath, sampleStep=1)

    assert result.changedPixelRatio == 0
    assert result.averageChannelDifference == 0
    assert result.hasVisibleChange is False


def test_compare_images_rejects_different_sizes(tmp_path: Path) -> None:
    beforeImagePath = saveSolidImage(tmp_path / "before.png", (20, 20), (0, 0, 0))
    afterImagePath = saveSolidImage(tmp_path / "after.png", (10, 10), (0, 0, 0))

    with pytest.raises(ValueError):
        compareImages(beforeImagePath, afterImagePath)
