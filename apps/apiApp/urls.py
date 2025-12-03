from django.urls import path
from . import views

urlpatterns = [
    # Cart
    path("cart/", views.handle_cart, name="handle_cart"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/merge/", views.merge_carts, name="merge_carts"),
    path(
        "cart/update/", views.update_cartitem_quantity, name="update_cartitem_quantity"
    ),
    path("cart/item/<int:pk>/delete/", views.delete_cartitem, name="delete_cartitem"),
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
