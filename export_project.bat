@echo off
setlocal enabledelayedexpansion

REM اسکریپت خروجی گرفتن از پروژه DjangoCraft برای Windows
REM این اسکریپت پروژه را برای انتقال آماده می‌کند

echo 🚀 شروع خروجی گرفتن از پروژه DjangoCraft...

REM تنظیم متغیرها
set PROJECT_NAME=DjangoCraft
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "TIMESTAMP=%dt:~0,8%_%dt:~8,6%"
set EXPORT_DIR=%PROJECT_NAME%_export_%TIMESTAMP%
set CURRENT_DIR=%CD%

REM ایجاد دایرکتوری خروجی
echo 📁 ایجاد دایرکتوری خروجی: %EXPORT_DIR%
if not exist "%EXPORT_DIR%" mkdir "%EXPORT_DIR%"

REM کپی کردن فایل‌های اصلی پروژه
echo 📋 کپی کردن فایل‌های پروژه...
xcopy "core" "%EXPORT_DIR%\core\" /E /I /Y >nul
xcopy "project_manager" "%EXPORT_DIR%\project_manager\" /E /I /Y >nul
copy "manage.py" "%EXPORT_DIR%\" >nul
copy "requirements.txt" "%EXPORT_DIR%\" >nul
copy "README.md" "%EXPORT_DIR%\" >nul
copy "LICENSE" "%EXPORT_DIR%\" >nul
copy "env_example.txt" "%EXPORT_DIR%\" >nul

REM کپی کردن فایل‌های Docker (اگر وجود دارند)
if exist "Dockerfile" (
    copy "Dockerfile" "%EXPORT_DIR%\" >nul
)

if exist "docker-compose.yml" (
    copy "docker-compose.yml" "%EXPORT_DIR%\" >nul
)

if exist "nginx.conf" (
    copy "nginx.conf" "%EXPORT_DIR%\" >nul
)

REM کپی کردن فایل‌های اضافی
if exist "deployment_guide.md" (
    copy "deployment_guide.md" "%EXPORT_DIR%\" >nul
)

REM حذف فایل‌های غیرضروری
echo 🧹 حذف فایل‌های غیرضروری...
cd /d "%EXPORT_DIR%"

REM حذف فایل‌های Python cache
for /r %%f in (*.pyc) do del "%%f" >nul 2>&1
for /d /r %%d in (__pycache__) do rmdir /s /q "%%d" >nul 2>&1

REM حذف فایل‌های .pyo
for /r %%f in (*.pyo) do del "%%f" >nul 2>&1

REM حذف فایل‌های Thumbs.db
for /r %%f in (Thumbs.db) do del "%%f" >nul 2>&1

REM حذف فایل‌های .env (اگر وجود دارد)
if exist ".env" (
    del ".env" >nul
    echo ⚠️  فایل .env حذف شد (برای امنیت)
)

REM حذف پوشه venv (اگر وجود دارد)
if exist "venv" (
    rmdir /s /q "venv" >nul
    echo ⚠️  پوشه venv حذف شد
)

REM حذف فایل‌های لاگ
for /r %%f in (*.log) do del "%%f" >nul 2>&1

REM حذف فایل‌های موقت
for /r %%f in (*.tmp) do del "%%f" >nul 2>&1
for /r %%f in (*.temp) do del "%%f" >nul 2>&1

REM بازگشت به دایرکتوری اصلی
cd /d "%CURRENT_DIR%"

