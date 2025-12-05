from django.test import TestCase
from .models import Category, Product

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category_data = {
            "name": "CategoryTest",
            # "slug": "categorytest",
        }
    
    def test_create_category(self):
        category = Category.objects.create(**self.category_data)
        self.assertEqual(category.name, "CategoryTest")
        self.assertEqual(category.slug, "categorytest")
