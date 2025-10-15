from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from .models import Product, Category, Cart, CartItem, Review, Wishlist
from .serializers import (
    CustomTokenObtainPairSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    CategoryListSerialiizer,
    CategoryDetailSerialiizer,
    CartSerializer,
    CartItemSerializer,
    RegistrationSerializer,
    ReviewSerializer,
    UserSerializer,
    WishListSerializer,
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
            {"message": "Novo usuário criado com sucesso."},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response(
            {"message": "Succesfully logged out"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request, user_id):
    try:
        user_to_view = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "Perfil não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    # PERMISSIONS: Just the himself profile and admin can see the some profile
    if request.user.id == user_to_view.id or request.user.is_staff:
        serializer = UserSerializer(user_to_view)
        return Response(serializer.data)

    return Response(
        {"error": "Você não tem permissão para ver este perfil."},
        status=status.HTTP_403_FORBIDDEN,
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


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def handle_cart(request):
    """
    Endpoint unify for create and get cart.
    - POST: Create a cart (anonumos or user).
    - GET: Get cart (anonymos with ?code= or auth user).
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            # Case 1: Auth User
            cart, created = Cart.objects.get_or_create(user=request.user)
            if created:
                import random
                import string

                cart.cart_code = "".join(
                    random.choices(string.ascii_letters + string.digits, k=11)
                )
                cart.save()
            message = "Carrinho do usuário obtido/criado com sucesso."
        else:
            # Case 2: Invite (Anonymos)
            import random
            import string

            cart_code = "".join(
                random.choices(string.ascii_letters + string.digits, k=11)
            )
            cart = Cart.objects.create(cart_code=cart_code)
            message = "Carrinho de visitante criado com sucesso."

        serializer = CartSerializer(cart)
        return Response(
            {"data": serializer.data, "message": message},
            status=status.HTTP_201_CREATED,
        )

    elif request.method == "GET":
        cart_code = request.query_params.get("code")

        if cart_code:
            try:
                cart = Cart.objects.get(cart_code=cart_code)
                serializer = CartSerializer(cart)
                return Response(serializer.data)
            except Cart.DoesNotExist:
                return Response(
                    {"error": "Carrinho não encontrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        elif request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                serializer = CartSerializer(cart)
                return Response(serializer.data)
            except Cart.DoesNotExist:
                return Response(
                    {"error": "Carrinho de usuário não encontrado. Crie um primeiro."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        return Response(
            {
                "error": "É necessário estar autenticado ou fornecer um código de carrinho."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def add_to_cart(request):
    cart_code = request.data.get("cart_code")
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    try:
        cart, created = Cart.objects.get_or_create(cart_code=cart_code)
        product = Product.objects.get(id=product_id)

        cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)

        if created:
            cartitem.quantity = quantity
        else:
            cartitem.quantity += quantity

        cartitem.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(
            {"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_cartitem_quantity(request):
    cartitem_id = request.data.get("item_id")
    quantity = request.data.get("quantity")

    try:
        quantity = int(quantity)
        if quantity <= 0:
            return Response(
                {"error": "A quantidade deve ser maior que zero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        cartitem = CartItem.objects.get(id=cartitem_id)

        if cartitem.cart.user and cartitem.cart.user != request.user:
            return Response(
                {"error": "Você não tem permissão para modificar este item."},
                status=status.HTTP_403_FORBIDDEN,
            )

        cartitem.quantity = quantity
        cartitem.save()

        serializer = CartItemSerializer(cartitem)
        return Response(
            {
                "data": serializer.data,
                "message": "Item do carrinho atualizado com sucesso!",
            }
        )
    except CartItem.DoesNotExist:
        return Response(
            {"error": "Item do carrinho não encontrado."},
            status=status.HTTP_404_NOT_FOUND,
        )
    except ValueError:
        return Response(
            {"error": "Quantidade inválida."}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request):
    product_id = request.data.get("product_id")
    rating = request.data.get("rating")
    comment = request.data.get("comment")

    try:
        product = Product.objects.get(id=product_id)

        user = request.user

        if Review.objects.filter(product=product, user=user).exists():
            return Response(
                {"error": "Você já avaliou este produto"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        review = Review.objects.create(
            product=product, user=user, rating=rating, comment=comment
        )
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Product.DoesNotExist:
        return Response(
            {"error": "Produto não encontrado"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_review(request, pk):
    try:
        review = Review.objects.get(id=pk)

        if review.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "Você não tem permissão para modificar esta avaliação"},
                status=status.HTTP_403_FORBIDDEN,
            )

        rating = request.data.get("rating")
        comment = request.data.get("comment")

        review.rating = rating
        review.comment = comment
        review.save()

        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    except Review.DoesNotExist:
        return Response(
            {"error": "Avaliação não encontrada"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    try:
        review = Review.objects.get(id=pk)

        if review.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "Você não tem permissão para excluir esta avaliação"},
                status=status.HTTP_403_FORBIDDEN,
            )

        review.delete()
        return Response(
            {"message": "Avaliação excluída com sucesso"},
            status=status.HTTP_204_NO_CONTENT,
        )
    except Review.DoesNotExist:
        return Response(
            {"error": "Avaliação não encontrada"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_cartitem(request, pk):
    try:
        cartitem = CartItem.objects.get(id=pk)

        if cartitem.cart.user and cartitem.cart.user != request.user:
            return Response(
                {"error": "Você não tem permissão para excluir este item"},
                status=status.HTTP_403_FORBIDDEN,
            )

        cartitem.delete()
        return Response(
            {"message": "Item do carrinho excluído com sucesso"},
            status=status.HTTP_204_NO_CONTENT,
        )
    except CartItem.DoesNotExist:
        return Response(
            {"error": "Item do carrinho não encontrado"},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def merge_carts(request):
    try:
        # Get the user cart
        user_cart, created = Cart.objects.get_or_create(user=request.user)
        if created:
            # Generate an unique code for cart
            import random
            import string

            user_cart.cart_code = "".join(
                random.choices(string.ascii_letters + string.digits, k=11)
            )
            user_cart.save()

        # Get the temporary cart (if exist)
        temp_cart_code = request.data.get("temp_cart_code")
        if temp_cart_code:
            try:
                temp_cart = Cart.objects.get(cart_code=temp_cart_code)
                # Move items from temporary cart to user cart
                for item in temp_cart.cartitems.all():
                    CartItem.objects.update_or_create(
                        cart=user_cart,
                        product=item.product,
                        defaults={"quantity": item.quantity},
                    )
                temp_cart.delete()
            except Cart.DoesNotExist:
                pass

        serializer = CartSerializer(user_cart)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
