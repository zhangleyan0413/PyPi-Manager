@echo off
chcp 65001 >nul

echo ===============================
echo PyPi Manager - File Check
echo ===============================

REM 检查必要的文件
set "FILES=main.py main_gui.py version_fetcher.py installer.py setup.bat"

for %%f in (!FILES!) do (
    if exist "%%f" (
        echo %%f exists
    ) else (
        echo %%f missing
    )
)

REM 检查Python和依赖
set "ERROR_COUNT=0"

echo ===============================
echo Checking Python and dependencies
echo ===============================

REM 检查Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python: OK
) else (
    echo Python: NOT FOUND
    set "ERROR_COUNT=1"
)

REM 检查requests
python -c "import requests" >nul 2>&1
if %errorlevel% equ 0 (
    echo requests: OK
) else (
    echo requests: NOT FOUND
    set "ERROR_COUNT=1"
)

REM 检查wxPython
python -c "import wx" >nul 2>&1
if %errorlevel% equ 0 (
    echo wxPython: OK
) else (
    echo wxPython: NOT FOUND
    set "ERROR_COUNT=1"
)

echo ===============================
if %ERROR_COUNT% equ 0 (
    echo All checks passed! You can run setup.bat to start PyPi Manager.
) else (
    echo Some checks failed. Please run setup.bat to install missing components.
)
echo ===============================
pause