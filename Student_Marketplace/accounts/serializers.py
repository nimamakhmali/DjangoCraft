from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers  

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ["bio", "skills"]


class UserSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer()

	class Meta:
		model = User
		fields = ["id", "username", "email", "profile"]


class SignupSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=75)
	email = serializers.EmailField(required=False, allow_blank=True)
	password = serializers.CharField(read_only=False, write_only=True, min_length=6)

	def create(self, validated_data):
		user = User.objects.create_user(
			username=validated_data["username"],
			email=validated_data.get("email", ""),
			password=validated_data["password"],
		)
		return user


class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=75)
	password = serializers.CharField(read_only=False, write_only=True)

	def validate(self, attrs):
		user = authenticate(username=attrs["username"], password=attrs["password"])
		if not user:
			raise serializers.ValidationError("Invalid credentials")
		attrs["user"] = user
		return attrs


class PasswordChangeSerializer(serializers.Serializer):
	old_password = serializers.CharField(read_only=False, write_only=True)
	new_password = serializers.CharField(read_only=False, write_only=True, min_length=6)
