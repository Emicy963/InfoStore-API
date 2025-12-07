from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
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


class CartAPITest(TestCase):
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
    
    def test_create_cart_authenticated(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.post("/api/v2/cart/")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("cart_code", response.data)
        self.assertTrue(Cart.objects.filter(user=self.user).exists())
    
    def test_create_cart_anonymous(self):
        response = self.client.post("/api/v2/cart/")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("cart_code", response.data)
        
        # Cart should exist without user
        cart_code = response.data["cart_code"]
        self.assertTrue(Cart.objects.filter(cart_code=cart_code, user=None).exists())
    
    def test_get_cart_by_code(self):
        # Create cart
        cart = Cart.objects.create(cart_code="ABC123")
        
        response = self.client.get("/api/v2/cart/?code=ABC123")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cart_code"], "ABC123")
    
    def test_get_cart_by_code_not_found(self):
        response = self.client.get("/api/v2/cart/?code=NONEXISTENT")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cartitems"], [])
    
    def test_get_cart_authenticated_user(self):
        # Create cart for user
        cart = Cart.objects.create(user=self.user, cart_code="USER123")
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get("/api/v2/cart/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["cart_code"], "USER123")
    
    def test_get_cart_no_code_no_auth(self):
        response = self.client.get("/api/v2/cart/")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
    
    def test_add_to_cart_success(self):
        cart = Cart.objects.create(cart_code="CART123")
        
        data = {
            "cart_code": "CART123",
            "product_id": self.product1.id,
            "quantity": 2
        }
        
        response = self.client.post("/api/v2/cart/add/", data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CartItem.objects.filter(cart=cart, product=self.product1).count(), 1)
        
        cart_item = CartItem.objects.get(cart=cart, product=self.product1)
        self.assertEqual(cart_item.quantity, 2)
    
    def test_add_to_cart_increment_quantity(self):
        cart = Cart.objects.create(cart_code="CART123")
        CartItem.objects.create(cart=cart, product=self.product1, quantity=3)
        
        data = {
            "cart_code": "CART123",
            "product_id": self.product1.id,
            "quantity": 2
        }
        
        response = self.client.post("/api/v2/cart/add/", data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        cart_item = CartItem.objects.get(cart=cart, product=self.product1)
        self.assertEqual(cart_item.quantity, 5)  # 3 + 2
    
    def test_add_to_cart_invalid_cart(self):
        data = {
            "cart_code": "INVALID",
            "product_id": self.product1.id,
            "quantity": 1
        }
        
        response = self.client.post("/api/v2/cart/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_add_to_cart_invalid_product(self):
        cart = Cart.objects.create(cart_code="CART123")
        
        data = {
            "cart_code": "CART123",
            "product_id": 9999,
            "quantity": 1
        }
        
        response = self.client.post("/api/v2/cart/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_cartitem_quantity_success(self):
        cart = Cart.objects.create(user=self.user, cart_code="CART123")
        cart_item = CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        
        self.client.force_authenticate(user=self.user)
        
        data = {
            "item_id": cart_item.id,
            "quantity": 5
        }
        
        response = self.client.put("/api/v2/cart/update/", data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)
    
    def test_update_cartitem_invalid_quantity(self):
        cart = Cart.objects.create(user=self.user, cart_code="CART123")
        cart_item = CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        
        self.client.force_authenticate(user=self.user)
        
        data = {
            "item_id": cart_item.id,
            "quantity": 0
        }
        
        response = self.client.put("/api/v2/cart/update/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_cartitem_not_owner(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123"
        )
        
        cart = Cart.objects.create(user=other_user, cart_code="CART123")
        cart_item = CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        
        self.client.force_authenticate(user=self.user)
        
        data = {
            "item_id": cart_item.id,
            "quantity": 5
        }
        
        response = self.client.put("/api/v2/cart/update/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_cartitem_success(self):
        cart = Cart.objects.create(user=self.user, cart_code="CART123")
        cart_item = CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f"/api/v2/cart/item/{cart_item.id}/delete/")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())
    
    def test_delete_cartitem_not_owner(self):
        other_user = User.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password123"
        )
        
        cart = Cart.objects.create(user=other_user, cart_code="CART123")
        cart_item = CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(f"/api/v2/cart/item/{cart_item.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_merge_carts_success(self):
        # Create temporary cart
        temp_cart = Cart.objects.create(cart_code="TEMP123")
        CartItem.objects.create(cart=temp_cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=temp_cart, product=self.product2, quantity=1)
        
        self.client.force_authenticate(user=self.user)
        
        data = {
            "temp_cart_code": "TEMP123"
        }
        
        response = self.client.post("/api/v2/cart/merge/", data, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Temp cart should be deleted
        self.assertFalse(Cart.objects.filter(cart_code="TEMP123").exists())
        
        # User cart should have the items
        user_cart = Cart.objects.get(user=self.user)
        self.assertEqual(user_cart.cartitems.count(), 2)
    
    def test_merge_carts_no_temp_cart(self):
        self.client.force_authenticate(user=self.user)
        
        data = {
            "temp_cart_code": "NONEXISTENT"
        }
        
        response = self.client.post("/api/v2/cart/merge/", data, format="json")
        
        # Should still succeed and create user cart
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Cart.objects.filter(user=self.user).exists())

