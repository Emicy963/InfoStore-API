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


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="ProductTest",
            description="Create the new product for test.",
            price=9.99
        )
        self.category = Category.objects.create(name="CategoryTest")
    
    def test_create_product(self):
        self.assertEqual(self.product.name, "ProductTest")
        self.assertEqual(self.product.description, "Create the new product for test.")
        self.assertEqual(self.product.price, 9.99)
        self.assertEqual(self.product.slug, "producttest")
    
    def test_add_category(self):
        self.product.category = self.category
        self.assertEqual(self.product.category.name, "CategoryTest")
        self.assertEqual(self.product.category.slug, "categorytest")
    
    def test_is_not_featured(self):
        self.product.featured = False
        self.assertEqual(self.product.featured, False)
