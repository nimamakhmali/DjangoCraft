from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import uuid
import random
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer, PaymentConfirmSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
	"""Initiate a payment for an order (Mock implementation)"""
	serializer = PaymentCreateSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	
	order_id = serializer.validated_data['order_id']
	payment_method = serializer.validated_data['payment_method']
	
	# Get the order
	from orders.models import Order
	order = Order.objects.get(pk=order_id)
	
	# Create payment record
	payment = Payment.objects.create(
		order=order,
		user=request.user,
		amount=order.total_amount,
		currency='USD',
		gateway='mock',
		payment_method=payment_method,
		status=Payment.STATUS_PENDING
	)
	
	# Mock gateway response
	payment.external_id = f"mock_{payment.payment_id.hex[:8]}"
	payment.gateway_response = {
		"gateway": "mock",
		"status": "initiated",
		"redirect_url": f"/mock-payment/{payment.payment_id}/",
		"confirmation_code": f"CONF_{random.randint(1000, 9999)}"
	}
	payment.save()
	
	return Response({
		"payment_id": str(payment.payment_id),
		"amount": float(payment.amount),
		"currency": payment.currency,
		"status": payment.status,
		"redirect_url": payment.gateway_response["redirect_url"],
		"confirmation_code": payment.gateway_response["confirmation_code"]
	}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_payment(request):
	"""Confirm a payment using confirmation code (Mock implementation)"""
	serializer = PaymentConfirmSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	
	payment_id = serializer.validated_data['payment_id']
	confirmation_code = serializer.validated_data['confirmation_code']
	
	payment = Payment.objects.get(payment_id=payment_id)
	
	# Mock payment confirmation logic
	# In real implementation, you'd call the payment gateway API
	expected_code = payment.gateway_response.get("confirmation_code")
	
	if confirmation_code == expected_code:
		# Simulate successful payment
		payment.status = Payment.STATUS_COMPLETED
		payment.completed_at = timezone.now()
		payment.gateway_response.update({
			"status": "completed",
			"transaction_id": f"TXN_{payment.external_id}",
			"confirmed_at": timezone.now().isoformat()
		})
		payment.save()
		
		# Update order status
		payment.order.status = payment.order.STATUS_PAID
		payment.order.save(update_fields=['status'])
		
		return Response({
			"payment_id": str(payment.payment_id),
			"status": payment.status,
			"transaction_id": payment.gateway_response["transaction_id"],
			"completed_at": payment.completed_at.isoformat()
		})
	else:
		# Simulate failed payment
		payment.status = Payment.STATUS_FAILED
		payment.gateway_response.update({
			"status": "failed",
			"error": "Invalid confirmation code"
		})
		payment.save()
		
		return Response({
			"payment_id": str(payment.payment_id),
			"status": payment.status,
			"error": "Invalid confirmation code"
		}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payment_status(request, payment_id):
	"""Get payment status"""
	try:
		payment = Payment.objects.get(payment_id=payment_id, user=request.user)
	except Payment.DoesNotExist:
		return Response({"detail": "Payment not found"}, status=404)
	
	return Response(PaymentSerializer(payment).data)


@api_view(["POST"])
def mock_webhook(request):
	"""Mock webhook endpoint for testing payment callbacks"""
	# This simulates a webhook from a payment gateway
	payment_id = request.data.get('payment_id')
	webhook_status = request.data.get('status')  # 'completed', 'failed', etc.
	
	if not payment_id or not webhook_status:
		return Response({"detail": "Missing payment_id or status"}, status=400)
	
	try:
		payment = Payment.objects.get(payment_id=payment_id)
	except Payment.DoesNotExist:
		return Response({"detail": "Payment not found"}, status=404)
	
	# Update payment based on webhook
	if webhook_status == 'completed':
		payment.status = Payment.STATUS_COMPLETED
		payment.completed_at = timezone.now()
		payment.order.status = payment.order.STATUS_PAID
		payment.order.save(update_fields=['status'])
	elif webhook_status == 'failed':
		payment.status = Payment.STATUS_FAILED
	elif webhook_status == 'cancelled':
		payment.status = Payment.STATUS_CANCELLED
	
	payment.save()
	
	return Response({
		"payment_id": str(payment.payment_id),
		"status": payment.status,
		"order_status": payment.order.status
	})