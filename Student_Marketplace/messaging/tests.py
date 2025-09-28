from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Conversation, Message, MessageReadStatus, Notification
from orders.models import Order, OrderItem
from services.models import Service, Category


class MessagingModelTests(TestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username='user1', password='testpass')
		self.user2 = User.objects.create_user(username='user2', password='testpass')
		self.category = Category.objects.create(name='Programming')
		self.service = Service.objects.create(
			title='Test Service',
			description='Test Description',
			price=50.00,
			category=self.category
		)
		self.order = Order.objects.create(
			user=self.user1,
			total_amount=50.00,
			status=Order.STATUS_PENDING
		)
		OrderItem.objects.create(
			order=self.order,
			service_title=self.service.title,
			unit_price=self.service.price,
			quantity=1
		)
	
	def test_conversation_creation(self):
		conversation = Conversation.objects.create(
			title='Test Conversation',
			order=self.order
		)
		conversation.participants.add(self.user1, self.user2)
		
		self.assertEqual(conversation.participants.count(), 2)
		self.assertEqual(conversation.title, 'Test Conversation')
		self.assertTrue(conversation.is_active)
	
	def test_message_creation(self):
		conversation = Conversation.objects.create(title='Test Conversation')
		conversation.participants.add(self.user1, self.user2)
		
		message = Message.objects.create(
			conversation=conversation,
			sender=self.user1,
			content='Hello, this is a test message',
			message_type=Message.MESSAGE_TYPE_TEXT
		)
		
		self.assertEqual(message.conversation, conversation)
		self.assertEqual(message.sender, self.user1)
		self.assertEqual(message.content, 'Hello, this is a test message')
		self.assertFalse(message.is_edited)
		self.assertFalse(message.is_read)
	
	def test_notification_creation(self):
		notification = Notification.objects.create(
			user=self.user1,
			notification_type=Notification.NOTIFICATION_TYPE_MESSAGE,
			title='New Message',
			message='You have a new message'
		)
		
		self.assertEqual(notification.user, self.user1)
		self.assertEqual(notification.notification_type, Notification.NOTIFICATION_TYPE_MESSAGE)
		self.assertFalse(notification.is_read)


