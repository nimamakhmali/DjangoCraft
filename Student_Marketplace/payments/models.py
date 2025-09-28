from django.db import models
from django.contrib.auth.models import User
from orders.models import Order
import uuid


class Payment(models.Model):
	STATUS_PENDING = 'pending'
	STATUS_PROCESSING = 'processing'
	STATUS_COMPLETED = 'completed'
	STATUS_FAILED = 'failed'
	STATUS_CANCELLED = 'cancelled'
	STATUS_REFUNDED = 'refunded'
	
	STATUS_CHOICES = [
		(STATUS_PENDING, 'Pending'),
		(STATUS_PROCESSING, 'Processing'),
		(STATUS_COMPLETED, 'Completed'),
		(STATUS_FAILED, 'Failed'),
		(STATUS_CANCELLED, 'Cancelled'),
		(STATUS_REFUNDED, 'Refunded'),
	]
	
	# Payment identification
	payment_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	external_id = models.CharField(max_length=100, blank=True)  # Gateway transaction ID
	
	# Relationships
	order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
	
	# Payment details
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	currency = models.CharField(max_length=3, default='USD')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	
	# Gateway info (for real integration)
	gateway = models.CharField(max_length=50, default='mock')  # 'stripe', 'paypal', 'mock'
	gateway_response = models.JSONField(blank=True, null=True)
	
	# Timestamps
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	completed_at = models.DateTimeField(blank=True, null=True)
	
	# Additional fields for real payment gateways
	payment_method = models.CharField(max_length=50, blank=True)  # 'card', 'paypal', etc.
	last_four_digits = models.CharField(max_length=4, blank=True)
	
	def __str__(self) -> str:
		return f"Payment {self.payment_id} - {self.status} - ${self.amount}"
	
	@property
	def is_successful(self):
		return self.status == self.STATUS_COMPLETED
	
	@property
	def is_pending(self):
		return self.status in [self.STATUS_PENDING, self.STATUS_PROCESSING]