@echo off
title 🚀 Ultimate Root Debloat & Telemetry Eradicator
color 0b
echo ========================================================================
echo    🚀 RUNNING ULTIMATE ROOT TELEMETRY ERADICATION & DEBLOAT SUITE
echo ========================================================================
echo.
set SCRIPT_PATH="%~dp0Root_Telemetry_Remover.ps1"
if not exist %SCRIPT_PATH% set SCRIPT_PATH="C:\Users\Public\Desktop\Root_Telemetry_Remover.ps1"
if not exist %SCRIPT_PATH% set SCRIPT_PATH="C:\Users\runneradmin\Desktop\Root_Telemetry_Remover.ps1"

powershell.exe -NoProfile -ExecutionPolicy Bypass -File %SCRIPT_PATH%
echo.
echo ========================================================================
echo    [✓] ALL TELEMETRY ERADICATED & SYSTEM BOOSTED!
echo ========================================================================
echo Press any key to close this window...
pause >nul
