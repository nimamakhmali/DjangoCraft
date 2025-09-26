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
