from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = [
			'payment_id', 'external_id', 'amount', 'currency', 'status',
			'gateway', 'payment_method', 'last_four_digits',
			'created_at', 'updated_at', 'completed_at'
		]
		read_only_fields = [
			'payment_id', 'external_id', 'status', 'gateway_response',
			'created_at', 'updated_at', 'completed_at'
		]


class PaymentCreateSerializer(serializers.Serializer):
	order_id = serializers.IntegerField()
	payment_method = serializers.CharField(max_length=50, default='mock')
	
	def validate_order_id(self, value):
		# In a real app, you'd check if order belongs to user and is in correct state
		from orders.models import Order
		try:
			order = Order.objects.get(pk=value)
		except Order.DoesNotExist:
			raise serializers.ValidationError("Order not found")
		
		# Check if order already has a payment
		if hasattr(order, 'payment'):
			raise serializers.ValidationError("Order already has a payment")
		
		return value


class PaymentConfirmSerializer(serializers.Serializer):
	payment_id = serializers.UUIDField()
	confirmation_code = serializers.CharField(max_length=100)
	
	def validate_payment_id(self, value):
		try:
			payment = Payment.objects.get(payment_id=value)
		except Payment.DoesNotExist:
			raise serializers.ValidationError("Payment not found")
		
		if not payment.is_pending:
			raise serializers.ValidationError("Payment is not in pending state")
		
		return value
