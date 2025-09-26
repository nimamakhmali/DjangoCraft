from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	bio = models.TextField(blank=True)
	skills = models.TextField(blank=True)
	ROLE_CHOICES = [
		('student', 'Student'),
		('freelancer', 'Freelancer'),
		('admin', 'Admin'),
	]
	role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='student')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"Profile({self.user.username})"

# Create your models here.
