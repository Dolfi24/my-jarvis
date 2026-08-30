$ErrorActionPreference = "Stop"

if (-not (Test-Path .\.venv\Scripts\python.exe)) {
    throw "Jarvis is not set up yet. Run .\setup.ps1 first."
}

& .\.venv\Scripts\python.exe -m jarvis

