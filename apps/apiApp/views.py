from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Category, Cart, CartItem, Review, Wishlist
from .serializers import (
    ProducListSerializer,
    ProducDetailSerializer,
    CategoryListSerialiizer,
    CategoryDetailSerialiizer,
    CartSerializer,
    CartItemSerializer,
    ReviewSerializer,
    WishListSerializer,
    CustomTokenObtainPairSerializer,
)

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get("email")
    password = request.data.get("password")
    name = request.data.get("name")

    if not email or not password:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "User with this email already exists."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.create_user(email=email, password=password, username=email)
    if name:
        user.first_name = name.split(" ")[0]
        if len(name.split(" ")) > 1:
            user.last_name = " ".join(name.split(" ")[1:])
        user.save()
    
    return Response(
        {"message": "User created successfully."},
        status=status.HTTP_201_CREATED
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response(
            {"message": "Succesfully logged out"},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    return Response(
        {
            "id": user.id,
            "email": user.email,
            "name": user.get_full_name() or user.username,
        }
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def product_list(requesst):
    products = Product.objects.filter(featured=True)
    serializer = ProducListSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def product_detail(request, slug):
    products = Product.objects.get(slug=slug)
    serializer = ProducDetailSerializer(products)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategoryListSerialiizer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerialiizer(category)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_cart(request, cart_code):
    try:
        cart = Cart.objects.get(cart_code=cart_code)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def add_to_cart(request):
    cart_code = request.data.get("cart_code")
    product_id = request.data.get("product_id")

    cart, created = Cart.objects.get_or_create(cart_code=cart_code)
    product = Product.objects.get(id=product_id)

    cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)
    cartitem.quantity = 1
    cartitem.save()

    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(["PUT"])
def update_cartitem_quantity(request):
    cartitem_id = request.data.get("item_id")
    quantity = request.data.get("quantity")

    quantity = int(quantity)

    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.quantity = quantity
    cartitem.save()

    serializer = CartItemSerializer(cartitem)
    return Response(
        {"data": serializer.data, "message": "CartItem updated sucessfully!"}
    )


@api_view(["POST"])
def add_review(request):
    product_id = request.data.get("product_id")
    email = request.data.get("email")
    rating = request.data.get("rating")
    comment = request.data.get("comment")

    product = Product.objects.get(id=product_id)
    user = User.objects.get(email=email)

    if Review.objects.filter(product=product, user=user).exists():
        return Response({"error": "You have already reviewed this product"}, status=400)

    review = Review.objects.create(
        product=product, user=user, rating=rating, comment=comment
    )
    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(["PUT"])
def update_review(request, pk):
    review = Review.objects.get(id=pk)
    rating = request.data.get("rating")
    comment = request.data.get("comment")

    review.rating = rating
    review.comment = comment
    review.save()

    serializer = ReviewSerializer(review)
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_review(request, pk):
    review = Review.objects.get(id=pk)
    review.delete()

    return Response("Review delete sucessfully", status=204)


@api_view(["DELETE"])
def delete_cartitem(request, pk):
    cartitem = CartItem.objects.get(id=pk)
    cartitem.delete()

    return Response("Cartitem delete sucessfully", status=204)


@api_view(["POST"])
def add_to_wishlist(request):
    email = request.data.get("email")
    product_id = request.data.get("product_id")

    user = User.objects.get(email=email)
    product = Product.objects.get(id=product_id)

    wishlist = Wishlist.objects.filter(user=user, product=product)
    if wishlist:
        wishlist.delete()
        return Response("Product removed from wishlist", status=204)

    now_wishlist = Wishlist.objects.create(user=user, product=product)
    serializer = WishListSerializer(now_wishlist)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_wishlist(request):
    wishlist_itmes = Wishlist.objects.filter(user=request.user)
    serializer = WishListSerializer(wishlist_itmes, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_wishlist_items(request, pk):
    try:
        wishlist_item = Wishlist.objects.get(pk=pk, user=request.user)
        wishlist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Wishlist.DoesNotExist:
        return Response({"error": "Wishlist item not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_user_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if created:
        # Generated a unique code for cart
        import random
        import string
        cart_code = "".join(random.choices(string.ascii_letters + string.digits, k=11))
        cart.cart_code = cart_code
        cart.save()
    serialiazer = CartSerializer(cart)
    return Response(serialiazer.data)

@api_view(["GET"])
@permission_classes([AllowAny])
def product_search(request):
    query = request.query_params.get("query")
    if not query:
        return Response({"error": "No query provided"}, status=400)
    
    products = Product.objects.filter(Q(name__icontains=query) | 
                                      Q(description__icontains=query) | 
                                      Q(category__name__icontains=query))
    
    serializer = ProducListSerializer(products, many=True)
    return Response(serializer.data)
