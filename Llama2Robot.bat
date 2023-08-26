@echo off
mode 85,43
rem con:cols=85 lines=100
title Llama2Robot
cls

:: Run the freqbeat.py script
echo Launching Llama2Robot...
echo.
@echo on
wsl python3 main.py
@echo off
echo.
echo.

:: Exiting
echo Llama2Robot shutting down...
echo.
echo.
pause
exit /b
