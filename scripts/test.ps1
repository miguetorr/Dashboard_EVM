<#
.SYNOPSIS
    Ejecuta todos los tests y linters del proyecto.
.DESCRIPTION
    - Tests backend (pytest + cobertura)
    - Linter backend (flake8)
    - TypeScript check (tsc)
    - Linter frontend (eslint)
.NOTES
    Ejecutar desde la raíz del proyecto:
    powershell -ExecutionPolicy Bypass -File scripts\test.ps1
#>

$ErrorActionPreference = "Continue"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EVM Tracker - Tests y calidad"          -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$backendDir = Join-Path $Root "backend"
$frontendDir = Join-Path $Root "frontend"
$venvDir = Join-Path $backendDir ".venv"
$pythonExe = Join-Path $venvDir "Scripts\python.exe"
$allPassed = $true

# ── 1. Tests backend ────────────────────────────────────────────────────────
Write-Host "[1/4] Tests backend (pytest + cobertura)..." -ForegroundColor Yellow
Write-Host ""
Push-Location $backendDir
try {
    & $pythonExe -m pytest --cov=app --cov-report=term-missing -q
    if ($LASTEXITCODE -ne 0) { $allPassed = $false }
} finally {
    Pop-Location
}

# ── 2. Linter backend ───────────────────────────────────────────────────────
Write-Host ""
Write-Host "[2/4] Linter backend (flake8)..." -ForegroundColor Yellow
Push-Location $backendDir
try {
    & $pythonExe -m flake8 app/
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  flake8: 0 errores" -ForegroundColor Green
    } else {
        $allPassed = $false
    }
} finally {
    Pop-Location
}

# ── 3. TypeScript check ─────────────────────────────────────────────────────
Write-Host ""
Write-Host "[3/4] TypeScript check (tsc)..." -ForegroundColor Yellow
Push-Location $frontendDir
try {
    npx tsc --noEmit
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  tsc: 0 errores" -ForegroundColor Green
    } else {
        $allPassed = $false
    }
} finally {
    Pop-Location
}

# ── 4. Linter frontend ──────────────────────────────────────────────────────
Write-Host ""
Write-Host "[4/4] Linter frontend (eslint)..." -ForegroundColor Yellow
Push-Location $frontendDir
try {
    npx eslint src/
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  eslint: 0 errores" -ForegroundColor Green
    } else {
        $allPassed = $false
    }
} finally {
    Pop-Location
}

# ── Resultado ────────────────────────────────────────────────────────────────
Write-Host ""
if ($allPassed) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Todo paso correctamente!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  Hay errores. Revisa los detalles." -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}
Write-Host ""
