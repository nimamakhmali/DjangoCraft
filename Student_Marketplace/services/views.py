from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .models import Category, Service
from .serializers import CategorySerializer, ServiceSerializer


@api_view(["GET"])
def list_services(_request):
    return Response({"services": []})


@api_view(["GET"])
def list_categories(_request):
	categories = Category.objects.all()
	return Response({"categories": CategorySerializer(categories, many=True).data})


@api_view(["GET"])
def list_services_db(_request):
	services = Service.objects.select_related("category").all()
	return Response({"services": ServiceSerializer(services, many=True).data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_service(request):
	# Require freelancer role to create a service
	if not hasattr(request.user, 'profile') or request.user.profile.role != 'freelancer':
		return Response({"detail": "Only freelancers can create services"}, status=403)
	serializer = ServiceSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	service = serializer.save()
	return Response(ServiceSerializer(service).data, status=201)
