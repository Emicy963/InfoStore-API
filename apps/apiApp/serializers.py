from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Category, CartItem, Cart, Review, Wishlist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'avatar_url']

class ProducListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'image', 'price']

class ProducDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'image', 'price']

class CategoryListSerialiizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image' 'slug']

class CategoryDetailSerialiizer(serializers.ModelSerializer):
    products = ProducListSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'products']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProducListSerializer(read_only=True)
    sub_total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'sub_total']

    def get_sub_total(self, obj):
        total = obj.product.price * obj.quantity
        return total

class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(read_only=True, many=True)
    cart_total = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'cartitems', 'cart_total']

    def get_cart_total(self, cart):
        items = cart.cartitems.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total

class CartStatSerializer(serializers.ModelSerializer):
    total_quantity = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'total_quantity']
    
    def get_total_quantity(self, cart):
        items = cart.cartitems.all()
        total = sum([item.quantity for item in items])
        return total

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at', 'updated_at']

class WishListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProducListSerializer(read_only=True)
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'created_at']
