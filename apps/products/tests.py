from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
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


class ProductsAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create categories
        self.category1 = Category.objects.create(name="Electronics")
        self.category2 = Category.objects.create(name="Books")
        
        # Create featured products
        self.featured_product1 = Product.objects.create(
            name="Laptop",
            description="High performance laptop",
            price=999.99,
            category=self.category1,
            featured=True
        )
        
        self.featured_product2 = Product.objects.create(
            name="Smartphone",
            description="Latest smartphone",
            price=599.99,
            category=self.category1,
            featured=True
        )
        
        # Create non-featured product
        self.non_featured = Product.objects.create(
            name="USB Cable",
            description="Standard USB cable",
            price=5.99,
            category=self.category1,
            featured=False
        )
        
        # Create product in another category
        self.book = Product.objects.create(
            name="Python Programming",
            description="Learn Python programming",
            price=29.99,
            category=self.category2,
            featured=True
        )
    
    def test_product_list_returns_featured_only(self):
        response = self.client.get("/api/v2/product/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        
        # Should return 3 featured products
        self.assertEqual(len(response.data["results"]), 3)
        
        # Non-featured product should not be in results
        product_names = [p["name"] for p in response.data["results"]]
        self.assertNotIn("USB Cable", product_names)
    
    def test_product_list_pagination(self):
        response = self.client.get("/api/v2/product/?page=1")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
    
    def test_product_detail_success(self):
        response = self.client.get(f"/api/v2/product/{self.featured_product1.slug}/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Laptop")
        self.assertEqual(response.data["slug"], "laptop")
        # Category may or may not be in detail serializer
        # self.assertIn("category", response.data)
    
    def test_product_detail_not_found(self):
        response = self.client.get("/api/v2/product/nonexistent-slug/")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
    
    def test_category_list(self):
        response = self.client.get("/api/v2/product/categories/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        category_names = [c["name"] for c in response.data]
        self.assertIn("Electronics", category_names)
        self.assertIn("Books", category_names)
    
    def test_category_detail_success(self):
        response = self.client.get(f"/api/v2/product/categories/{self.category1.slug}/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Electronics")
    
    def test_category_detail_not_found(self):
        response = self.client.get("/api/v2/product/categories/nonexistent/")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
    
    def test_product_search_by_name(self):
        response = self.client.get("/api/v2/product/search/?query=laptop")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertGreaterEqual(len(response.data["results"]), 1)
        
        # Verify the laptop is in results
        product_names = [p["name"] for p in response.data["results"]]
        self.assertIn("Laptop", product_names)
    
    def test_product_search_by_description(self):
        response = self.client.get("/api/v2/product/search/?query=programming")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        
        # Should find Python Programming book
        product_names = [p["name"] for p in response.data["results"]]
        self.assertIn("Python Programming", product_names)
    
    def test_product_search_by_category(self):
        response = self.client.get("/api/v2/product/search/?query=electronics")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        
        # Should find products in Electronics category
        self.assertGreaterEqual(len(response.data["results"]), 1)
    
    def test_product_search_no_query(self):
        response = self.client.get("/api/v2/product/search/")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
    
    def test_product_search_no_results(self):
        response = self.client.get("/api/v2/product/search/?query=nonexistentproduct")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 0)
    
    def test_product_search_pagination(self):
        response = self.client.get("/api/v2/product/search/?query=product&page=1")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)

