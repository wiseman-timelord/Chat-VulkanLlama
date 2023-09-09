@echo off
mode 45,20
rem con:cols=90 lines=100
title Llama2Robot-Launcher


:: Run both windows for Llama2Robot
echo Launching, Window1 & Windows2...
@echo on
start cmd.exe /K "main1.bat"
start cmd.exe /K "main2.bat"
echo Window1 & Windows2, Launched!
@echo off
echo.
echo.


:: Exiting
echo Exiting Launcher!
exit