from django.urls import path
from .views import service_reviews, create_review, review_detail

urlpatterns = [
	path('service/<int:service_id>/', service_reviews, name='reviews-service-list'),
	path('service/<int:service_id>/create/', create_review, name='reviews-create'),
	path('<int:review_id>/', review_detail, name='reviews-detail'),
]
