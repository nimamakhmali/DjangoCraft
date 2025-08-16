#!/bin/bash

# اسکریپت خروجی گرفتن از پروژه DjangoCraft
# این اسکریپت پروژه را برای انتقال آماده می‌کند

set -e  # توقف در صورت خطا

echo "🚀 شروع خروجی گرفتن از پروژه DjangoCraft..."

# تنظیم متغیرها
PROJECT_NAME="DjangoCraft"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
EXPORT_DIR="${PROJECT_NAME}_export_${TIMESTAMP}"
CURRENT_DIR=$(pwd)

# ایجاد دایرکتوری خروجی
echo "📁 ایجاد دایرکتوری خروجی: $EXPORT_DIR"
mkdir -p "$EXPORT_DIR"

# کپی کردن فایل‌های اصلی پروژه
echo "📋 کپی کردن فایل‌های پروژه..."
cp -r core/ "$EXPORT_DIR/"
cp -r project_manager/ "$EXPORT_DIR/"
cp manage.py "$EXPORT_DIR/"
cp requirements.txt "$EXPORT_DIR/"
cp README.md "$EXPORT_DIR/"
cp LICENSE "$EXPORT_DIR/"
cp env_example.txt "$EXPORT_DIR/"

# کپی کردن فایل‌های Docker (اگر وجود دارند)
if [ -f "Dockerfile" ]; then
    cp Dockerfile "$EXPORT_DIR/"
fi

if [ -f "docker-compose.yml" ]; then
    cp docker-compose.yml "$EXPORT_DIR/"
fi

if [ -f "nginx.conf" ]; then
    cp nginx.conf "$EXPORT_DIR/"
fi

# کپی کردن فایل‌های اضافی
if [ -f "deployment_guide.md" ]; then
    cp deployment_guide.md "$EXPORT_DIR/"
fi

# حذف فایل‌های غیرضروری
echo "🧹 حذف فایل‌های غیرضروری..."
cd "$EXPORT_DIR"

# حذف فایل‌های Python cache
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# حذف فایل‌های .pyo
find . -type f -name "*.pyo" -delete

# حذف فایل‌های .DS_Store (macOS)
find . -type f -name ".DS_Store" -delete

# حذف فایل‌های Thumbs.db (Windows)
find . -type f -name "Thumbs.db" -delete

# حذف فایل‌های .env (اگر وجود دارد)
if [ -f ".env" ]; then
    rm .env
    echo "⚠️  فایل .env حذف شد (برای امنیت)"
fi

# حذف پوشه venv (اگر وجود دارد)
if [ -d "venv" ]; then
    rm -rf venv
    echo "⚠️  پوشه venv حذف شد"
fi

# حذف فایل‌های لاگ
find . -type f -name "*.log" -delete

# حذف فایل‌های موقت
find . -type f -name "*.tmp" -delete
find . -type f -name "*.temp" -delete

# بازگشت به دایرکتوری اصلی
cd "$CURRENT_DIR"

# ایجاد فایل .gitignore برای پروژه خروجی
cat > "$EXPORT_DIR/.gitignore" << 'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
media/
staticfiles/
*.sql
*.sqlite3
EOF

# ایجاد فایل راهنمای نصب سریع
cat > "$EXPORT_DIR/QUICK_START.md" << 'EOF'
# راهنمای نصب سریع DjangoCraft

## پیش‌نیازها
- Python 3.8+
- PostgreSQL
- pip

## نصب سریع

### 1. ایجاد محیط مجازی
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate     # Windows
```

### 2. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### 3. تنظیم پایگاه داده
```bash
# کپی کردن فایل محیط
cp env_example.txt .env
# ویرایش فایل .env با تنظیمات پایگاه داده
```

### 4. اجرای مایگریشن‌ها
```bash
python manage.py migrate
```

### 5. ایجاد کاربر ادمین
```bash
python manage.py createsuperuser
```

### 6. اجرای سرور
```bash
python manage.py runserver
```

## استفاده از Docker

### اجرای کامل با Docker Compose
```bash
docker-compose up -d
```

### فقط پایگاه داده
```bash
docker-compose up -d db
```

## دسترسی
- وب‌سایت: http://localhost:8000
- ادمین: http://localhost:8000/admin

## پشتیبانی
برای اطلاعات بیشتر، فایل `deployment_guide.md` را مطالعه کنید.
EOF

# ایجاد فایل ZIP
echo "📦 ایجاد فایل ZIP..."
zip -r "${EXPORT_DIR}.zip" "$EXPORT_DIR"

# نمایش اطلاعات نهایی
echo ""
echo "✅ خروجی گرفتن از پروژه با موفقیت انجام شد!"
echo ""
echo "📁 دایرکتوری خروجی: $EXPORT_DIR"
echo "📦 فایل ZIP: ${EXPORT_DIR}.zip"
echo ""
echo "📋 محتویات خروجی:"
echo "   - کد کامل پروژه"
echo "   - فایل‌های Docker"
echo "   - راهنمای نصب سریع"
echo "   - فایل .gitignore"
echo "   - فایل‌های پیکربندی"
echo ""
echo "🚀 برای شروع:"
echo "   1. فایل ZIP را استخراج کنید"
echo "   2. فایل QUICK_START.md را مطالعه کنید"
echo "   3. مراحل نصب را دنبال کنید"
echo ""
echo "📖 برای اطلاعات بیشتر: deployment_guide.md را مطالعه کنید"
