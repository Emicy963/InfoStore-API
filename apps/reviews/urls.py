from django.urls import path
from . import views


urlpatterns = [
    # Reviews
    path("add/", views.add_review, name="add_review"),
    path("<int:pk>/update/", views.update_review, name="update_review"),
    path("<int:pk>/delete/", views.delete_review, name="delete_review"),
]
