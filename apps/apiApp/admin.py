from django.contrib import admin
from .models import (
    Cart,
    CartItem,
    Review,
    Wishlist,
)

admin.site.register([Cart, CartItem, Review, Wishlist])
