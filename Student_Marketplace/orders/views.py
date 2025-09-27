from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer


@api_view(["POST"])
def create_order(request):
	serializer = OrderCreateSerializer(data=request.data)
	if not serializer.is_valid():
		return Response(serializer.errors, status=400)
	validated = serializer.validated_data
	order = Order.objects.create()
	total = 0
	for item in validated['items']:
		OrderItem.objects.create(
			order=order,
			service_title=item['title'],
			unit_price=item['price'],
			quantity=item['qty'],
		)
		total += float(item['price']) * item['qty']
	order.total_amount = total
	order.save(update_fields=['total_amount'])
	return Response({"order_id": order.id, "status": order.status, "total": float(order.total_amount)})


@api_view(["GET"])
def order_detail(_request, order_id: int):
	try:
		order = Order.objects.prefetch_related('items').get(pk=order_id)
	except Order.DoesNotExist:
		return Response({"detail": "Not found"}, status=404)
	return Response(OrderSerializer(order).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_orders(request):
	# List orders for the authenticated user
	# In a real app, you'd filter by user: Order.objects.filter(user=request.user)
	orders = Order.objects.prefetch_related('items').all()
	
	# Pagination
	page_size = int(request.GET.get('page_size', 10))
	page = int(request.GET.get('page', 1))
	
	from django.core.paginator import Paginator
	paginator = Paginator(orders, page_size)
	page_obj = paginator.get_page(page)
	
	serializer = OrderSerializer(page_obj, many=True)
	
	return Response({
		'results': serializer.data,
		'count': paginator.count,
		'page': page,
		'num_pages': paginator.num_pages,
		'has_next': page_obj.has_next(),
		'has_previous': page_obj.has_previous(),
	})


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
	try:
		order = Order.objects.get(pk=order_id)
	except Order.DoesNotExist:
		return Response({"detail": "Not found"}, status=404)
	
	# In a real app, you'd check if order.user == request.user or user is admin
	new_status = request.data.get('status')
	if new_status not in [choice[0] for choice in Order.STATUS_CHOICES]:
		return Response({"detail": "Invalid status"}, status=400)
	
	order.status = new_status
	order.save(update_fields=['status'])
	
	return Response(OrderSerializer(order).data)

# Create your views here.
