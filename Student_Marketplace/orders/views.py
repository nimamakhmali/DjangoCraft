from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer


@require_POST
def create_order(request):
	# naive minimal create: expect JSON with items: [{title, price, qty}]
	data = request.POST or {}
	items = data.get('items') or []
	order = Order.objects.create()
	total = 0
	for item in items:
		title = item.get('title', 'Untitled')
		price = item.get('price', 0)
		qty = int(item.get('qty', 1))
		OrderItem.objects.create(order=order, service_title=title, unit_price=price, quantity=qty)
		total += float(price) * qty
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
