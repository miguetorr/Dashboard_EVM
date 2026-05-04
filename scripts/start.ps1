<#
.SYNOPSIS
    Levanta backend y frontend simultaneamente.
.DESCRIPTION
    Abre el backend (uvicorn) y el frontend (vite) en procesos paralelos.
    Con Ctrl+C se detienen ambos.
.NOTES
    Ejecutar desde la raíz del proyecto:
    powershell -ExecutionPolicy Bypass -File scripts\start.ps1
#>

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EVM Tracker - Iniciando servidores"     -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$backendDir = Join-Path $Root "backend"
$frontendDir = Join-Path $Root "frontend"
$venvDir = Join-Path $backendDir ".venv"
$pythonExe = Join-Path $venvDir "Scripts\python.exe"

# Verificar que el setup se haya ejecutado
if (-not (Test-Path $pythonExe)) {
    Write-Host "ERROR: No se encontro el entorno virtual." -ForegroundColor Red
    Write-Host "Ejecuta primero: powershell -ExecutionPolicy Bypass -File scripts\setup.ps1" -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path (Join-Path $frontendDir "node_modules"))) {
    Write-Host "ERROR: No se encontro node_modules." -ForegroundColor Red
    Write-Host "Ejecuta primero: powershell -ExecutionPolicy Bypass -File scripts\setup.ps1" -ForegroundColor Yellow
    exit 1
}

# ── Iniciar backend en background ────────────────────────────────────────────
Write-Host "Iniciando backend (FastAPI en puerto 8000)..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    param($pythonExe, $backendDir)
    Set-Location $backendDir
    & $pythonExe -m uvicorn app.main:app --reload --port 8000 2>&1
} -ArgumentList $pythonExe, $backendDir

# ── Iniciar frontend en background ──────────────────────────────────────────
Write-Host "Iniciando frontend (Vite en puerto 5173)..." -ForegroundColor Yellow
$frontendJob = Start-Job -ScriptBlock {
    param($frontendDir)
    Set-Location $frontendDir
    npx vite 2>&1
} -ArgumentList $frontendDir

# ── Esperar a que arranquen ──────────────────────────────────────────────────
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Servidores levantados!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Backend  (API):    http://localhost:8000" -ForegroundColor White
Write-Host "  Swagger UI:        http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Frontend (React):  http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "  Presiona Ctrl+C para detener ambos servidores." -ForegroundColor DarkGray
Write-Host ""

# ── Monitorear output hasta Ctrl+C ──────────────────────────────────────────
try {
    while ($true) {
        # Mostrar logs del backend
        $backendOutput = Receive-Job -Job $backendJob -ErrorAction SilentlyContinue
        if ($backendOutput) {
            $backendOutput | ForEach-Object {
                Write-Host "[backend]  $_" -ForegroundColor DarkCyan
            }
        }

        # Mostrar logs del frontend
        $frontendOutput = Receive-Job -Job $frontendJob -ErrorAction SilentlyContinue
        if ($frontendOutput) {
            $frontendOutput | ForEach-Object {
                Write-Host "[frontend] $_" -ForegroundColor DarkMagenta
            }
        }

        # Verificar si algún job murió
        if ($backendJob.State -eq "Failed") {
            Write-Host "ERROR: El backend se detuvo inesperadamente." -ForegroundColor Red
            Receive-Job -Job $backendJob | Write-Host -ForegroundColor Red
            break
        }
        if ($frontendJob.State -eq "Failed") {
            Write-Host "ERROR: El frontend se detuvo inesperadamente." -ForegroundColor Red
            Receive-Job -Job $frontendJob | Write-Host -ForegroundColor Red
            break
        }

        Start-Sleep -Milliseconds 500
    }
} finally {
    Write-Host ""
    Write-Host "Deteniendo servidores..." -ForegroundColor Yellow
    Stop-Job -Job $backendJob -ErrorAction SilentlyContinue
    Stop-Job -Job $frontendJob -ErrorAction SilentlyContinue
    Remove-Job -Job $backendJob -Force -ErrorAction SilentlyContinue
    Remove-Job -Job $frontendJob -Force -ErrorAction SilentlyContinue
    Write-Host "Servidores detenidos." -ForegroundColor Green
}
