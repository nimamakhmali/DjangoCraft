FROM python:3.9-slim

# تنظیم متغیرهای محیطی
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تنظیم دایرکتوری کاری
WORKDIR /app

# نصب وابستگی‌های سیستم
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# کپی کردن فایل requirements
COPY requirements.txt .

# نصب وابستگی‌های Python
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن کد پروژه
COPY . .

# ایجاد پوشه‌های مورد نیاز
RUN mkdir -p /app/staticfiles /app/media

# جمع‌آوری فایل‌های استاتیک
RUN python manage.py collectstatic --noinput

# ایجاد کاربر غیر root
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# پورت
EXPOSE 8000

# دستور اجرا
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "project_manager.wsgi:application"]
