$ErrorActionPreference = "Stop"

$env:SHEEPY_RUN_STEAM_TESTS = "1"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Virtual environment not found. Run scripts\run_local_steam_tests.ps1 first."
    exit 1
}

& ".\.venv\Scripts\python.exe" -m pytest tests/local/test_tc_009_017_language_selection.py::test_tc_017_language_selection_enter_input_changes_screen
