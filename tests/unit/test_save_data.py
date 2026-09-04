from sheepy_qa.save_data import SaveDataSnapshot, SaveFileSnapshot, compareSaveSnapshots, createSaveDataSnapshot


def test_create_save_data_snapshot_finds_sheepy_named_files(tmp_path) -> None:
    saveDir = tmp_path / "Sheepy" / "profile"
    saveDir.mkdir(parents=True)
    saveFile = saveDir / "save.dat"
    saveFile.write_text("save", encoding="utf-8")

    snapshot = createSaveDataSnapshot(roots=[tmp_path])

    assert len(snapshot.files) == 1
    assert snapshot.files[0].path == str(saveFile)


def test_compare_save_snapshots_reports_preserved_files() -> None:
    before = SaveDataSnapshot(
        searchedRoots=["root"],
        files=[SaveFileSnapshot(path="root/Sheepy/save.dat", size=10, modifiedTime=1.0)]
    )
    after = SaveDataSnapshot(
        searchedRoots=["root"],
        files=[SaveFileSnapshot(path="root/Sheepy/save.dat", size=10, modifiedTime=1.0)]
    )

    result = compareSaveSnapshots(before, after)

    assert result.resultState == "SAVE_DATA_PRESERVED"
    assert result.missingFiles == []


def test_compare_save_snapshots_requires_existing_save_files() -> None:
    result = compareSaveSnapshots(
        SaveDataSnapshot(searchedRoots=["root"], files=[]),
        SaveDataSnapshot(searchedRoots=["root"], files=[])
    )

    assert result.resultState == "REVIEW_REQUIRED"


def test_compare_save_snapshots_reports_missing_files() -> None:
    before = SaveDataSnapshot(
        searchedRoots=["root"],
        files=[SaveFileSnapshot(path="root/Sheepy/save.dat", size=10, modifiedTime=1.0)]
    )
    after = SaveDataSnapshot(searchedRoots=["root"], files=[])

    result = compareSaveSnapshots(before, after)

    assert result.resultState == "SAVE_DATA_MISSING"
    assert result.missingFiles == ["root/Sheepy/save.dat"]
