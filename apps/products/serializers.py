from rest_framework import serializers
from .models import Product


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