class MessagingAPITests(APITestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username='user1', password='testpass')
		self.user2 = User.objects.create_user(username='user2', password='testpass')
		self.category = Category.objects.create(name='Programming')
		self.service = Service.objects.create(
			title='Test Service',
			description='Test Description',
			price=50.00,
			category=self.category
		)
		self.order = Order.objects.create(
			user=self.user1,
			total_amount=50.00,
			status=Order.STATUS_PENDING
		)
		OrderItem.objects.create(
			order=self.order,
			service_title=self.service.title,
			unit_price=self.service.price,
			quantity=1
		)
	
	def test_conversation_create_success(self):
		self.client.force_authenticate(user=self.user1)
		data = {
			'participant_id': self.user2.id,
			'title': 'Test Conversation',
			'order_id': self.order.id
		}
		response = self.client.post('/api/messaging/conversations/create/', data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('conversation_id', response.data)
		
		# Check conversation was created
		conversation = Conversation.objects.get(participants=self.user1)
		self.assertEqual(conversation.participants.count(), 2)
		self.assertEqual(conversation.title, 'Test Conversation')
		self.assertEqual(conversation.order, self.order)
	
	def test_conversation_create_duplicate(self):
		# Create existing conversation
		conversation = Conversation.objects.create(title='Existing Conversation')
		conversation.participants.add(self.user1, self.user2)
		
		self.client.force_authenticate(user=self.user1)
		data = {
			'participant_id': self.user2.id,
			'title': 'New Conversation'
		}
		response = self.client.post('/api/messaging/conversations/create/', data)
		# Should return 201 for new conversation since the logic creates a new one
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('conversation_id', response.data)
	
	def test_message_send_success(self):
		# Create conversation first
		conversation = Conversation.objects.create(title='Test Conversation')
		conversation.participants.add(self.user1, self.user2)
		
		self.client.force_authenticate(user=self.user1)
		data = {
			'content': 'Hello, this is a test message',
			'message_type': Message.MESSAGE_TYPE_TEXT
		}
		response = self.client.post(f'/api/messaging/conversations/{conversation.conversation_id}/send/', data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('message_id', response.data)
		
		# Check message was created
		message = Message.objects.get(conversation=conversation)
		self.assertEqual(message.content, 'Hello, this is a test message')
		self.assertEqual(message.sender, self.user1)
	
	def test_message_send_unauthorized(self):
		# Create conversation with different users
		user3 = User.objects.create_user(username='user3', password='testpass')
		conversation = Conversation.objects.create(title='Test Conversation')
		conversation.participants.add(self.user2, user3)
		
		self.client.force_authenticate(user=self.user1)
		data = {'content': 'Unauthorized message'}
		response = self.client.post(f'/api/messaging/conversations/{conversation.conversation_id}/send/', data)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
	
	def test_conversation_list(self):
		# Create conversations
		conversation1 = Conversation.objects.create(title='Conversation 1')
		conversation1.participants.add(self.user1, self.user2)
		
		conversation2 = Conversation.objects.create(title='Conversation 2')
		conversation2.participants.add(self.user1, self.user2)
		
		self.client.force_authenticate(user=self.user1)
		response = self.client.get('/api/messaging/conversations/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data['results']), 2)
	
	def test_message_mark_read(self):
		# Create conversation and message
		conversation = Conversation.objects.create(title='Test Conversation')
		conversation.participants.add(self.user1, self.user2)
		
		message = Message.objects.create(
			conversation=conversation,
			sender=self.user2,
			content='Test message'
		)
		
		self.client.force_authenticate(user=self.user1)
		response = self.client.post(f'/api/messaging/messages/{message.message_id}/read/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
		# Check read status was created
		read_status = MessageReadStatus.objects.get(message=message, user=self.user1)
		self.assertIsNotNone(read_status.read_at)
	
	def test_notifications_list(self):
		# Create notifications
		Notification.objects.create(
			user=self.user1,
			notification_type=Notification.NOTIFICATION_TYPE_MESSAGE,
			title='Test Notification 1',
			message='Test message 1'
		)
		Notification.objects.create(
			user=self.user1,
			notification_type=Notification.NOTIFICATION_TYPE_ORDER,
			title='Test Notification 2',
			message='Test message 2'
		)
		
		self.client.force_authenticate(user=self.user1)
		response = self.client.get('/api/messaging/notifications/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data['results']), 2)
	
	def test_notification_mark_read(self):
		notification = Notification.objects.create(
			user=self.user1,
			notification_type=Notification.NOTIFICATION_TYPE_MESSAGE,
			title='Test Notification',
			message='Test message'
		)
		
		self.client.force_authenticate(user=self.user1)
		response = self.client.post(f'/api/messaging/notifications/{notification.notification_id}/read/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
		# Check notification was marked as read
		notification.refresh_from_db()
		self.assertTrue(notification.is_read)
		self.assertIsNotNone(notification.read_at)
	
	def test_unread_counts(self):
		# Create conversation with unread messages
		conversation = Conversation.objects.create(title='Test Conversation')
		conversation.participants.add(self.user1, self.user2)
		
		Message.objects.create(
			conversation=conversation,
			sender=self.user2,
			content='Unread message 1'
		)
		Message.objects.create(
			conversation=conversation,
			sender=self.user2,
			content='Unread message 2'
		)
		
		# Create unread notification
		Notification.objects.create(
			user=self.user1,
			notification_type=Notification.NOTIFICATION_TYPE_MESSAGE,
			title='Unread Notification',
			message='Unread message'
		)
		
		self.client.force_authenticate(user=self.user1)
		response = self.client.get('/api/messaging/unread-counts/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['unread_conversations'], 1)
		self.assertEqual(response.data['unread_notifications'], 1)