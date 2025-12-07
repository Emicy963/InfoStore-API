from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Review
from apps.products.models import Product


User = get_user_model()


class ReviewModelTest(TestCase):
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

        self.review_data = {
            "product": self.product,
            "user": self.user,
            "rating": 5,
            "comment": "Excellent product!"
        }
    
    def test_create_review(self):
        review = Review.objects.create(**self.review_data)
        self.assertEqual(review.user.username, "testuser123")
        self.assertEqual(review.product.name, "ProductTest")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent product!")
        self.assertEqual(str(review), f"{self.user.username}'s review of {self.product.name}")
    
    def test_review_unique_together(self):
        # Create first review
        Review.objects.create(**self.review_data)
        
        # Try to create duplicate review
        with self.assertRaises(Exception):
            Review.objects.create(**self.review_data)
    
    def test_review_ordering(self):
        # Create multiple reviews
        user2 = User.objects.create_user(
            username="testuser456",
            email="test2@example.com",
        )
        
        review1 = Review.objects.create(**self.review_data)
        
        review2 = Review.objects.create(
            product=self.product,
            user=user2,
            rating=4,
            comment="Good product"
        )
        
        reviews = Review.objects.all()
        self.assertEqual(reviews[0], review2)  # Most recent first
        self.assertEqual(reviews[1], review1)


class ReviewAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username="testuser123",
            email="test@example.com",
            password="testpassword123"
        )
        
        self.staff_user = User.objects.create_user(
            username="staffuser",
            email="staff@example.com",
            password="staffpassword123",
            is_staff=True
        )
        
        self.product = Product.objects.create(
            name="ProductTest",
            description="Create the new product for test.",
            price=9.99
        )
    
    def test_add_review_authenticated(self):
        self.client.force_authenticate(user=self.user)
        
        data = {
            "product_id": self.product.id,
            "rating": 5,
            "comment": "Excellent product!"
        }
        
        response = self.client.post("/api/v2/review/add/", data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        
        review = Review.objects.first()
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.rating, 5)
    
    def test_add_review_unauthenticated(self):
        data = {
            "product_id": self.product.id,
            "rating": 5,
            "comment": "Excellent product!"
        }
        
        response = self.client.post("/api/v2/review/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_add_review_duplicate(self):
        self.client.force_authenticate(user=self.user)
        
        # Create first review
        Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="First review"
        )
        
        # Try to add duplicate
        data = {
            "product_id": self.product.id,
            "rating": 4,
            "comment": "Second review"
        }
        
        response = self.client.post("/api/v2/review/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
    
    def test_add_review_product_not_found(self):
        self.client.force_authenticate(user=self.user)
        
        data = {
            "product_id": 9999,
            "rating": 5,
            "comment": "Test"
        }
        
        response = self.client.post("/api/v2/review/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_review_owner(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            comment="Initial review"
        )
        
        self.client.force_authenticate(user=self.user)
        
        data = {
            "rating": 5,
            "comment": "Updated review"
        }
        
        response = self.client.put(f"/api/v2/review/{review.id}/update/", data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Updated review")
    
    def test_update_review_not_owner(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            comment="Initial review"
        )
        
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123"
        )
        
        self.client.force_authenticate(user=other_user)
        
        data = {
            "rating": 5,
            "comment": "Updated review"
        }
        
        response = self.client.put(f"/api/v2/review/{review.id}/update/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_review_staff(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=3,
            comment="Initial review"
        )
        
        self.client.force_authenticate(user=self.staff_user)
        
        data = {
            "rating": 5,
            "comment": "Updated by staff"
        }
        
        response = self.client.put(f"/api/v2/review/{review.id}/update/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_review_not_found(self):
        self.client.force_authenticate(user=self.user)
        
        data = {
            "rating": 5,
            "comment": "Updated review"
        }
        
        response = self.client.put("/api/v2/review/9999/update/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_review_owner(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Test review"
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f"/api/v2/review/{review.id}/delete/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)
    
    def test_delete_review_not_owner(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Test review"
        )
        
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123"
        )
        
        self.client.force_authenticate(user=other_user)
        
        response = self.client.delete(f"/api/v2/review/{review.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_review_staff(self):
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=5,
            comment="Test review"
        )
        
        self.client.force_authenticate(user=self.staff_user)
        
        response = self.client.delete(f"/api/v2/review/{review.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_delete_review_not_found(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete("/api/v2/review/9999/delete/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
