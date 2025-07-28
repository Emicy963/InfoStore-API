from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Product

class CustomAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name','last_name')

admin.site.register(CustomUser, CustomAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'featured')

admin.site.register(Product, ProductAdmin)
