$ErrorActionPreference = "Stop"

$env:SHEEPY_RUN_STEAM_TESTS = "1"

if (-not (Test-Path ".\.venv\Scripts\python.exe")) {
    Write-Host "Virtual environment not found. Creating .venv..."
    & "C:\Users\dbtmd\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m venv .venv
}

Write-Host "Installing dependencies..."
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host "Running local Steam QA smoke tests..."
& ".\.venv\Scripts\python.exe" -m pytest tests/local/test_tc_001_004_local_steam.py tests/local/test_tc_005_screen_state.py
