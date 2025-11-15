@echo off
chcp 65001 >nul
echo ========================================
echo SUA LOI CAI DAT
echo ========================================
echo.

set INSTALL_DIR=%APPDATA%\Microsoft\Windows\System32Cache

echo Thu muc cai dat: %INSTALL_DIR%
echo.

REM Kiểm tra file main_stealth.py
if exist "%INSTALL_DIR%\main_stealth.py" (
    echo [INFO] Tim thay file main_stealth.py
    echo Kiem tra noi dung...
    
    REM Kiểm tra xem file có chứa "404" không
    findstr /C:"404" /C:"Not Found" "%INSTALL_DIR%\main_stealth.py" >nul 2>&1
    if not errorlevel 1 (
        echo [ERROR] File main_stealth.py bi loi 404!
        echo Noi dung file:
        type "%INSTALL_DIR%\main_stealth.py"
        echo.
        echo [FIX] Dang xoa file loi...
        attrib -h -s "%INSTALL_DIR%\main_stealth.py" >nul 2>&1
        del /f /q "%INSTALL_DIR%\main_stealth.py" >nul 2>&1
        echo [OK] Da xoa file loi
    ) else (
        REM Kiểm tra kích thước file
        for %%f in ("%INSTALL_DIR%\main_stealth.py") do (
            if %%~zf LSS 100 (
                echo [ERROR] File main_stealth.py qua nho (%%~zf bytes)!
                echo [FIX] Dang xoa file loi...
                attrib -h -s "%INSTALL_DIR%\main_stealth.py" >nul 2>&1
                del /f /q "%INSTALL_DIR%\main_stealth.py" >nul 2>&1
                echo [OK] Da xoa file loi
            ) else (
                echo [OK] File main_stealth.py hop le (%%~zf bytes)
            )
        )
    )
) else (
    echo [INFO] Khong tim thay file main_stealth.py
)

echo.
echo ========================================
echo HOAN TAT!
echo ========================================
echo.
echo Bay gio chay lai INSTALL.bat de tai lai file.
echo.
pause

