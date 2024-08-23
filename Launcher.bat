@echo off
mode 45,22
title Chat-LlamaVulkan-Launcher

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrative privileges.
    echo Please run this script as an administrator.
    pause
    exit /b 1
)
echo Running with Admin rights.

:: Intro
echo *********************************************
echo         Chat-LlamaVulkan - Launcher
echo *********************************************
echo.
set "ScriptDirectoryWt=%~dp0"
set "ScriptDirectoryWt=%ScriptDirectoryWt:~0,-1%"
pushd "%ScriptDirectoryWt%"
echo Working Dir: %ScriptDirectoryWt%
echo.

:: Run both windows for Chat-LlamaVulkan
echo Launching 2 Windows...
echo.
timeout /t 1 /nobreak >nul
echo Options for window1: --logs
echo Options for window2: --tts --sound
echo.
timeout /t 2 /nobreak >nul

start "" cmd /c "wsl python3 window_1.py --logs || pause"
if errorlevel 1 (
    echo Error launching window 1.
    pause
    exit /b 1
)

start "" cmd /c "python window_2.py --tts --sound || pause"
if errorlevel 1 (
    echo Error launching window 2.
    pause
    exit /b 1
)

echo.
echo Windows launched, closing in 3 seconds...
echo.
timeout /t 3 /nobreak >nul
exit /b 0