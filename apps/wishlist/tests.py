from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Wishlist
from apps.products.models import Product


User = get_user_model()


class WishlistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser123",
            email="test@example.com",
        )

        self.product = Product.objects.create(
            name="ProductTest",
            description="Create the new product for test.",
            price=9.99
        )

        self.wishlist_data = {
            "user": self.user,
            "product": self.product,
        }
    
    def test_create_wishlist(self):
        wishlist = Wishlist.objects.create(**self.wishlist_data)
        self.assertEqual(wishlist.user.username, "testuser123")
        self.assertEqual(wishlist.product.name, "ProductTest")
        self.assertEqual(str(wishlist), f"{self.user.username} - {self.product.name} in wishlist")
    
    def test_wishlist_unique_together(self):
        # Create first wishlist item
        Wishlist.objects.create(**self.wishlist_data)
        
        # Try to create duplicate wishlist item
        with self.assertRaises(Exception):
            Wishlist.objects.create(**self.wishlist_data)
    
    def test_wishlist_ordering(self):
        # Create multiple wishlist items
        product2 = Product.objects.create(
            name="ProductTest2",
            description="Second product for test.",
            price=19.99
        )
        
        wishlist1 = Wishlist.objects.create(**self.wishlist_data)
        
        wishlist2 = Wishlist.objects.create(
            user=self.user,
            product=product2
        )
        
        wishlists = Wishlist.objects.all()
        self.assertEqual(wishlists[0], wishlist2)  # Most recent first
        self.assertEqual(wishlists[1], wishlist1)


class WishlistAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username="testuser123",
            email="test@example.com",
            password="testpassword123"
        )
        
        self.product = Product.objects.create(
            name="ProductTest",
            description="Create the new product for test.",
            price=9.99
        )
        
        self.product2 = Product.objects.create(
            name="ProductTest2",
            description="Second product for test.",
            price=19.99
        )
    
    def test_add_to_wishlist_authenticated(self):
        self.client.force_authenticate(user=self.user)
        
        data = {
            "product_id": self.product.id
        }
        
        response = self.client.post("/api/v2/wishlist/add/", data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wishlist.objects.count(), 1)
        
        wishlist = Wishlist.objects.first()
        self.assertEqual(wishlist.user, self.user)
        self.assertEqual(wishlist.product, self.product)
    
    def test_add_to_wishlist_unauthenticated(self):
        data = {
            "product_id": self.product.id
        }
        
        response = self.client.post("/api/v2/wishlist/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_add_to_wishlist_toggle_behavior(self):
        """Test that adding the same product twice removes it (toggle behavior)"""
        self.client.force_authenticate(user=self.user)
        
        data = {
            "product_id": self.product.id
        }
        
        # First add - should create
        response = self.client.post("/api/v2/wishlist/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wishlist.objects.count(), 1)
        
        # Second add - should remove (toggle)
        response = self.client.post("/api/v2/wishlist/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wishlist.objects.count(), 0)
    
    def test_add_to_wishlist_product_not_found(self):
        self.client.force_authenticate(user=self.user)
        
        data = {
            "product_id": 9999
        }
        
        response = self.client.post("/api/v2/wishlist/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
    
    def test_get_user_wishlist_authenticated(self):
        self.client.force_authenticate(user=self.user)
        
        # Create wishlist items
        Wishlist.objects.create(user=self.user, product=self.product)
        Wishlist.objects.create(user=self.user, product=self.product2)
        
        response = self.client.get("/api/v2/wishlist/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_user_wishlist_unauthenticated(self):
        response = self.client.get("/api/v2/wishlist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_wishlist_empty(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get("/api/v2/wishlist/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_get_user_wishlist_filters_by_user(self):
        """Test that user only sees their own wishlist items"""
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123"
        )
        
        # Create wishlist items for both users
        Wishlist.objects.create(user=self.user, product=self.product)
        Wishlist.objects.create(user=other_user, product=self.product2)
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get("/api/v2/wishlist/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["product"]["id"], self.product.id)
    
    def test_delete_wishlist_item_authenticated(self):
        wishlist_item = Wishlist.objects.create(
            user=self.user,
            product=self.product
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f"/api/v2/wishlist/{wishlist_item.id}/delete/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Wishlist.objects.count(), 0)
    
    def test_delete_wishlist_item_unauthenticated(self):
        wishlist_item = Wishlist.objects.create(
            user=self.user,
            product=self.product
        )
        
        response = self.client.delete(f"/api/v2/wishlist/{wishlist_item.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_delete_wishlist_item_not_owner(self):
        """Test that user can only delete their own wishlist items"""
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123"
        )
        
        wishlist_item = Wishlist.objects.create(
            user=other_user,
            product=self.product
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f"/api/v2/wishlist/{wishlist_item.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Wishlist.objects.count(), 1)  # Item should still exist
    
    def test_delete_wishlist_item_not_found(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete("/api/v2/wishlist/9999/delete/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
