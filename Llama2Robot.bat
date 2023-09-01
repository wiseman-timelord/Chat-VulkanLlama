@echo off
mode 89,37
rem con:cols=89 lines=100
title Llama2Robot
cls

:: Run the freqbeat.py script
echo Launching Llama2Robot...
echo.
echo Options: --output
echo.
@echo 
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
