from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Order, OrderItem
from apps.products.models import Product
from apps.cart.models import Cart, CartItem

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
        self.assertEqual(order.payment_method, "")  # Default is empty string
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


class OrdersAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        
        self.product1 = Product.objects.create(
            name="Product 1",
            description="First product",
            price=10.99
        )
        
        self.product2 = Product.objects.create(
            name="Product 2",
            description="Second product",
            price=20.99
        )
    
    def test_create_order_success(self):
        # Create cart with items
        cart = Cart.objects.create(user=self.user, cart_code="CART123")
        CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=cart, product=self.product2, quantity=1)
        
        self.client.force_authenticate(user=self.user)
        
        order_data = {
            "payment_method": "credit_card",
            "shipping_address": {
                "street": "123 Main St",
                "city": "Test City",
                "postal_code": "12345",
                "country": "Test Country"
            },
            "notes": "Please deliver in the morning"
        }
        
        response = self.client.post("/api/v2/order/create/", order_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertIn("message", response.data)
        
        # Verify order was created
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        
        # Verify cart was cleared
        cart.refresh_from_db()
        self.assertEqual(cart.cartitems.count(), 0)
    
    def test_create_order_empty_cart(self):
        # Create empty cart
        Cart.objects.create(user=self.user, cart_code="CART123")
        
        self.client.force_authenticate(user=self.user)
        
        order_data = {
            "payment_method": "credit_card",
            "shipping_address": {
                "street": "123 Main St",
                "city": "Test City",
                "postal_code": "12345",
                "country": "Test Country"
            },
            "notes": "Test"
        }
        
        response = self.client.post("/api/v2/order/create/", order_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
    
    def test_create_order_no_cart(self):
        self.client.force_authenticate(user=self.user)
        
        order_data = {
            "payment_method": "credit_card",
            "shipping_address": {
                "street": "123 Main St",
                "city": "Test City",
                "postal_code": "12345",
                "country": "Test Country"
            },
            "notes": "Test"
        }
        
        response = self.client.post("/api/v2/order/create/", order_data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)
    
    def test_create_order_unauthenticated(self):
        order_data = {
            "payment_method": "credit_card",
            "shipping_address": {
                "street": "123 Main St",
                "city": "Test City",
                "postal_code": "12345",
                "country": "Test Country"
            },
            "notes": "Test"
        }
        
        response = self.client.post("/api/v2/order/create/", order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_user_orders(self):
        # Create some orders
        Order.objects.create(
            user=self.user,
            total_amount=50.00,
            shipping_address={"street": "123 Main St"},
            payment_method="credit_card"
        )
        
        Order.objects.create(
            user=self.user,
            total_amount=75.00,
            shipping_address={"street": "456 Oak St"},
            payment_method="paypal"
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get("/api/v2/order/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_user_orders_filters_by_user(self):
        # Create order for this user
        Order.objects.create(
            user=self.user,
            total_amount=50.00,
            shipping_address={"street": "123 Main St"},
            payment_method="credit_card"
        )
        
        # Create order for another user
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123"
        )
        
        Order.objects.create(
            user=other_user,
            total_amount=100.00,
            shipping_address={"street": "789 Elm St"},
            payment_method="credit_card"
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get("/api/v2/order/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["total_amount"], "50.00")
    
    def test_get_user_orders_unauthenticated(self):
        response = self.client.get("/api/v2/order/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_order_detail_success(self):
        order = Order.objects.create(
            user=self.user,
            total_amount=50.00,
            shipping_address={"street": "123 Main St"},
            payment_method="credit_card"
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(f"/api/v2/order/{order.id}/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], order.id)
        self.assertEqual(response.data["total_amount"], "50.00")
    
    def test_get_order_detail_not_owner(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123"
        )
        
        order = Order.objects.create(
            user=other_user,
            total_amount=50.00,
            shipping_address={"street": "123 Main St"},
            payment_method="credit_card"
        )
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get(f"/api/v2/order/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_order_detail_not_found(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get("/api/v2/order/9999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_order_detail_unauthenticated(self):
        order = Order.objects.create(
            user=self.user,
            total_amount=50.00,
            shipping_address={"street": "123 Main St"},
            payment_method="credit_card"
        )
        
        response = self.client.get(f"/api/v2/order/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

