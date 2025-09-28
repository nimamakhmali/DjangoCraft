from django.db import models
from django.contrib.auth.models import User
from orders.models import Order
import uuid


class Conversation(models.Model):
	"""Represents a conversation between users, typically related to an order"""
	conversation_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	
	# Participants
	participants = models.ManyToManyField(User, related_name='conversations')
	
	# Related order (optional - for order-related conversations)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='conversations', null=True, blank=True)
	
	# Conversation metadata
	title = models.CharField(max_length=200, blank=True)
	is_active = models.BooleanField(default=True)
	
	# Timestamps
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	last_message_at = models.DateTimeField(null=True, blank=True)
	
	def __str__(self):
		return f"Conversation {self.conversation_id} - {self.title or 'Untitled'}"
	
	@property
	def other_participant(self, user):
		"""Get the other participant in the conversation"""
		return self.participants.exclude(id=user.id).first()
	
	@property
	def unread_count(self, user):
		"""Get unread message count for a user"""
		return self.messages.filter(
			sender__ne=user,
			read_at__isnull=True
		).count()


class Message(models.Model):
	"""Individual message in a conversation"""
	MESSAGE_TYPE_TEXT = 'text'
	MESSAGE_TYPE_FILE = 'file'
	MESSAGE_TYPE_SYSTEM = 'system'
	
	MESSAGE_TYPE_CHOICES = [
		(MESSAGE_TYPE_TEXT, 'Text'),
		(MESSAGE_TYPE_FILE, 'File'),
		(MESSAGE_TYPE_SYSTEM, 'System'),
	]
	
	# Message identification
	message_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	
	# Relationships
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
	
	# Message content
	message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default=MESSAGE_TYPE_TEXT)
	content = models.TextField()
	
	# File attachment (for file messages)
	attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
	attachment_name = models.CharField(max_length=255, blank=True)
	attachment_size = models.PositiveIntegerField(null=True, blank=True)
	
	# Message status
	is_edited = models.BooleanField(default=False)
	edited_at = models.DateTimeField(null=True, blank=True)
	read_at = models.DateTimeField(null=True, blank=True)
	
	# Timestamps
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return f"Message from {self.sender.username} in {self.conversation.conversation_id}"
	
	@property
	def is_read(self):
		return self.read_at is not None
	
	@property
	def file_size_mb(self):
		if self.attachment_size:
			return round(self.attachment_size / (1024 * 1024), 2)
		return 0


class MessageReadStatus(models.Model):
	"""Track read status of messages for each user"""
	message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='read_statuses')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_read_statuses')
	read_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		unique_together = ['message', 'user']
	
	def __str__(self):
		return f"{self.user.username} read message {self.message.message_id}"


class Notification(models.Model):
	"""System notifications for users"""
	NOTIFICATION_TYPE_MESSAGE = 'message'
	NOTIFICATION_TYPE_ORDER = 'order'
	NOTIFICATION_TYPE_SYSTEM = 'system'
	
	NOTIFICATION_TYPE_CHOICES = [
		(NOTIFICATION_TYPE_MESSAGE, 'Message'),
		(NOTIFICATION_TYPE_ORDER, 'Order'),
		(NOTIFICATION_TYPE_SYSTEM, 'System'),
	]
	
	# Notification identification
	notification_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	
	# Recipient
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
	
	# Notification content
	notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
	title = models.CharField(max_length=200)
	message = models.TextField()
	
	# Related objects (optional)
	related_conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)
	related_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
	
	# Status
	is_read = models.BooleanField(default=False)
	read_at = models.DateTimeField(null=True, blank=True)
	
	# Timestamps
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"Notification for {self.user.username}: {self.title}"