@echo off
mode 90,45
rem con:cols=90 lines=100
title Llama2Robot-Window1
cls

:: Run the main1.py script
echo Launching Llama2Robot-Window1...
echo.
@echo on
wsl python3 main1.py %1
@echo off
echo.
echo.

:: Exiting
echo Llama2Robot-Window1 shutting down...
echo.
echo.
pause
exit /b