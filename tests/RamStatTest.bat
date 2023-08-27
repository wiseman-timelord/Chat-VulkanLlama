@echo off
mode 85,40
title RamStatTest
cls

:: Run the ramstattest.py script
echo Launching RamStatTest...
echo.
@echo on
wsl python3 ramstattest.py
@echo off
echo.
echo.

:: Exiting
echo RamStatTest shutting down...
echo.
echo.
pause
exit /b
