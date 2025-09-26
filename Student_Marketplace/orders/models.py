from django.db import models


class Order(models.Model):
	STATUS_PENDING = 'pending'
	STATUS_PAID = 'paid'
	STATUS_REFUNDED = 'refunded'
	STATUS_CHOICES = [
		(STATUS_PENDING, 'Pending'),
		(STATUS_PAID, 'Paid'),
		(STATUS_REFUNDED, 'Refunded'),
	]

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

	def __str__(self) -> str:
		return f"Order #{self.pk} - {self.status}"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	service_title = models.CharField(max_length=150)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self) -> str:
		return f"{self.service_title} x{self.quantity}"

	@property
	def line_total(self):
		return self.unit_price * self.quantity
