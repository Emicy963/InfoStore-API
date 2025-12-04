from django.db import models
from django.conf import settings


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("processing", "Processando"),
        ("shipped", "Enviado"),
        ("delivered", "Entregue"),
        ("cancelled", "Cancelado"),
    ]

    PAYMENT_CHOICES = [
        ("multicaixa", "Multicaixa Express"),
        ("transferencia", "Transferência Bancária"),
        ("dinheiro", "Dinheiro na Entrega"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        blank=True,
        null=True,
    )
    order_code = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.JSONField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.order_code}"

    def save(self, *args, **kwargs):
        if not self.order_code:
            import random
            import string

            self.order_code = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=10)
            )
        super().save(*args, **kwargs)
