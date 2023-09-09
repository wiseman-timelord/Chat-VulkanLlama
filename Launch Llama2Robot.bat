@echo off
mode 45,20
title Llama2Robot-Launcher

:: Intro
echo.
echo.
echo The Llama2Robot-Launcher
echo -=-=-=-=-=-=-=-=-=-=-=-=
echo.

:: Check for ENV file
echo.
echo Searching for ENV...
timeout /t 1 /nobreak >nul
if exist .\.ENV (
    echo ENV file found.
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
echo Launching, Window1 & Window2...
echo.
timeout /t 1 /nobreak >nul
echo Options for main1: --output
timeout /t 2 /nobreak >nul
echo.
@echo on
start cmd.exe /K "call .\scripts\window1.bat --output"
start cmd.exe /K "call .\scripts\window2.bat"
echo Window1 & Window2, Launched!
@echo off
timeout /t 1 /nobreak >nul
echo.
echo Exiting Launcher!
echo.
exit

