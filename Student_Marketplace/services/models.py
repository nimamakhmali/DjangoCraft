from django.db import models


class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)

	def __str__(self) -> str:
		return self.name


class Service(models.Model):
	title = models.CharField(max_length=150)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services', null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return self.title
