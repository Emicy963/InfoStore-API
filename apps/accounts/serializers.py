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
        fields = ['email', 'username', 'password', 'password_confirm']
        extra_kwarks = {
            'username': {'required': False},
            'email': {'required': True},
        }

    def validate(self, attrs):
        """
        Validate thate the password and password confirmation match.
        """

        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError('Passwords do not match.')
        return attrs
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is already in use.')
        return value
    
    def create(self, validated_data):
        """
        Create a new user instance.
        """

        validated_data.pop('password_confirm')
        
        # Create username if not provided
        if not validated_data.get('username'):
            validated_data['username'] = validated_data['email'].split('@')[0]

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

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile with additional fields.
    """
    class Meta:
        model = User
        fields = ['avatar', 'birth_date', 'address']
