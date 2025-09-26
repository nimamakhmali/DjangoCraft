from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class AuthFlowTests(TestCase):
	def setUp(self):
		self.client = APIClient()

	def test_signup_login_me_password_jwt(self):
		# signup
		resp = self.client.post(reverse('accounts-signup'), {"username": "u1", "email": "e@example.com", "password": "secret12"}, format='json')
		self.assertEqual(resp.status_code, 201)
		# login
		resp = self.client.post(reverse('accounts-login'), {"username": "u1", "password": "secret12"}, format='json')
		self.assertEqual(resp.status_code, 200)
		# me
		resp = self.client.get(reverse('accounts-me'))
		self.assertEqual(resp.status_code, 200)
		# password change
		resp = self.client.post(reverse('accounts-password-change'), {"old_password": "secret12", "new_password": "secret34"}, format='json')
		self.assertEqual(resp.status_code, 200)
		# jwt obtain
		resp = self.client.post(reverse('token_obtain_pair'), {"username": "u1", "password": "secret34"}, format='json')
		self.assertEqual(resp.status_code, 200)
		self.assertIn('access', resp.data)
		# verify email send/confirm
		resp = self.client.post(reverse('accounts-verify-send'))
		self.assertEqual(resp.status_code, 200)
		user = User.objects.get(username='u1')
		token = user.profile.verification_token
		resp = self.client.post(reverse('accounts-verify-confirm'), {"token": token}, format='json')
		self.assertEqual(resp.status_code, 200)
