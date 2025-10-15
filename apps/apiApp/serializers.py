from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from .models import Product, Category, CartItem, Cart, Review, Wishlist


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password", "first_name", "last_name", "phone_number", "bi"]

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Este nome de usuário já está em uso.")
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("As palavras-passes não são iguais.")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
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
                attrs["username"] = user_obj.username # Chance the real username for father validation
            except User.DoesNotExist:
                # If don't founde, use the username
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
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "phone_number", "bi", "avatar_url"]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "image", "price", "average_rating", "total_reviews"]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "image", "price"]


class CategoryListSerialiizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image", "slug"]


class CategoryDetailSerialiizer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "image", "products"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "sub_total"]

    def get_sub_total(self, obj):
        total = obj.product.price * obj.quantity
        return total


class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(read_only=True, many=True)
    cart_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "cart_code", "cartitems", "cart_total"]

    def get_cart_total(self, cart):
        items = cart.cartitems.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total


class CartStatSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "cart_code", "total_quantity"]

    def get_total_quantity(self, cart):
        items = cart.cartitems.all()
        total = sum([item.quantity for item in items])
        return total


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "comment", "created_at", "updated_at"]


class WishListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "user", "product", "created_at"]
