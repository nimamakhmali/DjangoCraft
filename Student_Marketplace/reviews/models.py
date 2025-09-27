from django.db import models
from django.contrib.auth.models import User
from services.models import Service


class Review(models.Model):
	RATING_CHOICES = [
		(1, '1 Star'),
		(2, '2 Stars'),
		(3, '3 Stars'),
		(4, '4 Stars'),
		(5, '5 Stars'),
	]
	
	service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
	rating = models.IntegerField(choices=RATING_CHOICES)
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	class Meta:
		unique_together = ['service', 'user']  # One review per user per service
	
	def __str__(self) -> str:
		return f"Review by {self.user.username} for {self.service.title} - {self.rating} stars"