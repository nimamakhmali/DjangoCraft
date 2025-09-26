from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes  # pyright: ignore[reportMissingImports]
from rest_framework.permissions import IsAuthenticated, AllowAny  # pyright: ignore[reportMissingImports]
from rest_framework.response import Response  # pyright: ignore[reportMissingImports]
from django.contrib.auth import login, logout
from .serializers import SignupSerializer, LoginSerializer, UserSerializer, ProfileSerializer


def ping(_request):
    return JsonResponse({"accounts": "pong"})


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
	serializer = SignupSerializer(data=request.data)
	serializer.is_valid(raise_exception=True)
	user = serializer.save()
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
def logout_view(request):
	logout(request)
	return Response({"detail": "logged out"})

# Create your views here.