REM ایجاد فایل .gitignore برای پروژه خروجی
echo # Byte-compiled / optimized / DLL files > "%EXPORT_DIR%\.gitignore"
echo __pycache__/ >> "%EXPORT_DIR%\.gitignore"
echo *.py[cod] >> "%EXPORT_DIR%\.gitignore"
echo *$py.class >> "%EXPORT_DIR%\.gitignore"
echo. >> "%EXPORT_DIR%\.gitignore"
echo # C extensions >> "%EXPORT_DIR%\.gitignore"
echo *.so >> "%EXPORT_DIR%\.gitignore"
echo. >> "%EXPORT_DIR%\.gitignore"
echo # Distribution / packaging >> "%EXPORT_DIR%\.gitignore"
echo .Python >> "%EXPORT_DIR%\.gitignore"
echo build/ >> "%EXPORT_DIR%\.gitignore"
echo develop-eggs/ >> "%EXPORT_DIR%\.gitignore"
echo dist/ >> "%EXPORT_DIR%\.gitignore"
echo downloads/ >> "%EXPORT_DIR%\.gitignore"
echo eggs/ >> "%EXPORT_DIR%\.gitignore"
echo .eggs/ >> "%EXPORT_DIR%\.gitignore"
echo lib/ >> "%EXPORT_DIR%\.gitignore"
echo lib64/ >> "%EXPORT_DIR%\.gitignore"
echo parts/ >> "%EXPORT_DIR%\.gitignore"
echo sdist/ >> "%EXPORT_DIR%\.gitignore"
echo var/ >> "%EXPORT_DIR%\.gitignore"
echo wheels/ >> "%EXPORT_DIR%\.gitignore"
echo *.egg-info/ >> "%EXPORT_DIR%\.gitignore"
echo .installed.cfg >> "%EXPORT_DIR%\.gitignore"
echo *.egg >> "%EXPORT_DIR%\.gitignore"
echo MANIFEST >> "%EXPORT_DIR%\.gitignore"
echo. >> "%EXPORT_DIR%\.gitignore"
echo # Environments >> "%EXPORT_DIR%\.gitignore"
echo .env >> "%EXPORT_DIR%\.gitignore"
echo .venv >> "%EXPORT_DIR%\.gitignore"
echo env/ >> "%EXPORT_DIR%\.gitignore"
echo venv/ >> "%EXPORT_DIR%\.gitignore"
echo ENV/ >> "%EXPORT_DIR%\.gitignore"
echo env.bak/ >> "%EXPORT_DIR%\.gitignore"
echo venv.bak/ >> "%EXPORT_DIR%\.gitignore"
echo. >> "%EXPORT_DIR%\.gitignore"
echo # IDE >> "%EXPORT_DIR%\.gitignore"
echo .vscode/ >> "%EXPORT_DIR%\.gitignore"
echo .idea/ >> "%EXPORT_DIR%\.gitignore"
echo *.swp >> "%EXPORT_DIR%\.gitignore"
echo *.swo >> "%EXPORT_DIR%\.gitignore"
echo *~ >> "%EXPORT_DIR%\.gitignore"
echo. >> "%EXPORT_DIR%\.gitignore"
echo # OS >> "%EXPORT_DIR%\.gitignore"
echo .DS_Store >> "%EXPORT_DIR%\.gitignore"
echo .DS_Store? >> "%EXPORT_DIR%\.gitignore"
echo ._* >> "%EXPORT_DIR%\.gitignore"
echo .Spotlight-V100 >> "%EXPORT_DIR%\.gitignore"
echo .Trashes >> "%EXPORT_DIR%\.gitignore"
echo ehthumbs.db >> "%EXPORT_DIR%\.gitignore"
echo Thumbs.db >> "%EXPORT_DIR%\.gitignore"
echo. >> "%EXPORT_DIR%\.gitignore"
echo # Project specific >> "%EXPORT_DIR%\.gitignore"
echo media/ >> "%EXPORT_DIR%\.gitignore"
echo staticfiles/ >> "%EXPORT_DIR%\.gitignore"
echo *.sql >> "%EXPORT_DIR%\.gitignore"
echo *.sqlite3 >> "%EXPORT_DIR%\.gitignore"

