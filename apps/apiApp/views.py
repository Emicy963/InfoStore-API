from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProducListSerializer, ProducDetailSerializer

@api_view(['GET'])
def product_list(requesst):
    products = Product.objects.filter(featured=True)
    serializer = ProducListSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, slug):
    products = Product.objects.get(slug=slug)
    serializer = ProducDetailSerializer(products)
    return Response(serializer.data)
