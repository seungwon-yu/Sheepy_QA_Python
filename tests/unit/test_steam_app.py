from sheepy_qa.config import SHEEPY_APP_ID, STEAM_RUN_URI
from sheepy_qa.steam_app import SteamApp


def test_steam_run_uri_uses_sheepy_app_id() -> None:
    assert SHEEPY_APP_ID == "1568400"
    assert STEAM_RUN_URI == "steam://run/1568400"


def test_create_launch_command_supports_dry_run() -> None:
    app = SteamApp()
    command = app.createLaunchCommand(dryRun=True)

    assert command.dryRun is True
    assert "steam://run/1568400" in command.command
