@echo off
mode 45,18
title Llama2Robot-Launcher

:: Intro
echo *********************************************
echo                MULTI-LAUNCHR
echo *********************************************

:: Check for ENV file
echo.
echo Searching for ENV...
timeout /t 1 /nobreak >nul
if exist .\.ENV (
    echo ENV file found.
	echo.
    timeout /t 2 /nobreak >nul
) else (
    echo ...ENV file not found...
    timeout /t 1 /nobreak >nul
    echo.
    copy .\data\example.ENV .\.ENV
    echo ...ENV file created.
    echo.
    echo Review .ENV now then re-launch!
    echo.
    timeout /t 2 /nobreak >nul
    echo.
    pause
    exit /b
)


:: Run both windows for Llama2Robot
echo Launching 2 Windows...
echo.
timeout /t 1 /nobreak >nul
echo Options for main1.py: --output
echo.
timeout /t 2 /nobreak >nul
@echo on
start cmd.exe /K "call .\scripts\window1.bat --output"
start cmd.exe /K "call .\scripts\window2.bat"
echo Program Launched!
@echo off
timeout /t 1 /nobreak >nul
echo Exiting Launcher!
echo.
timeout /t 1 /nobreak >nul
exit

