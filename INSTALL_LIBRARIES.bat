@echo off
chcp 65001 >nul
echo ========================================
echo CAI DAT THU VIEN CAN THIET
echo ========================================
echo.

REM Tìm Python đúng
set "PYTHON_PATH="
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PYTHON_PATH=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
) else (
    where python >nul 2>&1
    if not errorlevel 1 (
        for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%i"
    )
)

if "%PYTHON_PATH%"=="" (
    echo [ERROR] Khong tim thay Python!
    pause
    exit /b 1
)

echo [OK] Tim thay Python: %PYTHON_PATH%
echo.

REM Cài đặt các thư viện
echo [1/8] Dang cai dat python-telegram-bot...
%PYTHON_PATH% -m pip install python-telegram-bot --upgrade
echo.

echo [2/8] Dang cai dat opencv-python...
%PYTHON_PATH% -m pip install opencv-python --upgrade
echo.

echo [3/8] Dang cai dat numpy...
%PYTHON_PATH% -m pip install numpy --upgrade
echo.

echo [4/8] Dang cai dat pynput...
%PYTHON_PATH% -m pip install pynput --upgrade
echo.

echo [5/8] Dang cai dat psutil...
%PYTHON_PATH% -m pip install psutil --upgrade --no-cache-dir 2>nul
if errorlevel 1 (
    echo [RETRY] Thu cai dat tu mirror Tsinghua...
    %PYTHON_PATH% -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple psutil --no-cache-dir 2>nul
)
if errorlevel 1 (
    echo [RETRY] Thu cai dat tu mirror Aliyun...
    %PYTHON_PATH% -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com psutil --no-cache-dir 2>nul
)
echo.

echo [6/8] Dang cai dat pyperclip...
%PYTHON_PATH% -m pip install pyperclip --upgrade
echo.

echo [7/8] Dang cai dat pywin32...
%PYTHON_PATH% -m pip install pywin32 --upgrade --no-cache-dir 2>nul
if errorlevel 1 (
    echo [RETRY] Thu cai dat tu mirror Tsinghua...
    %PYTHON_PATH% -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pywin32 --no-cache-dir 2>nul
)
if errorlevel 1 (
    echo [RETRY] Thu cai dat tu mirror Aliyun...
    %PYTHON_PATH% -m pip install -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com pywin32 --no-cache-dir 2>nul
)
echo.

echo [8/8] Dang cai dat pystray...
%PYTHON_PATH% -m pip install pystray --upgrade
echo.

REM Kiểm tra
echo ========================================
echo KIEM TRA CAI DAT
echo ========================================
echo.

%PYTHON_PATH% -c "from telegram import Bot; print('[OK] python-telegram-bot')" 2>nul || echo [ERROR] python-telegram-bot
%PYTHON_PATH% -c "import cv2; print('[OK] opencv-python')" 2>nul || echo [ERROR] opencv-python
%PYTHON_PATH% -c "import numpy; print('[OK] numpy')" 2>nul || echo [ERROR] numpy
%PYTHON_PATH% -c "import pynput; print('[OK] pynput')" 2>nul || echo [ERROR] pynput
%PYTHON_PATH% -c "import psutil; print('[OK] psutil')" 2>nul || echo [ERROR] psutil
%PYTHON_PATH% -c "import pyperclip; print('[OK] pyperclip')" 2>nul || echo [ERROR] pyperclip
%PYTHON_PATH% -c "import win32gui; print('[OK] pywin32')" 2>nul || echo [ERROR] pywin32
%PYTHON_PATH% -c "import pystray; print('[OK] pystray')" 2>nul || echo [WARNING] pystray (khong bat buoc)

echo.
echo ========================================
echo HOAN TAT!
echo ========================================
pause

