Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
python -m venv "$Root/.venv"
& "$Root/.venv/Scripts/Activate.ps1"
pip install -r "$Root/backend/requirements.txt"
Set-Location "$Root/frontend"
npm install
