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

# Create your views here.
