from rest_framework import serializers
from .models import Wishlist
from apps.accounts.serializers import UserSerializer
from apps.products.serializers import ProductListSerializer


class WishListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "user", "product", "created_at"]
