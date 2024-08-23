@echo off
setlocal enabledelayedexpansion
cls

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
echo         Chat-LlamaVulkan - Installer
echo *********************************************
echo.
set "ScriptDirectoryWt=%~dp0"
set "ScriptDirectoryWt=%ScriptDirectoryWt:~0,-1%"
pushd "%ScriptDirectoryWt%"
echo Working Dir: %ScriptDirectoryWt%
echo.

:install
echo Installing the requirements...
echo.

:: Install WSL requirements
wsl sudo apt-get update
if errorlevel 1 goto :error
wsl sudo apt-get install -y libncurses5-dev
if errorlevel 1 goto :error

:: Install Python requirements
powershell -Command "& {pip install -r ./data/requires/req_wsl.txt; if ($LASTEXITCODE -ne 0) {exit 1}}"
if errorlevel 1 goto :error
powershell -Command "& {pip install -r ./data/requires/req_win.txt; if ($LASTEXITCODE -ne 0) {exit 1}}"
if errorlevel 1 goto :error

echo Requirements installed successfully.
goto :end

:error
echo An error occurred during installation.
pause
exit /b 1

:end
echo.
echo Installation complete.
pause
exit /b 0