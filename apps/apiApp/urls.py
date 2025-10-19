from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Authentication
    path(
        "auth/token/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", views.register, name="register"),
    path("auth/logout/", views.logout, name="logout"),
    path("auth/profile/", views.handle_profile, name="handle_profile"),
    path("auth/change-password/", views.change_password, name="change_password"),
    # Cart
    path("cart/", views.handle_cart, name="handle_cart"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/merge/", views.merge_carts, name="merge_carts"),
    path(
        "cart/update/", views.update_cartitem_quantity, name="update_cartitem_quantity"
    ),
    path("cart/item/<int:pk>/delete/", views.delete_cartitem, name="delete_cartitem"),
    # Product and Category
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<slug:slug>/", views.category_detail, name="category_detail"),
    # Wishlist
    path("wishlist/", views.get_user_wishlist, name="get_user_wishlist"),
    path(
        "wishlist/<int:pk>/delete/",
        views.delete_wishlist_item,
        name="delete_wishlist_item",
    ),
    path("wishlist/add/", views.add_to_wishlist, name="add_to_wishlist"),
    # Reviews
    path("reviews/add/", views.add_review, name="add_review"),
    path("reviews/<int:pk>/update/", views.update_review, name="update_review"),
    path("reviews/<int:pk>/delete/", views.delete_review, name="delete_review"),
    # Orders
    path("orders/create/", views.create_order, name="create_order"),
    path("orders/", views.get_user_orders, name="get_user_orders"),
    path("orders/<int:pk>/", views.get_order_detail, name="get_order_detail"),
    # Search
    path("search/", views.product_search, name="search"),
]
