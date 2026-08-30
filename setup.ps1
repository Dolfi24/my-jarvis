$ErrorActionPreference = "Stop"

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python launcher not found. Install Python 3.11 or newer from python.org and enable 'Add Python to PATH'."
}

py -3 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt

if (-not (Test-Path .env.local)) {
    Copy-Item .env.example .env.local
    Write-Host "Created .env.local. Add your OPENAI_API_KEY before running Jarvis."
}

Write-Host "Setup complete. Run .\run.ps1"
