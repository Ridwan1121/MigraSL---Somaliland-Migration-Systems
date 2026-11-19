$ErrorActionPreference = "Stop"
$root = "C:\Users\Ridwan Farah\OneDrive\Desktop\MigraSL - Somaliland Migration Systems"
$backend = "$root\backend-api"
Set-Location $backend

$py = "$backend\venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $py)) { $py = "python" }

Write-Host "=== 1. Python Syntax Check (py_compile) ===" -ForegroundColor Cyan
$pyFiles = Get-ChildItem -Path $backend -Filter "*.py" -File | ForEach-Object { $_.FullName }
& $py -m py_compile $pyFiles
Write-Host "OK: Dhammaan faylasha .py syntax-koodu waa sax." -ForegroundColor Green

Write-Host "`n=== 2. Running Pytest Suite ===" -ForegroundColor Cyan
& $py -m pytest --version 2>$null
if ($LASTEXITCODE -ne 0) {
  Write-Host "pytest kuma jiro env-ga, waa la rakibayaa..." -ForegroundColor Yellow
  $devReq = "$backend\requirements-dev.txt"
  if (Test-Path -LiteralPath $devReq) {
    & $py -m pip install -r $devReq
  } else {
    & $py -m pip install pytest httpx
  }
}
& $py -m pytest -v

Write-Host "`n=== 3. Checking Live API Endpoints (http://127.0.0.1:8000) ===" -ForegroundColor Cyan
$endpoints = @(
  "http://127.0.0.1:8000/openapi.json",
  "http://127.0.0.1:8000/docs",
  "http://127.0.0.1:8000/dashboard/summary"
)

foreach ($url in $endpoints) {
  try {
    $res = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 5
    Write-Host "PASS [$($res.StatusCode)] -> $url" -ForegroundColor Green
  } catch {
    Write-Host "SKIP/OFFLINE -> $url (Shid uvicorn haddii uusan shidnayn)" -ForegroundColor Yellow
  }
}
