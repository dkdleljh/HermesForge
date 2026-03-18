Set-StrictMode -Version Latest
$Root = Split-Path -Parent $PSScriptRoot
Set-Location "$Root/backend"
$env:PYTHONPATH='.'
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
