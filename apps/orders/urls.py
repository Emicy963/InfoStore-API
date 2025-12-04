from django.urls import path
from . import views

urlpatterns = [
    # Orders
    path("", views.get_user_orders, name="get_user_orders"),
    path("create/", views.create_order, name="create_order"),
    path("<int:pk>/", views.get_order_detail, name="get_order_detail"),
]
