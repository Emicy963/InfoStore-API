from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Order, OrderItem
from apps.products.models import Product

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
                "country": "Testland",
            },
            "notes": "Please deliver between 9 AM and 5 PM.",
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


class OrderItemModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=49.99,
            shipping_address={
                "street": "123 Test St",
                "city": "Testville",
                "postal_code": "12345",
                "country": "Testland",
            },
            notes="Please deliver between 9 AM and 5 PM.",
        )
        self.product = Product.objects.create(
            name="ProductTest",
            description="Create the new product for test.",
            price=9.99,
        )
        self.order_item_data = {
            "order": self.order,
            "product": self.product,
            "price": 9.99,
        }

    def test_create_order_item(self):
        order_item = OrderItem.objects.create(**self.order_item_data)
        self.assertEqual(order_item.order.user.username, "testuser")
        self.assertEqual(order_item.order.user.email, "test@example.com")
        self.assertEqual(order_item.order.total_amount, 49.99)
        self.assertEqual(order_item.product.name, "ProductTest")
        self.assertEqual(
            order_item.product.description, "Create the new product for test."
        )
        self.assertEqual(order_item.product.price, 9.99)
        self.assertEqual(order_item.quantity, 1)
        self.assertEqual(
            str(order_item),
            f"{order_item.quantity} x {order_item.product.name} in order {order_item.order.order_code}",
        )

    def test_update_order_item_quantity(self):
        order_item = OrderItem.objects.create(**self.order_item_data)
        order_item.quantity = 5
        order_item.save()
        self.assertEqual(order_item.quantity, 5)
        self.assertEqual(
            str(order_item),
            f"{order_item.quantity} x {order_item.product.name} in order {order_item.order.order_code}",
        )
