from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ('payment_id', 'user', 'order', 'amount', 'status', 'gateway', 'created_at')
	list_filter = ('status', 'gateway', 'created_at')
	search_fields = ('payment_id', 'external_id', 'user__username')
	readonly_fields = ('payment_id', 'created_at', 'updated_at', 'completed_at')
	
	fieldsets = (
		('Payment Info', {
			'fields': ('payment_id', 'external_id', 'order', 'user', 'amount', 'currency')
		}),
		('Status', {
			'fields': ('status', 'gateway', 'payment_method', 'last_four_digits')
		}),
		('Gateway Response', {
			'fields': ('gateway_response',),
			'classes': ('collapse',)
		}),
		('Timestamps', {
			'fields': ('created_at', 'updated_at', 'completed_at'),
			'classes': ('collapse',)
		}),
	)