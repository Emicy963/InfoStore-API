from rest_framework import serializers


class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.JSONField()
    payment_method = serializers.CharField()
    notes = serializers.CharField(required=False, allow_blank=True)
