from django.urls import path
from .views import list_services

urlpatterns = [
	path('', list_services, name='services-list'),
]
