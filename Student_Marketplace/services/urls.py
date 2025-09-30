from django.urls import path
from .views import list_services, list_categories, list_services_db, create_service, service_detail, services_search, admin_summary

urlpatterns = [
	path('', list_services, name='services-list'),
	path('categories/', list_categories, name='services-categories'),
	path('list/', list_services_db, name='services-list-db'),
	path('search/', services_search, name='services-search'),
	path('create/', create_service, name='services-create'),
	path('<int:service_id>/', service_detail, name='services-detail'),
	# admin/reporting
	path('admin/summary/', admin_summary, name='services-admin-summary'),
]
