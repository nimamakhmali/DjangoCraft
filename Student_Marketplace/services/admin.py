from django.contrib import admin
from .models import Category, Service
from django.utils import timezone


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name")
	search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "price", "category", "status", "approved_at")
	list_filter = ("category", "status")
	search_fields = ("title",)
	actions = ("approve_services", "reject_services", "mark_pending",)
	readonly_fields = ("approved_at", "approved_by")

	def approve_services(self, request, queryset):
		updated = queryset.update(status=Service.STATUS_APPROVED, approved_at=timezone.now(), approved_by=request.user, rejection_reason="")
		self.message_user(request, f"Approved {updated} services")
	approve_services.short_description = "Approve selected services"

	def reject_services(self, request, queryset):
		updated = queryset.update(status=Service.STATUS_REJECTED, approved_at=None, approved_by=request.user)
		self.message_user(request, f"Rejected {updated} services")
	reject_services.short_description = "Reject selected services"

	def mark_pending(self, request, queryset):
		updated = queryset.update(status=Service.STATUS_PENDING, approved_at=None, approved_by=None)
		self.message_user(request, f"Moved {updated} services to pending")
	mark_pending.short_description = "Mark selected services as pending"
