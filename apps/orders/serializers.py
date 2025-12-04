from rest_framework import serializers
from .models import OrderItem
from apps.products.serializers import ProductListSerializer


class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.JSONField()
    payment_method = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]
