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
echo Options for window1: --logs
echo Options for window2: --tts --sound
echo.
timeout /t 2 /nobreak >nul
@echo on
start cmd.exe /K "call .\scripts\window1.bat --logs"
start cmd.exe /K "call .\scripts\window2.bat --tts --sound"
@echo off
echo Exiting Launcher!
echo.
timeout /t 3 /nobreak >nul
exit

