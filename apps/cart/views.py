from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer
from apps.products.models import Product


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def handle_cart(request):
    """
    Endpoint unify for create and get cart.
    - POST: Create a cart (anonymos or user).
    - GET: Get cart (anonymos with ?code= or auth user).
    """
    if request.method == "POST":
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            if created:
                import random
                import string

                cart.cart_code = "".join(
                    random.choices(string.ascii_letters + string.digits, k=11)
                )
                cart.save()
        else:
            import random
            import string

            cart_code = "".join(
                random.choices(string.ascii_letters + string.digits, k=11)
            )
            cart = Cart.objects.create(cart_code=cart_code)

        serializer = CartSerializer(cart)
        return Response(
            serializer.data,
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
                return Response({"cartitems": [], "cart_code": cart_code})

        elif request.user.is_authenticated:
            try:
                cart = Cart.objects.filter(user=request.user).first()
                if not cart:
                    cart = Cart.objects.create(user=request.user)
                    import random
                    import string

                    cart.cart_code = "".join(
                        random.choices(string.ascii_letters + string.digits, k=11)
                    )
                    cart.save()
                serializer = CartSerializer(cart)
                return Response(serializer.data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
        # Buscar ou criar o carrinho
        cart = Cart.objects.get(cart_code=cart_code)
        product = Product.objects.get(id=product_id)

        # Buscar ou criar o item do carrinho
        cartitem, created = CartItem.objects.get_or_create(
            product=product, cart=cart, defaults={"quantity": 0}
        )

        if created:
            cartitem.quantity = quantity
        else:
            cartitem.quantity += quantity

        cartitem.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Cart.DoesNotExist:
        return Response(
            {"error": "Carrinho não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )
    except Product.DoesNotExist:
        return Response(
            {"error": "Produto não encontrado."}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
