@echo off
cls

:: Store the current directory
set "currentDir=%cd%"
echo Current working directory detected: %currentDir%

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    goto gotAdmin
) else (
    goto requestAdmin
)

:requestAdmin
echo Requesting administrative privileges...
echo.

:: Create a temporary batch file to set the directory
echo @echo off > "%temp%\tempBatch.bat"
echo cd /d "%currentDir%" >> "%temp%\tempBatch.bat"
echo "%~f0" >> "%temp%\tempBatch.bat"

:: Get the full path of the current batch script
set "batchPath=%~f0"
echo Batch script path: %batchPath%
goto checkUAC

:checkUAC
echo Creating VBScript to request admin privileges...
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%temp%\tempBatch.bat", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
exit /b

:gotAdmin
:: If running with admin privileges, proceed with the script
echo Installing the requirements...
echo.
wsl pip3 install -r requirements.txt

:: Check if requirements.txt was found and installed successfully
if %errorLevel% == 0 (
    echo Requirements install finished.
) else (
    echo ERROR: Could not install.
)
echo.

:: Pause at the end
pause
exit /b
