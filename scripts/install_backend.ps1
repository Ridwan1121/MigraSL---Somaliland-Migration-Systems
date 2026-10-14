$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

$python = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $python) {
    throw "Python is not installed or not available on PATH."
}

$version = & python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
Write-Host "Python version: $version"

$versionParts = $version.Split('.')
$major = [int]$versionParts[0]
$minor = [int]$versionParts[1]

if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 12)) {
    throw "This project requires Python 3.12 or newer."
}

Write-Host "Installing project dependencies..."
& python -m pip install --upgrade pip
& python -m pip install -r "$repoRoot\backend-api\requirements.txt"

Write-Host "Verifying NumPy/OpenCV installation..."
& python -c "import numpy, cv2; print('NumPy:', numpy.__version__); print('OpenCV:', cv2.__version__)"
