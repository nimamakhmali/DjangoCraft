from rest_framework import serializers
from .models import Category, Service


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ["id", "name", "description"]


class ServiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Service
		fields = ["id", "title", "description", "price", "category"]