REM ایجاد فایل راهنمای نصب سریع
echo # راهنمای نصب سریع DjangoCraft > "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ## پیش‌نیازها >> "%EXPORT_DIR%\QUICK_START.md"
echo - Python 3.8+ >> "%EXPORT_DIR%\QUICK_START.md"
echo - PostgreSQL >> "%EXPORT_DIR%\QUICK_START.md"
echo - pip >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ## نصب سریع >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ### 1. ایجاد محیط مجازی >> "%EXPORT_DIR%\QUICK_START.md"
echo ```bash >> "%EXPORT_DIR%\QUICK_START.md"
echo python -m venv venv >> "%EXPORT_DIR%\QUICK_START.md"
echo venv\Scripts\activate >> "%EXPORT_DIR%\QUICK_START.md"
echo ``` >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ### 2. نصب وابستگی‌ها >> "%EXPORT_DIR%\QUICK_START.md"
echo ```bash >> "%EXPORT_DIR%\QUICK_START.md"
echo pip install -r requirements.txt >> "%EXPORT_DIR%\QUICK_START.md"
echo ``` >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ### 3. تنظیم پایگاه داده >> "%EXPORT_DIR%\QUICK_START.md"
echo ```bash >> "%EXPORT_DIR%\QUICK_START.md"
echo copy env_example.txt .env >> "%EXPORT_DIR%\QUICK_START.md"
echo REM ویرایش فایل .env با تنظیمات پایگاه داده >> "%EXPORT_DIR%\QUICK_START.md"
echo ``` >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ### 4. اجرای مایگریشن‌ها >> "%EXPORT_DIR%\QUICK_START.md"
echo ```bash >> "%EXPORT_DIR%\QUICK_START.md"
echo python manage.py migrate >> "%EXPORT_DIR%\QUICK_START.md"
echo ``` >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ### 5. ایجاد کاربر ادمین >> "%EXPORT_DIR%\QUICK_START.md"
echo ```bash >> "%EXPORT_DIR%\QUICK_START.md"
echo python manage.py createsuperuser >> "%EXPORT_DIR%\QUICK_START.md"
echo ``` >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ### 6. اجرای سرور >> "%EXPORT_DIR%\QUICK_START.md"
echo ```bash >> "%EXPORT_DIR%\QUICK_START.md"
echo python manage.py runserver >> "%EXPORT_DIR%\QUICK_START.md"
echo ``` >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ## استفاده از Docker >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ### اجرای کامل با Docker Compose >> "%EXPORT_DIR%\QUICK_START.md"
echo ```bash >> "%EXPORT_DIR%\QUICK_START.md"
echo docker-compose up -d >> "%EXPORT_DIR%\QUICK_START.md"
echo ``` >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ## دسترسی >> "%EXPORT_DIR%\QUICK_START.md"
echo - وب‌سایت: http://localhost:8000 >> "%EXPORT_DIR%\QUICK_START.md"
echo - ادمین: http://localhost:8000/admin >> "%EXPORT_DIR%\QUICK_START.md"
echo. >> "%EXPORT_DIR%\QUICK_START.md"
echo ## پشتیبانی >> "%EXPORT_DIR%\QUICK_START.md"
echo برای اطلاعات بیشتر، فایل `deployment_guide.md` را مطالعه کنید. >> "%EXPORT_DIR%\QUICK_START.md"

REM ایجاد فایل ZIP (اگر PowerShell در دسترس باشد)
echo 📦 ایجاد فایل ZIP...
powershell -Command "Compress-Archive -Path '%EXPORT_DIR%' -DestinationPath '%EXPORT_DIR%.zip' -Force" >nul 2>&1

REM نمایش اطلاعات نهایی
echo.
echo ✅ خروجی گرفتن از پروژه با موفقیت انجام شد!
echo.
echo 📁 دایرکتوری خروجی: %EXPORT_DIR%
echo 📦 فایل ZIP: %EXPORT_DIR%.zip
echo.
echo 📋 محتویات خروجی:
echo    - کد کامل پروژه
echo    - فایل‌های Docker
echo    - راهنمای نصب سریع
echo    - فایل .gitignore
echo    - فایل‌های پیکربندی
echo.
echo 🚀 برای شروع:
echo    1. فایل ZIP را استخراج کنید
echo    2. فایل QUICK_START.md را مطالعه کنید
echo    3. مراحل نصب را دنبال کنید
echo.
echo 📖 برای اطلاعات بیشتر: deployment_guide.md را مطالعه کنید
echo.
pause
