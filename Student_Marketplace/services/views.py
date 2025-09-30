from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import status
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Sum
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
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
	services = Service.objects.select_related("category").filter(status=Service.STATUS_APPROVED)
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


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def service_detail(request, service_id):
	try:
		service = Service.objects.get(pk=service_id)
	except Service.DoesNotExist:
		return Response({"detail": "Not found"}, status=404)
	
	# Check ownership for update/delete
	if request.method in ['PUT', 'DELETE']:
		if not hasattr(request.user, 'profile') or request.user.profile.role != 'freelancer':
			return Response({"detail": "Only freelancers can modify services"}, status=403)
		# In a real app, you'd check if service.owner == request.user
	
	if request.method == "GET":
		return Response(ServiceSerializer(service).data)
	elif request.method == "PUT":
		serializer = ServiceSerializer(service, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		service = serializer.save()
		return Response(ServiceSerializer(service).data)
	elif request.method == "DELETE":
		service.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def services_search(request):
	# Search and filter services
	queryset = Service.objects.select_related('category').filter(status=Service.STATUS_APPROVED)
	
	# Filter by category
	category_id = request.GET.get('category')
	if category_id:
		queryset = queryset.filter(category_id=category_id)
	
	# Search in title and description
	search = request.GET.get('search')
	if search:
		queryset = queryset.filter(
			Q(title__icontains=search) | Q(description__icontains=search)
		)
	
	# Price range
	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')
	if min_price:
		queryset = queryset.filter(price__gte=min_price)
	if max_price:
		queryset = queryset.filter(price__lte=max_price)
	
	# Pagination
	page_size = int(request.GET.get('page_size', 10))
	page = int(request.GET.get('page', 1))
	
	paginator = Paginator(queryset, page_size)
	page_obj = paginator.get_page(page)
	
	serializer = ServiceSerializer(page_obj, many=True)
	
	return Response({
		'results': serializer.data,
		'count': paginator.count,
		'page': page,
		'num_pages': paginator.num_pages,
		'has_next': page_obj.has_next(),
		'has_previous': page_obj.has_previous(),
	})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_summary(request):
	# Staff-only guard
	if not request.user.is_staff:
		return Response({"detail": "Admins only"}, status=403)

	services_qs = Service.objects.all()
	data = {
		"users_total": User.objects.count(),
		"services_total": services_qs.count(),
		"services_pending": services_qs.filter(status=Service.STATUS_PENDING).count(),
		"services_approved": services_qs.filter(status=Service.STATUS_APPROVED).count(),
		"services_rejected": services_qs.filter(status=Service.STATUS_REJECTED).count(),
	}

	try:
		from payments.models import Payment
		revenue = Payment.objects.filter(status=Payment.STATUS_COMPLETED).aggregate(total=Sum('amount'))['total'] or 0
		data.update({
			"payments_total": Payment.objects.count(),
			"payments_completed": Payment.objects.filter(status=Payment.STATUS_COMPLETED).count(),
			"revenue_total": float(revenue),
		})
	except Exception:
		# payments app may not be fully configured
		data.update({
			"payments_total": 0,
			"payments_completed": 0,
			"revenue_total": 0.0,
		})

	return Response(data)
