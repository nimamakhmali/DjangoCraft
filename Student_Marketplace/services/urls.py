from django.urls import path
from .views import list_services, list_categories, list_services_db

urlpatterns = [
	path('', list_services, name='services-list'),
	path('categories/', list_categories, name='services-categories'),
	path('list/', list_services_db, name='services-list-db'),
]
