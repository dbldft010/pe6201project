$ErrorActionPreference = 'Stop'
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectDir
if (-not (Test-Path '.venv\Scripts\python.exe')) {
    throw 'Virtual environment not found. Create it with: python -m venv .venv; .\.venv\Scripts\python.exe -m pip install -r requirements.txt'
}
& '.\.venv\Scripts\python.exe' app.py
