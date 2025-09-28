from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Payment
from orders.models import Order, OrderItem
from services.models import Service, Category


class PaymentModelTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='testpass')
		self.category = Category.objects.create(name='Programming')
		self.service = Service.objects.create(
			title='Test Service',
			description='Test Description',
			price=50.00,
			category=self.category
		)
		self.order = Order.objects.create(
			user=self.user,
			total_amount=50.00,
			status=Order.STATUS_PENDING
		)
		OrderItem.objects.create(
			order=self.order,
			service_title=self.service.title,
			unit_price=self.service.price,
			quantity=1
		)
	
	def test_payment_creation(self):
		payment = Payment.objects.create(
			order=self.order,
			user=self.user,
			amount=50.00,
			status=Payment.STATUS_PENDING
		)
		self.assertEqual(payment.amount, 50.00)
		self.assertEqual(payment.status, Payment.STATUS_PENDING)
		self.assertFalse(payment.is_successful)
		self.assertTrue(payment.is_pending)
	
	def test_payment_successful(self):
		payment = Payment.objects.create(
			order=self.order,
			user=self.user,
			amount=50.00,
			status=Payment.STATUS_COMPLETED
		)
		self.assertTrue(payment.is_successful)
		self.assertFalse(payment.is_pending)


class PaymentAPITests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='testpass')
		self.category = Category.objects.create(name='Programming')
		self.service = Service.objects.create(
			title='Test Service',
			description='Test Description',
			price=50.00,
			category=self.category
		)
		self.order = Order.objects.create(
			user=self.user,
			total_amount=50.00,
			status=Order.STATUS_PENDING
		)
		OrderItem.objects.create(
			order=self.order,
			service_title=self.service.title,
			unit_price=self.service.price,
			quantity=1
		)
	
	def test_initiate_payment_success(self):
		self.client.force_authenticate(user=self.user)
		data = {
			'order_id': self.order.id,
			'payment_method': 'mock'
		}
		response = self.client.post('/api/payments/initiate/', data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIn('payment_id', response.data)
		self.assertIn('confirmation_code', response.data)
		
		# Check payment was created
		payment = Payment.objects.get(order=self.order)
		self.assertEqual(payment.amount, 50.00)
		self.assertEqual(payment.status, Payment.STATUS_PENDING)
	
	def test_initiate_payment_duplicate(self):
		# Create existing payment
		Payment.objects.create(
			order=self.order,
			user=self.user,
			amount=50.00,
			status=Payment.STATUS_PENDING
		)
		
		self.client.force_authenticate(user=self.user)
		data = {'order_id': self.order.id}
		response = self.client.post('/api/payments/initiate/', data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_confirm_payment_success(self):
		# Create payment first
		payment = Payment.objects.create(
			order=self.order,
			user=self.user,
			amount=50.00,
			status=Payment.STATUS_PENDING,
			gateway_response={'confirmation_code': 'CONF_1234'}
		)
		
		self.client.force_authenticate(user=self.user)
		data = {
			'payment_id': str(payment.payment_id),
			'confirmation_code': 'CONF_1234'
		}
		response = self.client.post('/api/payments/confirm/', data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['status'], Payment.STATUS_COMPLETED)
		
		# Check payment and order status updated
		payment.refresh_from_db()
		self.order.refresh_from_db()
		self.assertEqual(payment.status, Payment.STATUS_COMPLETED)
		self.assertEqual(self.order.status, Order.STATUS_PAID)
	
	def test_confirm_payment_invalid_code(self):
		payment = Payment.objects.create(
			order=self.order,
			user=self.user,
			amount=50.00,
			status=Payment.STATUS_PENDING,
			gateway_response={'confirmation_code': 'CONF_1234'}
		)
		
		self.client.force_authenticate(user=self.user)
		data = {
			'payment_id': str(payment.payment_id),
			'confirmation_code': 'WRONG_CODE'
		}
		response = self.client.post('/api/payments/confirm/', data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		
		# Check payment status is failed
		payment.refresh_from_db()
		self.assertEqual(payment.status, Payment.STATUS_FAILED)
	
	def test_payment_status(self):
		payment = Payment.objects.create(
			order=self.order,
			user=self.user,
			amount=50.00,
			status=Payment.STATUS_COMPLETED
		)
		
		self.client.force_authenticate(user=self.user)
		response = self.client.get(f'/api/payments/{payment.payment_id}/status/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['status'], Payment.STATUS_COMPLETED)
	
	def test_mock_webhook(self):
		payment = Payment.objects.create(
			order=self.order,
			user=self.user,
			amount=50.00,
			status=Payment.STATUS_PENDING
		)
		
		data = {
			'payment_id': str(payment.payment_id),
			'status': 'completed'
		}
		response = self.client.post('/api/payments/webhook/mock/', data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		
		# Check payment and order status updated
		payment.refresh_from_db()
		self.order.refresh_from_db()
		self.assertEqual(payment.status, Payment.STATUS_COMPLETED)
		self.assertEqual(self.order.status, Order.STATUS_PAID)