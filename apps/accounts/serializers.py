from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "phone_number",
            "bi",
        ]
    
    def validate_bi(self, value):
        """Validar BI apenas se fornecido"""
        if not value or value.strip() == '':
            return None
        
        if User.objects.filter(bi=value).exists():
            raise serializers.ValidationError("Este BI já está registrado.")
        
        return value
    
    def validate(self, attrs):
        email = attrs.get("email")
        username = attr.get("username")
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("As palavras-passes não são iguais.")
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        
        if validated_data.get('bi') is None:
            validated_data.pop('bi', None)
        
        if not validated_data.get('phone_number'):
            validated_data.pop('phone_number', None)
            
        user = User.objects.create_user(**validated_data)
        return user
