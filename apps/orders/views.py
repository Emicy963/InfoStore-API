from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import CreateOrderSerializer, OrderSerializer
from apps.cart.models import Cart


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    try:
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            # Get user cart
            try:
                cart = Cart.objects.get(user=request.user)
                if not cart.cartitems.exists():
                    return Response(
                        {"error": "Seu carrinho está vazio."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except Cart.DoesNotExist:
                return Response(
                    {"error": "Carrinho não encontrado."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            total = sum(
                item.product.price * item.quantity for item in cart.cartitems.all()
            )

            order = Order.objects.create(
                user=request.user,
                payment_method=serializer.validated_data["payment_method"],
                total_amount=total,
                shipping_address=serializer.validated_data["shipping_address"],
                notes=serializer.validated_data["notes"],
            )

            for item in cart.cartitems.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

            cart.cartitems.all().delete()

            return Response(
                {"id": order.id, "message": "Pedido criado com sucesso."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    try:
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response(
            {"error": "Pedido não encontrado"}, status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
