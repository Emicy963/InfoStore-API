from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category
from .serializers import ProducListSerializer, ProducDetailSerializer, CategorySerialiizer

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

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerialiizer(categories, many=True)
    return Response(serializer.data)
