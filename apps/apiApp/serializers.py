from rest_framework import serializers
from .models import Product, Category, CartItem

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
        fields = ['id', 'name', 'image' 'products']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProducListSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'sub_total']

    def get_sub_total(self, obj: CartItem):
        total = obj.product.price * obj.quantity
        return total
