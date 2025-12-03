from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
        if not value or value.strip() == "":
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

        if validated_data.get("bi") is None:
            validated_data.pop("bi", None)

        if not validated_data.get("phone_number"):
            validated_data.pop("phone_number", None)

        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # The field 'username' on request and be username or email
        identifier = attrs.get("username")
        password = attrs.get("password")

        # Try email first
        if identifier and password:
            try:
                user_obj = User.objects.get(email=identifier)
                attrs["username"] = (
                    user_obj.username
                )  # Chance the real username for father validation
            except User.DoesNotExist:
                # If don't found, use the username
                pass

        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "email": self.user.email,
            "username": self.user.username,
            "name": self.user.get_full_name() or self.user.username,
        }
        return data


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    phone = serializers.CharField(
        source="phone_number", allow_blank=True, allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "first_name",
            "last_name",
            "email",
            "phone",
            "bi",
            "avatar_url",
            "address",
            "city",
            "country",
        ]

    def get_name(self, obj):
        """Retorna o nome completo ou username"""
        full_name = obj.get_full_name()
        return full_name if full_name.strip() else obj.username
