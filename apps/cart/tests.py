from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Cart


User = get_user_model()

class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser123",
            email="test@example.com",
        )

        self.cart_data = {
            "user":self.user,
            "cart_code":"test123",
        }
    
    def test_create_cart(self):
        cart = Cart.objects.create(**self.cart_data)
        self.assertEqual(cart.user.username, "testuser123")
        self.assertEqual(cart.user.email, "test@example.com")
        self.assertEqual(cart.cart_code, "test123")
