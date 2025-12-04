from django.urls import path
from . import views


urlpatterns = [
    # Cart
    path("", views.handle_cart, name="handle_cart"),
    path("add/", views.add_to_cart, name="add_to_cart"),
    path("merge/", views.merge_carts, name="merge_carts"),
    path("update/", views.update_cartitem_quantity, name="update_cartitem_quantity"),
    path("item/<int:pk>/delete/", views.delete_cartitem, name="delete_cartitem"),
]
