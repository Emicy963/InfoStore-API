from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path("api/token/", views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", views.register, name="register"),
    path("api/logout/", views.logout, name="logout"),
    path("profile/", views.get_user_profile, name="user_profile"),
    # Product and Category
    path("product_list", views.product_list, name="product_list"),
    path("products/<slug:slug>", views.product_detail, name="product_detail"),
    path("category_list", views.category_list, name="category_list"),
    path("categories/<slug:slug>", views.category_detail, name="category_deatil"),
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/<str:cart_code>/", views.get_cart, name="get_cart"),
    path(
        "update_cartitem_quantity/",
        views.update_cartitem_quantity,
        name="update_cartitem_quantity",
    ),
    path("add_review/", views.add_review, name="add_review"),
    path("update_review/<int:pk>/", views.update_review, name="update_review"),
    path("delete_review/<int:pk>/", views.delete_review, name="delete_review"),
    path("delete_cartitem/<int:pk>/", views.delete_cartitem, name="delete_cartitem"),
    path("add_to_wishlist/", views.add_to_wishlist, name="add_to_wishlist"),
    path("search/", views.product_search, name="search"),
]
