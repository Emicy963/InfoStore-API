from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Order,
    OrderItem,
    Product,
    Category,
    CartItem,
    Cart,
    Review,
    Wishlist,
)
from apps.accounts.serializers import UserSerializer


User = get_user_model()


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "image",
            "price",
            "average_rating",
            "total_reviews",
        ]


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


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_code",
            "status",
            "payment_method",
            "total_amount",
            "shipping_address",
            "notes",
            "created_at",
            "updated_at",
            "items",
        ]


class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.JSONField()
    payment_method = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)
