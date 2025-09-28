from django.urls import path
from .views import initiate_payment, confirm_payment, payment_status, mock_webhook

urlpatterns = [
	path('initiate/', initiate_payment, name='payments-initiate'),
	path('confirm/', confirm_payment, name='payments-confirm'),
	path('<uuid:payment_id>/status/', payment_status, name='payments-status'),
	path('webhook/mock/', mock_webhook, name='payments-webhook-mock'),
]
