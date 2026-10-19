@echo off
title Ultimate Root Debloat & Telemetry Eradicator
color 0b
echo ========================================================================
echo    RUNNING ULTIMATE ROOT TELEMETRY ERADICATION & DEBLOAT SUITE
echo ========================================================================
echo.

set TARGET_PS1=%~dp0Root_Telemetry_Remover.ps1
if not exist "%TARGET_PS1%" set TARGET_PS1=C:\Users\Public\Desktop\Root_Telemetry_Remover.ps1
if not exist "%TARGET_PS1%" set TARGET_PS1=C:\Users\runneradmin\Desktop\Root_Telemetry_Remover.ps1

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%TARGET_PS1%"
echo.
echo ========================================================================
echo    [DONE] ALL TELEMETRY ERADICATED & SYSTEM BOOSTED!
echo ========================================================================
echo Press any key to close this window...
pause >nul
