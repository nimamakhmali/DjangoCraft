from django.contrib import admin
from .models import Conversation, Message, MessageReadStatus, Notification


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
	list_display = ('conversation_id', 'title', 'is_active', 'created_at', 'last_message_at')
	list_filter = ('is_active', 'created_at')
	search_fields = ('conversation_id', 'title')
	readonly_fields = ('conversation_id', 'created_at', 'updated_at', 'last_message_at')
	
	fieldsets = (
		('Conversation Info', {
			'fields': ('conversation_id', 'title', 'is_active', 'order')
		}),
		('Participants', {
			'fields': ('participants',)
		}),
		('Timestamps', {
			'fields': ('created_at', 'updated_at', 'last_message_at'),
			'classes': ('collapse',)
		}),
	)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ('message_id', 'conversation', 'sender', 'message_type', 'created_at', 'is_edited')
	list_filter = ('message_type', 'is_edited', 'created_at')
	search_fields = ('message_id', 'content', 'sender__username')
	readonly_fields = ('message_id', 'created_at', 'updated_at', 'edited_at')
	
	fieldsets = (
		('Message Info', {
			'fields': ('message_id', 'conversation', 'sender', 'message_type')
		}),
		('Content', {
			'fields': ('content', 'attachment', 'attachment_name', 'attachment_size')
		}),
		('Status', {
			'fields': ('is_edited', 'edited_at', 'read_at')
		}),
		('Timestamps', {
			'fields': ('created_at', 'updated_at'),
			'classes': ('collapse',)
		}),
	)


@admin.register(MessageReadStatus)
class MessageReadStatusAdmin(admin.ModelAdmin):
	list_display = ('message', 'user', 'read_at')
	list_filter = ('read_at',)
	search_fields = ('message__message_id', 'user__username')
	readonly_fields = ('read_at',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	list_display = ('notification_id', 'user', 'notification_type', 'title', 'is_read', 'created_at')
	list_filter = ('notification_type', 'is_read', 'created_at')
	search_fields = ('notification_id', 'title', 'user__username')
	readonly_fields = ('notification_id', 'created_at', 'read_at')
	
	fieldsets = (
		('Notification Info', {
			'fields': ('notification_id', 'user', 'notification_type')
		}),
		('Content', {
			'fields': ('title', 'message')
		}),
		('Related Objects', {
			'fields': ('related_conversation', 'related_order'),
			'classes': ('collapse',)
		}),
		('Status', {
			'fields': ('is_read', 'read_at', 'created_at')
		}),
	)