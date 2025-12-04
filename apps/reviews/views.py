from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from apps.products.models import Product


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
