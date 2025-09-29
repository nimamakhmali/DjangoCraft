from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.db.models import Q, F, Count
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Conversation, Message, MessageReadStatus, Notification
from .serializers import (
	ConversationSerializer, ConversationCreateSerializer, ConversationListSerializer,
	MessageSerializer, MessageCreateSerializer, NotificationSerializer
)


class MessagePagination(PageNumberPagination):
	page_size = 20
	page_size_query_param = 'page_size'
	max_page_size = 100


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def conversation_list(request):
	"""List conversations for the authenticated user"""
	conversations = Conversation.objects.filter(
		participants=request.user,
		is_active=True
	).prefetch_related('participants', 'messages').order_by('-last_message_at', '-created_at')
	
	# Apply pagination
	paginator = MessagePagination()
	page = paginator.paginate_queryset(conversations, request)
	
	serializer = ConversationListSerializer(page, many=True, context={'request': request})
	return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def conversation_create(request):
	"""Create a new conversation"""
	serializer = ConversationCreateSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	
	participant_id = serializer.validated_data['participant_id']
	order_id = serializer.validated_data.get('order_id')
	title = serializer.validated_data.get('title', '')
	
	# Check if conversation already exists
	existing = Conversation.objects.filter(
		participants=request.user,
		participants__id=participant_id,
		is_active=True
	).first()
	
	if existing:
		return Response({
			"conversation_id": str(existing.conversation_id),
			"message": "Conversation already exists"
		}, status=status.HTTP_200_OK)
	
	# Create new conversation
	conversation = Conversation.objects.create(
		title=title,
		order_id=order_id
	)
	conversation.participants.add(request.user, participant_id)
	
	# Create notification for the other participant
	other_user = User.objects.get(pk=participant_id)
	Notification.objects.create(
		user=other_user,
		notification_type=Notification.NOTIFICATION_TYPE_MESSAGE,
		title="New Conversation",
		message=f"{request.user.username} started a conversation with you",
		related_conversation=conversation
	)
	
	return Response({
		"conversation_id": str(conversation.conversation_id),
		"message": "Conversation created successfully"
	}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def conversation_detail(request, conversation_id):
	"""Get conversation details and messages"""
	try:
		conversation = Conversation.objects.get(
			conversation_id=conversation_id,
			participants=request.user,
			is_active=True
		)
	except Conversation.DoesNotExist:
		return Response({"detail": "Conversation not found"}, status=404)
	
	# Get messages with pagination
	messages = conversation.messages.select_related('sender').order_by('created_at')
	
	paginator = MessagePagination()
	page = paginator.paginate_queryset(messages, request)
	
	# Mark messages as read (those without a read status for this user)
	unread_messages = conversation.messages.exclude(sender=request.user).exclude(
		read_statuses__user=request.user
	)
	
	for message in unread_messages:
		MessageReadStatus.objects.get_or_create(
			message=message,
			user=request.user
		)
	
	conversation_serializer = ConversationSerializer(conversation, context={'request': request})
	messages_serializer = MessageSerializer(page, many=True, context={'request': request})
	
	return paginator.get_paginated_response({
		'conversation': conversation_serializer.data,
		'messages': messages_serializer.data
	})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def message_send(request, conversation_id):
	"""Send a message in a conversation"""
	try:
		conversation = Conversation.objects.get(
			conversation_id=conversation_id,
			participants=request.user,
			is_active=True
		)
	except Conversation.DoesNotExist:
		return Response({"detail": "Conversation not found"}, status=404)
	
	serializer = MessageCreateSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	
	# Create message
	validated = serializer.validated_data
	message = Message.objects.create(
		conversation=conversation,
		sender=request.user,
		content=validated.get('content', ''),
		message_type=validated['message_type'],
		attachment=validated.get('attachment'),
		attachment_name=validated.get('attachment_name') or (validated.get('attachment').name if validated.get('attachment') else ''),
		attachment_size=(validated.get('attachment').size if validated.get('attachment') else None),
	)
	
	# Update conversation last_message_at
	conversation.last_message_at = timezone.now()
	conversation.save(update_fields=['last_message_at'])
	
	# Create notification for other participants
	other_participants = conversation.participants.exclude(id=request.user.id)
	for participant in other_participants:
		Notification.objects.create(
			user=participant,
			notification_type=Notification.NOTIFICATION_TYPE_MESSAGE,
			title="New Message",
			message=f"{request.user.username} sent you a message",
			related_conversation=conversation
		)
	
	return Response(MessageSerializer(message, context={'request': request}).data, status=201)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def message_mark_read(request, message_id):
	"""Mark a message as read"""
	try:
		message = Message.objects.get(
			message_id=message_id,
			conversation__participants=request.user
		)
	except Message.DoesNotExist:
		return Response({"detail": "Message not found"}, status=404)
	
	# Create or update read status
	read_status, created = MessageReadStatus.objects.get_or_create(
		message=message,
		user=request.user,
		defaults={'read_at': timezone.now()}
	)
	
	if not created:
		read_status.read_at = timezone.now()
		read_status.save(update_fields=['read_at'])
	
	return Response({"message": "Message marked as read"}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notifications_list(request):
	"""List notifications for the authenticated user"""
	notifications = Notification.objects.filter(
		user=request.user
	).order_by('-created_at')
	
	# Apply pagination
	paginator = MessagePagination()
	page = paginator.paginate_queryset(notifications, request)
	
	serializer = NotificationSerializer(page, many=True)
	return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def notification_mark_read(request, notification_id):
	"""Mark a notification as read"""
	try:
		notification = Notification.objects.get(
			notification_id=notification_id,
			user=request.user
		)
	except Notification.DoesNotExist:
		return Response({"detail": "Notification not found"}, status=404)
	
	notification.is_read = True
	notification.read_at = timezone.now()
	notification.save(update_fields=['is_read', 'read_at'])
	
	return Response({"message": "Notification marked as read"}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_counts(request):
	"""Get unread counts for conversations and notifications"""
	# Unread conversation count
	unread_conversations = Conversation.objects.filter(
		participants=request.user,
		is_active=True
	).annotate(
		unread_count=Count(
			'messages',
			filter=Q(
				~Q(messages__sender=request.user)
			)
		)
	).filter(unread_count__gt=0).count()
	
	# Unread notifications count
	unread_notifications = Notification.objects.filter(
		user=request.user,
		is_read=False
	).count()
	
	return Response({
		'unread_conversations': unread_conversations,
		'unread_notifications': unread_notifications
	})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_conversations(request, order_id):
	"""Get conversations related to a specific order"""
	from orders.models import Order
	
	try:
		order = Order.objects.get(pk=order_id, user=request.user)
	except Order.DoesNotExist:
		return Response({"detail": "Order not found"}, status=404)
	
	conversations = Conversation.objects.filter(
		order=order,
		participants=request.user,
		is_active=True
	).prefetch_related('participants', 'messages').order_by('-last_message_at')
	
	serializer = ConversationListSerializer(conversations, many=True, context={'request': request})
	return Response(serializer.data)