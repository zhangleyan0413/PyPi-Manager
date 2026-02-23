@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ===============================
echo Python Auto Install Environment Check
echo ===============================

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python is installed
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo Current Python version: !PYTHON_VERSION!
) else (
    echo Python not installed, starting download...
    
    REM Set Python download version
    set PYTHON_VERSION=3.11.9
    set PYTHON_INSTALLER=python-!PYTHON_VERSION!-amd64.exe
    set DOWNLOAD_URL=https://www.python.org/ftp/python/!PYTHON_VERSION!/!PYTHON_INSTALLER!
    
    echo Downloading Python !PYTHON_VERSION!...
    echo This may take a few minutes, please wait...
    powershell -Command "Invoke-WebRequest -Uri '!DOWNLOAD_URL!' -OutFile '!PYTHON_INSTALLER!'"
    
    if exist "!PYTHON_INSTALLER!" (
        echo Download completed, starting installation...
        echo Installation progress will be shown below...
        !PYTHON_INSTALLER! /passive PrependPath=1 Include_pip=1
        echo Python installation completed
        del "!PYTHON_INSTALLER!"
    ) else (
        echo Python installer download failed
        pause
        exit /b 1
    )
)

REM Always check and install dependencies
echo Checking dependencies...

REM Check requests library
echo Checking requests library...
python -c "import requests" >nul 2>&1
if %errorlevel% equ 0 (
    echo requests is installed
) else (
    echo requests library not found, installing...
    echo Installation progress will be shown below...
    python -m pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
    if %errorlevel% equ 0 (
        echo requests installation successful
    ) else (
        echo requests installation failed
        pause
        exit /b 1
    )
)

REM Check wxPython library
echo Checking wxPython library...
python -c "import wx" >nul 2>&1
if %errorlevel% equ 0 (
    echo wxPython is installed
) else (
    echo wxPython library not found, installing...
    echo Installation progress will be shown below...
    python -m pip install wxPython -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir
    if %errorlevel% equ 0 (
        echo wxPython installation successful
    ) else (
        echo wxPython installation failed
        pause
        exit /b 1
    )
)

echo All dependencies are installed

echo ===============================
echo Environment check completed, starting program...
echo ===============================

REM Start main program with GUI interface
echo Starting PyPi Manager with GUI Interface...
python main.py

echo Program execution completed
pause
endlocal