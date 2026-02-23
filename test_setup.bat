@echo off
chcp 65001 >nul

 echo Testing setup.bat functionality...
 echo ===============================

REM Test 1: Check if Python is available
 echo Test 1: Checking Python installation...
 python --version
 if %errorlevel% equ 0 (
     echo Python is available
 ) else (
     echo Python is not available
 )

REM Test 2: Check if requests is installed
 echo Test 2: Checking requests library...
 python -c "import requests"
 if %errorlevel% equ 0 (
     echo requests is installed
 ) else (
     echo requests is not installed
 )

REM Test 3: Check if wxPython is installed
 echo Test 3: Checking wxPython library...
 python -c "import wx"
 if %errorlevel% equ 0 (
     echo wxPython is installed
 ) else (
     echo wxPython is not installed
 )

REM Test 4: Check if main.py exists
 echo Test 4: Checking main.py...
 if exist "main.py" (
     echo main.py exists
 ) else (
     echo main.py does not exist
 )

REM Test 5: Check if main_gui.py exists
 echo Test 5: Checking main_gui.py...
 if exist "main_gui.py" (
     echo main_gui.py exists
 ) else (
     echo main_gui.py does not exist
 )

echo ===============================
 echo Test completed.
 pause