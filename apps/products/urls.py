from django.urls import path
from . import views


urlpatterns = [
    # Product and Category
    path("", views.product_list, name="product_list"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    # Search
    path("search/", views.product_search, name="search"),
]
