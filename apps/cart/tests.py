from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Cart, CartItem
from apps.products.models import Product


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


class CartItemModelTest(TestCase):
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

        self.cart = Cart.objects.create(
            user=self.user,
            cart_code="cart123",
        )
        
        self.cart_item_data = {
            "cart": self.cart,
            "product": self.product,
        }
    
    def test_create_cart_item(self):
        cart_item = CartItem.objects.create(**self.cart_item_data)
        self.assertEqual(cart_item.cart.user.username, "testuser123")
        self.assertEqual(cart_item.cart.user.email, "test@example.com")
        self.assertEqual(cart_item.cart.cart_code, "cart123")
        self.assertEqual(cart_item.product.name, "ProductTest")
        self.assertEqual(cart_item.product.description, "Create the new product for test.")
        self.assertEqual(cart_item.product.price, 9.99)
        self.assertEqual(cart_item.quantity, 1)
        self.assertEqual(str(cart_item), f"{cart_item.quantity} x {cart_item.product.name} in cart {cart_item.cart.cart_code}")
    
    def test_update_cart_item_quantity(self):
        cart_item = CartItem.objects.create(**self.cart_item_data)
        cart_item.quantity = 10
        self.assertNotEqual(cart_item.quantity, 1)
