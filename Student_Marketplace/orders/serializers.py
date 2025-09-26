from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
	line_total = serializers.SerializerMethodField()

	class Meta:
		model = OrderItem
		fields = ["id", "service_title", "unit_price", "quantity", "line_total"]

	def get_line_total(self, obj):
		return float(obj.unit_price) * obj.quantity


class OrderSerializer(serializers.ModelSerializer):
	items = OrderItemSerializer(many=True, read_only=True)

	class Meta:
		model = Order
		fields = ["id", "status", "total_amount", "created_at", "items"]


class OrderCreateItemSerializer(serializers.Serializer):
	title = serializers.CharField(max_length=150)
	price = serializers.DecimalField(max_digits=10, decimal_places=2)
	qty = serializers.IntegerField(min_value=1, default=1)


class OrderCreateSerializer(serializers.Serializer):
	items = OrderCreateItemSerializer(many=True)
