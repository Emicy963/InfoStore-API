from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Q
from .models import Category, Product
from .serializers import (
    CategoryDetailSerialiizer,
    CategoryListSerialiizer,
    ProductDetailSerializer,
    ProductListSerializer,
)


class ProductPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(request):
    products = Product.objects.filter(featured=True).select_related("category")
    paginator = ProductPagination()
    result_page = paginator.paginate_queryset(products, request)
    serializer = ProductListSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def product_detail(request, slug):
    try:
        products = Product.objects.get(slug=slug)
        serializer = ProductDetailSerializer(products)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(
            {"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def category_list(request):
    try:
        categories = Category.objects.all()
        serializer = CategoryListSerialiizer(categories, many=True)
        return Response(serializer.data)
    except Category.DoesNotExist:
        Response(
            {"error": "Categorias não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def category_detail(request, slug):
    try:
        category = Category.objects.get(slug=slug)
        serializer = CategoryDetailSerialiizer(category)
        return Response(serializer.data)
    except Category.DoesNotExist:
        return Response(
            {"error": "Categoria não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([AllowAny])
def product_search(request):
    query = request.query_params.get("query")
    if not query:
        return Response({"error": "Nenhuma consulta fornecida"}, status=400)

    products = Product.objects.filter(
        Q(name__icontains=query)
        | Q(description__icontains=query)
        | Q(category__name__icontains=query)
    ).select_related("category")

    paginator = ProductPagination()
    result_page = paginator.paginate_queryset(products, request)

    serializer = ProductListSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
