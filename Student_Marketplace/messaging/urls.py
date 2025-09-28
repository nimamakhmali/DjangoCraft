from django.urls import path
from .views import (
	conversation_list, conversation_create, conversation_detail,
	message_send, message_mark_read,
	notifications_list, notification_mark_read, unread_counts,
	order_conversations
)

urlpatterns = [
	# Conversations
	path('conversations/', conversation_list, name='messaging-conversations'),
	path('conversations/create/', conversation_create, name='messaging-conversation-create'),
	path('conversations/<uuid:conversation_id>/', conversation_detail, name='messaging-conversation-detail'),
	
	# Messages
	path('conversations/<uuid:conversation_id>/send/', message_send, name='messaging-message-send'),
	path('messages/<uuid:message_id>/read/', message_mark_read, name='messaging-message-read'),
	
	# Notifications
	path('notifications/', notifications_list, name='messaging-notifications'),
	path('notifications/<uuid:notification_id>/read/', notification_mark_read, name='messaging-notification-read'),
	
	# Order integration
	path('orders/<int:order_id>/conversations/', order_conversations, name='messaging-order-conversations'),
	
	# Utility
	path('unread-counts/', unread_counts, name='messaging-unread-counts'),
]
