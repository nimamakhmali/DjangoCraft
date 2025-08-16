# راهنمای استقرار و خروجی گرفتن از DjangoCraft

## 📋 فهرست مطالب
1. [پیش‌نیازها](#پیشنیازها)
2. [آماده‌سازی پروژه](#آمادهسازی-پروژه)
3. [استقرار محلی](#استقرار-محلی)
4. [استقرار روی سرور](#استقرار-روی-سرور)
5. [پشتیبان‌گیری](#پشتیبانیگیری)
6. [مشکلات رایج](#مشکلات-رایج)

## پیش‌نیازها

### نرم‌افزارهای مورد نیاز:
- Python 3.8 یا بالاتر
- PostgreSQL 12 یا بالاتر
- Git
- pip (مدیر بسته‌های Python)

### پکیج‌های Python:
```
asgiref==3.9.1
Django==5.2.5
pillow==11.3.0
psycopg2-binary==2.9.10
python-dotenv==1.1.1
sqlparse==0.5.3
tzdata==2025.2
```

## آماده‌سازی پروژه

### 1. کپی کردن پروژه
```bash
# کپی کردن پروژه به مسیر مورد نظر
cp -r DjangoCraft /path/to/destination/
cd /path/to/destination/DjangoCraft
```

### 2. ایجاد محیط مجازی
```bash
# ایجاد محیط مجازی
python -m venv venv

# فعال‌سازی محیط مجازی
# در Windows:
venv\Scripts\activate
# در Linux/Mac:
source venv/bin/activate
```

### 3. نصب وابستگی‌ها
```bash
pip install -r requirements.txt
```

### 4. تنظیم متغیرهای محیطی
```bash
# کپی کردن فایل نمونه
cp env_example.txt .env

# ویرایش فایل .env با تنظیمات مناسب
```

### محتوای فایل .env:
```env
# Database Configuration
DB_NAME=project_manager_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=False  # برای تولید
ALLOWED_HOSTS=your-domain.com,localhost,127.0.0.1
```

## استقرار محلی

### 1. راه‌اندازی پایگاه داده
```bash
# ایجاد پایگاه داده PostgreSQL
createdb project_manager_db

# یا از طریق pgAdmin
```

### 2. اجرای مایگریشن‌ها
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. ایجاد کاربر ادمین
```bash
python manage.py createsuperuser
```

### 4. جمع‌آوری فایل‌های استاتیک
```bash
python manage.py collectstatic
```

### 5. اجرای سرور
```bash
python manage.py runserver
```

## استقرار روی سرور

### گزینه 1: استقرار با Gunicorn + Nginx

#### نصب Gunicorn:
```bash
pip install gunicorn
```

#### فایل gunicorn.conf.py:
```python
bind = "127.0.0.1:8000"
workers = 3
timeout = 120
```

#### فایل Nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/DjangoCraft/staticfiles/;
    }

    location /media/ {
        alias /path/to/DjangoCraft/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### گزینه 2: استقرار با Docker

#### Dockerfile:
```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project_manager.wsgi:application"]
```

#### docker-compose.yml:
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DB_HOST=db
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=project_manager_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## پشتیبان‌گیری

### 1. پشتیبان‌گیری از پایگاه داده
```bash
# پشتیبان‌گیری کامل
pg_dump project_manager_db > backup_$(date +%Y%m%d_%H%M%S).sql

# پشتیبان‌گیری فقط داده‌ها
pg_dump --data-only project_manager_db > data_backup_$(date +%Y%m%d_%H%M%S).sql
```

### 2. پشتیبان‌گیری از فایل‌های مدیا
```bash
# کپی کردن پوشه media
cp -r media/ backup_media_$(date +%Y%m%d_%H%M%S)/
```

### 3. اسکریپت پشتیبان‌گیری خودکار
```bash
#!/bin/bash
# backup_script.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/path/to/backups"

# ایجاد پوشه پشتیبان
mkdir -p $BACKUP_DIR

# پشتیبان‌گیری از پایگاه داده
pg_dump project_manager_db > $BACKUP_DIR/db_backup_$DATE.sql

# پشتیبان‌گیری از فایل‌های مدیا
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz media/

# حذف پشتیبان‌های قدیمی (بیش از 30 روز)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

## مشکلات رایج

### 1. خطای اتصال به پایگاه داده
```bash
# بررسی وضعیت PostgreSQL
sudo systemctl status postgresql

# راه‌اندازی مجدد
sudo systemctl restart postgresql
```

### 2. خطای مجوز فایل‌ها
```bash
# تنظیم مجوزهای مناسب
chmod 755 /path/to/DjangoCraft
chmod 644 /path/to/DjangoCraft/.env
```

### 3. خطای فایل‌های استاتیک
```bash
# جمع‌آوری مجدد فایل‌های استاتیک
python manage.py collectstatic --clear --noinput
```

### 4. خطای مایگریشن
```bash
# بازنشانی مایگریشن‌ها
python manage.py migrate --fake-initial
```

## نکات امنیتی

1. **تغییر SECRET_KEY**: حتماً SECRET_KEY پیش‌فرض را تغییر دهید
2. **غیرفعال کردن DEBUG**: در محیط تولید DEBUG=False تنظیم کنید
3. **تنظیم ALLOWED_HOSTS**: فقط دامنه‌های مجاز را اضافه کنید
4. **استفاده از HTTPS**: در محیط تولید حتماً از SSL استفاده کنید
5. **پشتیبان‌گیری منظم**: برنامه‌ریزی پشتیبان‌گیری خودکار

## تماس و پشتیبانی

برای سوالات و مشکلات:
- بررسی لاگ‌های Django: `python manage.py runserver --verbosity=2`
- بررسی لاگ‌های سرور: `/var/log/nginx/error.log`
- بررسی لاگ‌های PostgreSQL: `/var/log/postgresql/postgresql-*.log`
