$ErrorActionPreference = "Stop"

$env:SHEEPY_RUN_STEAM_TESTS = "1"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Virtual environment not found. Run scripts\run_local_steam_tests.ps1 first."
    exit 1
}

& ".\.venv\Scripts\python.exe" -m pytest tests/local/test_tc_001_004_local_steam.py::test_tc_002_sheepy_appid_launch_command_is_called
