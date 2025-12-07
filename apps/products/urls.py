from django.urls import path
from . import views


urlpatterns = [
    # Product and Category
    path("", views.product_list, name="product_list"),
    # Search MUST come before slug pattern
    path("search/", views.product_search, name="search"),
    # Categories MUST come before slug pattern
    path("categories/", views.category_list, name="category_list"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    # Generic slug pattern LAST to avoid capturing specific routes
    path("<slug:slug>/", views.product_detail, name="product_detail"),
]
