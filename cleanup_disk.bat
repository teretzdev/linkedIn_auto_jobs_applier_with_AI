@echo on
setlocal enabledelayedexpansion

echo Cleaning up temporary files and freeing up disk space...

:: Step 1: Clean pip cache
echo Cleaning pip cache...
py -3.12 -m pip cache purge
if %errorlevel% neq 0 (
    echo Failed to clean pip cache. Continuing with the next steps...
)

:: Step 2: Clean Windows temporary files
echo Cleaning Windows temporary files...
del /q /s %TEMP%\*
if %errorlevel% neq 0 (
    echo Failed to clean temporary files. Continuing with the next steps...
)

:: Step 2.1: Clean Windows prefetch files
echo Cleaning Windows prefetch files...
del /q /s C:\Windows\Prefetch\*
if %errorlevel% neq 0 (
    echo Failed to clean prefetch files. Continuing with the next steps...
)

:: Step 2.2: Clean Windows update cache
echo Cleaning Windows update cache...
del /q /s C:\Windows\SoftwareDistribution\Download\*
if %errorlevel% neq 0 (
    echo Failed to clean Windows update cache. Continuing with the next steps...
)

:: Step 3: Check disk space
echo Checking disk space on the system drive...
for /f "tokens=3" %%a in ('dir C:\ ^| find "bytes free"') do set FreeSpace=%%a
echo Free space on C:\: %FreeSpace%

echo Cleanup completed successfully. Please ensure there is sufficient disk space before proceeding with the installation.
pause