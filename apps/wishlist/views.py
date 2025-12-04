from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishListSerializer
from apps.products.models import Product


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    product_id = request.data.get("product_id")

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

    user = request.user

    wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)

    if not created:
        wishlist_item.delete()
        return Response(
            {"message": "Product removed from wishlist"},
            status=status.HTTP_204_NO_CONTENT,
        )

    serializer = WishListSerializer(wishlist_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_wishlist(request):
    wishlist_itmes = Wishlist.objects.filter(user=request.user)
    serializer = WishListSerializer(wishlist_itmes, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_wishlist_item(request, pk):
    try:
        wishlist_item = Wishlist.objects.get(pk=pk, user=request.user)
        wishlist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Wishlist.DoesNotExist:
        return Response(
            {"error": "Wishlist item not found"}, status=status.HTTP_404_NOT_FOUND
        )
