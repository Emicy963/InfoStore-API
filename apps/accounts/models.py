from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bi = models.CharField(
        "BI/Passaporte", max_length=30, blank=True, null=True, unique=True
    )
    avatar_url = models.URLField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, default="Angola")

    def __str__(self):
        return f"{self.username} ({self.email})"
