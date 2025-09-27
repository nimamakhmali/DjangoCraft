from django.urls import path
from .views import create_order, order_detail, user_orders, update_order_status

urlpatterns = [
	path('create/', create_order, name='orders-create'),
	path('my-orders/', user_orders, name='orders-user-list'),
	path('<int:order_id>/', order_detail, name='orders-detail'),
	path('<int:order_id>/status/', update_order_status, name='orders-update-status'),
]
