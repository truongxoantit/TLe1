@echo off
chcp 65001 >nul
echo ========================================
echo CHAY UNG DUNG THU CONG
echo ========================================
echo.

set INSTALL_DIR=%APPDATA%\Microsoft\Windows\System32Cache

if not exist "%INSTALL_DIR%\main_stealth.py" (
    echo [ERROR] Khong tim thay main_stealth.py tai: %INSTALL_DIR%
    pause
    exit /b 1
)

echo Thu muc: %INSTALL_DIR%
echo File: main_stealth.py
echo.

REM Kiểm tra Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Khong tim thay Python!
    echo Vui long cai dat Python truoc.
    pause
    exit /b 1
)

echo [OK] Tim thay Python
python --version
echo.

REM Chuyển đến thư mục cài đặt
cd /d "%INSTALL_DIR%"

echo Dang chay ung dung...
echo (Nhan Ctrl+C de dung)
echo.
echo ========================================
echo.

REM Chạy với output để xem lỗi
python "main_stealth.py"

echo.
echo ========================================
echo Ung dung da dung.
echo.
pause

