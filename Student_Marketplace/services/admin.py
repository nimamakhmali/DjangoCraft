from django.contrib import admin
from .models import Category, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "price", "category")
	list_filter = ("category",)
	search_fields = ("title",)
