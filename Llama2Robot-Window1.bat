@echo off
mode 89,44
rem con:cols=89 lines=100
title Llama2Robot-Window1
cls

:: Run the main1.py script
echo Launching Llama2Robot-Window1...
echo.
echo Options: --output
echo.
@echo on
wsl python3 main1.py --output
@echo off
echo.
echo.

:: Exiting
echo Llama2Robot-Window1 shutting down...
echo.
echo.
pause
exit /b
