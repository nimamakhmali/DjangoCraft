from django.http import JsonResponse
from .models import Category, Service


def list_services(_request):
    return JsonResponse({"services": []})


def list_categories(_request):
	categories = list(Category.objects.values("id", "name"))
	return JsonResponse({"categories": categories})


def list_services_db(_request):
	services = list(Service.objects.values("id", "title", "price", "category_id"))
	return JsonResponse({"services": services})
