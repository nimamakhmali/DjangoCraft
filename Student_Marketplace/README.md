# 🎓 Student Marketplace (Services for Students)

A Django REST backend powering a student-focused services marketplace: listings, messaging, orders, and payments (mock/Stripe-ready). Frontend is a separate Vite/React app under `frontend/` and connects via `/api`.

## Features
- Auth: signup/login, profile, password change, email verification (console)
- Services: categories, list/search, CRUD for freelancers, admin summary
- Orders: create order with items, list my orders, update status
- Messaging: conversations, messages with attachments, notifications, unread counts
- Reviews: create/edit/delete, list with average rating
- Payments: mock flow (initiate/confirm), Stripe test-mode ready
- API docs: OpenAPI (`/api/schema/`), Swagger UI (`/api/docs/`)

## Prerequisites
- Python 3.11+ (tested on Windows 10 PowerShell)
- Node 18+ (for the separate frontend app)

## Backend: Run locally
```powershell
cd Student_Marketplace
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create .env (you can also copy env_example.txt)
@"
SECRET_KEY=dev-secret-key-123
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOW_ALL_ORIGINS=True
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=no-reply@example.com
STRIPE_ENABLED=False
"@ | Out-File -FilePath .env -Encoding utf8

python manage.py migrate
python manage.py runserver 127.0.0.1:8000

# Health check
curl http://127.0.0.1:8000/health/
```

### Create a superuser (optional, for admin summary)
```powershell
python manage.py createsuperuser
```

## Frontend (optional but recommended)
The Vite/React app proxies `/api` to Django in dev.
```powershell
cd ..\frontend
npm install
npm run dev
# Open the shown localhost URL
```

### Quick demo flow (mock payments)
1) In the frontend header, click Signup, then Login.
2) Go to Services and click Quick Buy on an item.
3) A confirmation code (mock) is provided; confirm to complete payment.
4) Visit Admin (needs staff user) for KPIs, or Messaging for conversations.

## API Endpoints (highlights)
- Accounts: `/api/accounts/` (signup, token, me, logout, verify)
- Services: `/api/services/` (list, search, create, detail, admin/summary)
- Orders: `/api/orders/` (create, my-orders, detail, status)
- Payments: `/api/payments/` (initiate, confirm, status, webhook/mock)
- Messaging: `/api/messaging/` (conversations/messages/notifications)
- Reviews: `/api/reviews/` (service reviews CRUD)

## Stripe test-mode (optional)
Set in `.env` then restart:
```
STRIPE_ENABLED=True
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_SUCCESS_URL=http://localhost:5173/success
STRIPE_CANCEL_URL=http://localhost:5173/cancel
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

## Notes
- Email verification uses console backend; tokens appear in server logs.
- SQLite is used by default; switch `DATABASES` in `marketplace/settings.py` as needed.

## License
See `LICENSE` in repo root.
