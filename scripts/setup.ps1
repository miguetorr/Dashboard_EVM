<#
.SYNOPSIS
    Configura todo el proyecto EVM Tracker desde cero.
.DESCRIPTION
    - Copia .env.example a .env si no existe
    - Crea el entorno virtual de Python e instala dependencias
    - Instala dependencias de Node.js para el frontend
    - Verifica que todo esté listo
.NOTES
    Ejecutar desde la raíz del proyecto:
    powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
#>

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EVM Tracker - Setup automatico"        -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# ── 1. Variables de entorno ──────────────────────────────────────────────────
Write-Host "[1/4] Variables de entorno..." -ForegroundColor Yellow
$envFile = Join-Path $Root ".env"
$envExample = Join-Path $Root ".env.example"

if (Test-Path $envFile) {
    Write-Host "  .env ya existe, se conserva." -ForegroundColor DarkGray
} elseif (Test-Path $envExample) {
    Copy-Item $envExample $envFile
    Write-Host "  .env creado desde .env.example" -ForegroundColor Green
} else {
    Write-Host "  AVISO: No se encontro .env.example. Crea .env manualmente." -ForegroundColor Red
}

# ── 2. Backend (Python) ─────────────────────────────────────────────────────
Write-Host ""
Write-Host "[2/4] Configurando backend (Python)..." -ForegroundColor Yellow
$backendDir = Join-Path $Root "backend"
$venvDir = Join-Path $backendDir ".venv"

if (-not (Test-Path $venvDir)) {
    Write-Host "  Creando entorno virtual..."
    python -m venv $venvDir
    Write-Host "  Entorno virtual creado." -ForegroundColor Green
} else {
    Write-Host "  Entorno virtual ya existe." -ForegroundColor DarkGray
}

$pipExe = Join-Path $venvDir "Scripts\pip.exe"
Write-Host "  Instalando dependencias Python..."
$ErrorActionPreference = "Continue"
& $pipExe install -r (Join-Path $backendDir "requirements.txt") --quiet 2>$null
$ErrorActionPreference = "Stop"
Write-Host "  Dependencias Python instaladas." -ForegroundColor Green

# ── 3. Frontend (Node.js) ───────────────────────────────────────────────────
Write-Host ""
Write-Host "[3/4] Configurando frontend (Node.js)..." -ForegroundColor Yellow
$frontendDir = Join-Path $Root "frontend"

Push-Location $frontendDir
try {
    Write-Host "  Instalando dependencias npm..."
    npm install --silent 2>$null
    Write-Host "  Dependencias npm instaladas." -ForegroundColor Green
} finally {
    Pop-Location
}

# ── 4. Verificacion ─────────────────────────────────────────────────────────
Write-Host ""
Write-Host "[4/4] Verificando instalacion..." -ForegroundColor Yellow

$pythonExe = Join-Path $venvDir "Scripts\python.exe"
$ok = $true

# Python
try {
    $pyVer = & $pythonExe --version 2>&1
    Write-Host "  Python:   $pyVer" -ForegroundColor Green
} catch {
    Write-Host "  Python:   ERROR" -ForegroundColor Red
    $ok = $false
}

# FastAPI
try {
    & $pythonExe -c "import fastapi; print(f'  FastAPI:  {fastapi.__version__}')" 2>&1 | Write-Host -ForegroundColor Green
} catch {
    Write-Host "  FastAPI:  No instalado" -ForegroundColor Red
    $ok = $false
}

# Node
try {
    $nodeVer = node --version 2>&1
    Write-Host "  Node.js:  $nodeVer" -ForegroundColor Green
} catch {
    Write-Host "  Node.js:  No encontrado" -ForegroundColor Red
    $ok = $false
}

# Resultado
Write-Host ""
if ($ok) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  Setup completado exitosamente!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Siguiente paso:" -ForegroundColor White
    Write-Host "  powershell -ExecutionPolicy Bypass -File scripts\start.ps1" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "NOTA: Necesitas PostgreSQL con la BD creada." -ForegroundColor Yellow
    Write-Host "  psql -U postgres -c `"CREATE DATABASE evm_tracker;`"" -ForegroundColor DarkGray
    Write-Host "  psql -U postgres -d evm_tracker -f backend\database\schema.sql" -ForegroundColor DarkGray
    Write-Host "  psql -U postgres -d evm_tracker -f backend\database\seed.sql" -ForegroundColor DarkGray
} else {
    Write-Host "Setup completo con advertencias. Revisa los errores arriba." -ForegroundColor Yellow
}
Write-Host ""
