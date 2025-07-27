from rest_framework import serializers
from .models import Product, Category

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
