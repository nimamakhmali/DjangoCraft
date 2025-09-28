from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Conversation, Message, MessageReadStatus, Notification
from accounts.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
	sender = UserSerializer(read_only=True)
	is_read = serializers.SerializerMethodField()
	file_size_mb = serializers.ReadOnlyField()
	
	class Meta:
		model = Message
		fields = [
			'message_id', 'sender', 'message_type', 'content',
			'attachment', 'attachment_name', 'attachment_size', 'file_size_mb',
			'is_edited', 'edited_at', 'is_read', 'read_at',
			'created_at', 'updated_at'
		]
		read_only_fields = [
			'message_id', 'sender', 'is_edited', 'edited_at',
			'read_at', 'created_at', 'updated_at'
		]
	
	def get_is_read(self, obj):
		request = self.context.get('request')
		if request and request.user.is_authenticated:
			return obj.read_statuses.filter(user=request.user).exists()
		return False


class MessageCreateSerializer(serializers.Serializer):
	content = serializers.CharField(max_length=5000)
	message_type = serializers.ChoiceField(choices=Message.MESSAGE_TYPE_CHOICES, default=Message.MESSAGE_TYPE_TEXT)
	
	def validate_content(self, value):
		if not value.strip():
			raise serializers.ValidationError("Message content cannot be empty")
		return value.strip()


class ConversationSerializer(serializers.ModelSerializer):
	participants = UserSerializer(many=True, read_only=True)
	other_participant = serializers.SerializerMethodField()
	unread_count = serializers.SerializerMethodField()
	last_message = serializers.SerializerMethodField()
	
	class Meta:
		model = Conversation
		fields = [
			'conversation_id', 'participants', 'other_participant',
			'order', 'title', 'is_active', 'unread_count',
			'last_message', 'created_at', 'updated_at', 'last_message_at'
		]
		read_only_fields = [
			'conversation_id', 'participants', 'created_at', 'updated_at'
		]
	
	def get_other_participant(self, obj):
		request = self.context.get('request')
		if request and request.user.is_authenticated:
			other = obj.participants.exclude(id=request.user.id).first()
			if other:
				return UserSerializer(other).data
		return None
	
	def get_unread_count(self, obj):
		request = self.context.get('request')
		if request and request.user.is_authenticated:
			return obj.messages.filter(
				read_statuses__user=request.user
			).exclude(sender=request.user).count()
		return 0
	
	def get_last_message(self, obj):
		last_msg = obj.messages.order_by('-created_at').first()
		if last_msg:
			return MessageSerializer(last_msg, context=self.context).data
		return None


class ConversationCreateSerializer(serializers.Serializer):
	participant_id = serializers.IntegerField()
	order_id = serializers.IntegerField(required=False, allow_null=True)
	title = serializers.CharField(max_length=200, required=False, allow_blank=True)
	
	def validate_participant_id(self, value):
		try:
			user = User.objects.get(pk=value)
		except User.DoesNotExist:
			raise serializers.ValidationError("User not found")
		return value
	
	def validate_order_id(self, value):
		if value:
			from orders.models import Order
			try:
				order = Order.objects.get(pk=value)
			except Order.DoesNotExist:
				raise serializers.ValidationError("Order not found")
		return value


class MessageReadStatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = MessageReadStatus
		fields = ['message', 'user', 'read_at']
		read_only_fields = ['user', 'read_at']


class NotificationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notification
		fields = [
			'notification_id', 'notification_type', 'title', 'message',
			'related_conversation', 'related_order', 'is_read', 'read_at',
			'created_at'
		]
		read_only_fields = [
			'notification_id', 'is_read', 'read_at', 'created_at'
		]


class ConversationListSerializer(serializers.ModelSerializer):
	"""Simplified serializer for conversation lists"""
	other_participant = serializers.SerializerMethodField()
	unread_count = serializers.SerializerMethodField()
	last_message_preview = serializers.SerializerMethodField()
	
	class Meta:
		model = Conversation
		fields = [
			'conversation_id', 'other_participant', 'title',
			'unread_count', 'last_message_preview', 'last_message_at',
			'created_at', 'updated_at'
		]
	
	def get_other_participant(self, obj):
		request = self.context.get('request')
		if request and request.user.is_authenticated:
			other = obj.participants.exclude(id=request.user.id).first()
			if other:
				return {
					'id': other.id,
					'username': other.username,
					'first_name': other.first_name,
					'last_name': other.last_name
				}
		return None
	
	def get_unread_count(self, obj):
		request = self.context.get('request')
		if request and request.user.is_authenticated:
			return obj.messages.filter(
				read_statuses__user=request.user
			).exclude(sender=request.user).count()
		return 0
	
	def get_last_message_preview(self, obj):
		last_msg = obj.messages.order_by('-created_at').first()
		if last_msg:
			preview = last_msg.content[:100]
			if len(last_msg.content) > 100:
				preview += "..."
			return {
				'content': preview,
				'sender': last_msg.sender.username,
				'created_at': last_msg.created_at
			}
		return None
