from sheepy_qa.steam_environment import SteamEnvironmentSnapshot, isSteamAvailable


def test_protocol_registration_is_an_environment_signal():
    snapshot = SteamEnvironmentSnapshot(False, False, [], [], True, "custom steam launcher")
    assert isSteamAvailable(snapshot)


def test_no_environment_signal_is_not_available():
    assert not isSteamAvailable(SteamEnvironmentSnapshot(False, False, [], []))


def test_is_steam_available_returns_true_when_process_exists() -> None:
    snapshot = SteamEnvironmentSnapshot(
        steamProcessFound=True,
        steamExecutableFound=False,
        steamExecutableCandidates=[],
        steamProcesses=[
            {
                "name": "steam.exe",
                "pid": 1234,
                "status": "running"
            }
        ]
    )

    assert isSteamAvailable(snapshot) is True


def test_is_steam_available_returns_true_when_executable_exists() -> None:
    snapshot = SteamEnvironmentSnapshot(
        steamProcessFound=False,
        steamExecutableFound=True,
        steamExecutableCandidates=["C:/Program Files (x86)/Steam/steam.exe"],
        steamProcesses=[]
    )

    assert isSteamAvailable(snapshot) is True


def test_is_steam_available_returns_false_without_process_or_executable() -> None:
    snapshot = SteamEnvironmentSnapshot(
        steamProcessFound=False,
        steamExecutableFound=False,
        steamExecutableCandidates=[],
        steamProcesses=[]
    )

    assert isSteamAvailable(snapshot) is False
