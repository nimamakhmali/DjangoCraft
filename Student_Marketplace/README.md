# 🎓 Student Marketplace (Services for Students)

A Django-based marketplace for student-focused micro-services: small projects, consultations, short trainings, and digital deliverables.

## Features (MVP)
- Auth (Django built-in)
- Service listings and ordering
- Payments integration-ready (Stripe/PayPal placeholder)
- Reviews and ratings
- Basic recommendations (placeholder module)

## Quick Start
```bash
cd Student_Marketplace
python -m venv .venv
./.venv/Scripts/Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
cp env_example.txt .env
python manage.py migrate
python manage.py runserver
# Health check
curl http://localhost:8000/health/
```

## Environment
See `.env_example` for available variables.

## Tech Stack
- Django 4.2 LTS
- Django REST Framework
- django-environ, django-cors-headers

## Next
- Apps: accounts, services, orders, payments, reviews, recommendations, messaging
- Payment gateway integration
- Recommendation engine baseline
