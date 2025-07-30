from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Cart, CartItem, Review
from .serializers import ProducListSerializer, ProducDetailSerializer, CategoryListSerialiizer, CategoryDetailSerialiizer, CartSerializer, CartItemSerializer, ReviewSerializer

User = get_user_model()

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
    serializer = CategoryListSerialiizer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    serializer = CategoryDetailSerialiizer(category)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request):
    cart_code = request.data.get('cart_code')
    product_id = request.data.get('product_id')

    cart, created = Cart.objects.get_or_create(cart_code=cart_code)
    product = Product.objects.get(id=product_id)

    cartitem, created = CartItem.objects.get_or_create(product=product, cart=cart)
    cartitem.quantity = 1
    cartitem.save()

    serializer = CartSerializer(cart)
    return Response(serializer.data)

@api_view(['PUT'])
def update_cartitem_quantity(request):
    cartitem_id = request.data.get('item_id')
    quantity = request.data.get('quantity')

    quantity = int(quantity)

    cartitem = CartItem.objects.get(id=cartitem_id)
    cartitem.quantity = quantity
    cartitem.save()

    serializer = CartItemSerializer(cartitem)
    return Response({'data': serializer.data, 'message': 'CartItem updated sucessfully!'})

@api_view(['POST'])
def add_review(request):
    product_id = request.data.get('product_id')
    email = request.data.get('email')
    rating = request.data.get('rating')
    comment = request.data.get('comment')

    product = Product.objects.get(id=product_id)
    user = User.objects.get(email=email)

    if Review.objects.filter(product=product, user=user).exists():
        return Response({"error": "You have already reviewed this product"}, status=400)

    review = Review.objects.create(
        product=product, 
        user=user, 
        rating=rating, 
        comment=comment
        )
    serializer = ReviewSerializer(review)
    return Response(serializer.data)

@api_view(['PUT'])
def update_review(request, pk):
    review = Review.objects.get(id=pk)
    rating = request.data.get('rating')
    comment = request.data.get('comment')

    review.rating = rating
    review.comment = comment
    review.save()

    serializer = ReviewSerializer(review)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_review(request, pk):
    review = Review.objects.get(id=pk)
    review.delete()

    return Response('Review delete sucessfully', status=204)
