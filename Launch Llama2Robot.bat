@echo off
mode 45,20
title Llama2Robot-Launcher

:: Run both windows for Llama2Robot
echo Launching, Window1 & Windows2...
echo.
echo Options for main1: --output
echo.
@echo on
start cmd.exe /K "call .\scripts\window1.bat --output"
start cmd.exe /K "call .\scripts\window2.bat"
echo Window1 & Windows2, Launched!
@echo off
echo.
echo.

:: Exiting
echo Exiting Launcher!
exit