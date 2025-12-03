from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Product,
    Category,
    Cart,
    CartItem,
    Review,
    Wishlist,
)





class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]


admin.site.register(Category, CategoryAdmin)

admin.site.register([Cart, CartItem, Review, Wishlist])
