from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class ServicePermissionTests(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.user = User.objects.create_user(username='s1', password='secret12')
		# default role is student
		self.client.post(reverse('accounts-login'), {"username": "s1", "password": "secret12"}, format='json')

	def test_student_cannot_create_service(self):
		resp = self.client.post(reverse('services-create'), {"title": "t", "price": "5.00"}, format='json')
		self.assertEqual(resp.status_code, 403)

	def test_freelancer_can_create_service(self):
		u2 = User.objects.create_user(username='f1', password='secret12')
		u2.profile.role = 'freelancer'
		u2.profile.save(update_fields=['role'])
		client2 = APIClient()
		client2.post(reverse('accounts-login'), {"username": "f1", "password": "secret12"}, format='json')
		resp = client2.post(reverse('services-create'), {"title": "t2", "price": "5.00"}, format='json')
		self.assertEqual(resp.status_code, 201)
