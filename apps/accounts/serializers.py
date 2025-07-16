from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """

    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password_connfirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm']

    def validate(self, attrs):
        """
        Validate thate the password and password confirmation match.
        """

        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs
    
    def create(self, validated_data):
        """
        Create a new user instance.
        """

        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'phone', 'role', 'is_active', 'created_at']
        read_only_fields = ['id', 'email', 'role', 'is_active', 'created_at']
