from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Order

User = get_user_model()

class OrderModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
        )

        self.order_data = {
            "user": self.user,
            "total_amount": 49.99,
            "shipping_address": {
                "street": "123 Test St",
                "city": "Testville",
                "postal_code": "12345",
                "country": "Testland"
            },
            "notes": "Please deliver between 9 AM and 5 PM."
        }

    def test_create_order(self):
        order = Order.objects.create(**self.order_data)
        self.assertEqual(order.user.username, "testuser")
        self.assertEqual(order.user.email, "test@example.com")
        self.assertEqual(order.payment_method, "pending")
        self.assertEqual(order.total_amount, 49.99)
        self.assertEqual(order.shipping_address["street"], "123 Test St")
        self.assertEqual(order.notes, "Please deliver between 9 AM and 5 PM.")
        self.assertIsNotNone(order.order_code)
        self.assertEqual(str(order), f"Pedido #{order.order_code}")
    
    
