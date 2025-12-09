from rest_framework import serializers
from .models import Category, Product


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
    category = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "image", "price", "category"]
    
    def get_category(self, obj):
        if obj.category:
            return {
                "id": obj.category.id,
                "name": obj.category.name,
                "slug": obj.category.slug
            }
        return None


class CategoryListSerialiizer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ["id", "name", "image", "slug", "product_count"]
    
    def get_product_count(self, obj):
        return obj.products.count()


class CategoryDetailSerialiizer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "image", "products"]
