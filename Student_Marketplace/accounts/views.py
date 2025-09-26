from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes  # pyright: ignore[reportMissingImports]
from rest_framework.permissions import IsAuthenticated, AllowAny  # pyright: ignore[reportMissingImports]
from rest_framework.response import Response  # pyright: ignore[reportMissingImports]
from django.contrib.auth import login, logout
from .serializers import SignupSerializer, LoginSerializer, UserSerializer, ProfileSerializer, PasswordChangeSerializer
from django.core.mail import send_mail
from django.conf import settings
import secrets


def ping(_request):
    return JsonResponse({"accounts": "pong"})


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
	serializer = SignupSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	user = serializer.save()
	# generate verification token
	token = secrets.token_hex(16)
	user.profile.verification_token = token
	user.profile.email_verified = False
	user.profile.save(update_fields=['verification_token', 'email_verified'])
	# send console email
	try:
		send_mail(
			subject='Verify your email',
			message=f'Your verification token: {token}',
			from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com'),
			recipient_list=[user.email] if user.email else [],
			fail_silently=True,
		)
	except Exception:
		pass
	return Response(UserSerializer(user).data, status=201)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
	serializer = LoginSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	user = serializer.validated_data['user']
	login(request, user)
	return Response(UserSerializer(user).data)


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def me(request):
	user = request.user
	if request.method == "GET":
		return Response(UserSerializer(user).data)
	# PUT
	profile = user.profile
	profile_serializer = ProfileSerializer(profile, data=request.data.get('profile', {}), partial=True)
	profile_serializer.is_valid(raise_exception=True)
	profile_serializer.save()
	return Response(UserSerializer(user).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def password_change(request):
	serializer = PasswordChangeSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	user = request.user
	if not user.check_password(serializer.validated_data['old_password']):
		return Response({"detail": "old password incorrect"}, status=400)
	user.set_password(serializer.validated_data['new_password'])
	user.save(update_fields=['password'])
	return Response({"detail": "password changed"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_verification(request):
	user = request.user
	if user.profile.email_verified:
		return Response({"detail": "already verified"})
	token = secrets.token_hex(16)
	user.profile.verification_token = token
	user.profile.save(update_fields=['verification_token'])
	try:
		send_mail(
			subject='Verify your email',
			message=f'Your verification token: {token}',
			from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com'),
			recipient_list=[user.email] if user.email else [],
			fail_silently=True,
		)
	except Exception:
		pass
	return Response({"detail": "verification sent"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_email(request):
	user = request.user
	provided = request.data.get('token')
	if not provided or provided != user.profile.verification_token:
		return Response({"detail": "invalid token"}, status=400)
	user.profile.email_verified = True
	user.profile.verification_token = ''
	user.profile.save(update_fields=['email_verified', 'verification_token'])
	return Response({"detail": "email verified"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
	logout(request)
	return Response({"detail": "logged out"})

# Create your views here.
