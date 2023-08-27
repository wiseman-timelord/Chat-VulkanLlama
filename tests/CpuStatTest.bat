@echo off
mode 85,40
title CpuStatTest
cls

:: Run the ramstattest.py script
echo Launching CpuStatTest...
echo.
@echo on
wsl python3 cpustattest.py
@echo off
echo.
echo.

:: Exiting
echo CpuStatTest shutting down...
echo.
echo.
pause
exit /b
