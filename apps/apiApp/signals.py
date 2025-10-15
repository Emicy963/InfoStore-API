from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review, Product


@receiver(post_save, sender=Review)
def update_product_rating_on_save(sender, instance, **kwargs):
    product = instance.product
    reviews = product.reviews.all()

    # Update on Product
    product.total_reviews = reviews.count()
    product.average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0.0
    product.save()


@receiver(post_delete, sender=Review)
def update_product_rating_on_delete(sender, instance, **kwargs):
    product = instance.product
    reviews = product.reviews.all()

    # Update on Product
    product.total_reviews = reviews.count()
    product.average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0.0
    product.save()
