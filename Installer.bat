@echo off
setlocal enabledelayedexpansion
cls

:: Set the filename to download
set "llamaVulkanZip=llama-b3617-bin-win-vulkan-x64.zip"
set "downloadUrl=https://github.com/ggerganov/llama.cpp/releases/download/b3617/%llamaVulkanZip%"

:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrative privileges.
    echo Please run this script as an administrator.
    timeout /t 5
    goto :error
)
echo Running with Admin rights.

:: Script Working Directory
set "ScriptDirectory=%~dp0"
set "ScriptDirectory=%ScriptDirectory:~0,-1%"
pushd "%ScriptDirectory%"

:: Custom Banner
echo *******************************************************************************************************************
echo                                          Chat-LlamaVulkan - Installer
echo *******************************************************************************************************************
echo.
echo Working Dir: %ScriptDirectory%
echo.

:: Install Requirements
echo Installing Pip Requirements...
pip install -r ./data/requires/requirements.txt
echo Requirements install finished.
timeout /t 2

:: Install Libraries
echo Checking for ".\cache" directory...
if not exist ".\cache" (
    echo ".\cache" directory not found. Creating it...
    mkdir ".\cache"
    echo ".\cache" directory created.
) else (
    echo ".\cache" directory already exists.
)
timeout /t 2

:: Check if the file exists in the cache
set "cachedFilePath=.\cache\%llamaVulkanZip%"
if exist "%cachedFilePath%" (
    echo Cached file found. Continuing.
) else (
    echo Downloading Llama Vulkan Binary...
    powershell -Command "Invoke-WebRequest -Uri '%downloadUrl%' -OutFile '%cachedFilePath%'"
)

if %errorlevel% neq 0 (
    echo Failed to download Llama Vulkan Binary.
    goto :error
)
timeout /t 2

:: Locate 7-Zip
echo Locating 7-Zip...
set "sevenZipPath="
if exist "C:\Program Files\7-Zip\7z.exe" (
    set "sevenZipPath=C:\Program Files\7-Zip\7z.exe"
) else if exist "C:\Program Files (x86)\7-Zip\7z.exe" (
    set "sevenZipPath=C:\Program Files (x86)\7z.exe"
)

if not defined sevenZipPath (
    echo 7-Zip not found in default locations. Please install 7-Zip.
    goto :error
) else (
    echo 7-Zip found at "%sevenZipPath%".
)
timeout /t 2

:: Ensure the .\libraries folder exists and is empty
if not exist ".\libraries" (
    mkdir ".\libraries"
    echo ".\libraries" directory created.
) else (
    echo ".\libraries" directory already exists.
    if exist ".\libraries\*.*" (
        echo Clearing contents of ".\libraries" directory...
        del /s /q ".\libraries\*.*"
    )
    echo ".\libraries" directory is now empty.
)
timeout /t 2

:: Extract Llama Vulkan Binary
echo Extracting Llama Vulkan Binary to ".\libraries"...
"%sevenZipPath%" x "%cachedFilePath%" -o".\libraries" -mmt4 -y
if %errorlevel% neq 0 (
    echo Failed to extract Llama Vulkan Binary.
    goto :error
)
timeout /t 2

:: Installer Complete
goto :end

:error
echo An error occurred during installation.
pause
exit /b 1

:end
echo.
echo Installation Processes Completed.
timeout /t 2
exit /b 0
