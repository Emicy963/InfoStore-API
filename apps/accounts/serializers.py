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

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is inactive.')
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include email and password.')
        
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'full_name', 'phone', 
            'role', 'is_active', 'created_at', 'updated_at',
            'orders_count']
        read_only_fields = ['id', 'email', 'role', 'is_active', 'created_at', 'updated_at']
    
    def get_orders_count(self, obj):
        """
        Retorna o número de pedidos do usuário
        """
        return obj.orders.count()

class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile with additional fields.
    """
    class Meta:
        model = User
        fields = ['avatar', 'birth_date', 'address']
