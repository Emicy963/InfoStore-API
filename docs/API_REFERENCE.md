# 📖 API Reference

Complete API reference for InfoStore E-commerce API.

## Base URL

```
Production: https://infostore-api.onrender.com/api
Development: http://localhost:8000/api
```

## Authentication

All authenticated endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Token Lifetime

- **Access Token**: 1 hour
- **Refresh Token**: 7 days

---

## 🔐 Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /auth/register/`

**Authentication:** Not required

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "confirm_password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+244 923 456 789",
  "bi": "123456789LA001"
}
```

**Success Response:** `201 Created`

```json
{
  "message": "Novo usuário criado com sucesso."
}
```

**Error Response:** `400 Bad Request`
```json
{
  "email": ["Este email já está em uso."],
  "username": ["Este nome de usuário já está em uso."]
}
```

---

### Login (Obtain Tokens)

Authenticate and receive JWT tokens.

**Endpoint:** `POST /auth/token/`

**Authentication:** Not required

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

You can also use email instead of username:

```json
{
  "username": "john@example.com",
  "password": "SecurePass123"
}
```

**Success Response:** `200 OK`

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "username": "johndoe",
    "name": "John Doe"
  }
}
```

**Error Response:** `401 Unauthorized`

```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### Refresh Token

Get a new access token using refresh token.

**Endpoint:** `POST /auth/token/refresh/`

**Authentication:** Not required

**Request Body:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response:** `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Logout

Blacklist the refresh token.

**Endpoint:** `POST /auth/logout/`

**Authentication:** Required

**Request Body:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Success Response:** `200 OK`

```json
{
  "message": "Successfully logged out"
}
```

---

### Get User Profile

Retrieve authenticated user's profile.

**Endpoint:** `GET /auth/profile/`

**Authentication:** Required

**Success Response:** `200 OK`

```json
{
  "id": 1,
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone_number": "+244 923 456 789",
  "bi": "123456789LA001",
  "avatar_url": null
}
```

---

### Update User Profile

Update authenticated user's profile.

**Endpoint:** `PUT /auth/profile/`

**Authentication:** Required

**Request Body:**

```json
{
  "name": "John Smith",
  "email": "johnsmith@example.com",
  "phone": "+244 923 456 789",
  "address": "Rua 123, Luanda",
  "city": "Luanda"
}
```

**Success Response:** `200 OK`

```json
{
  "id": 1,
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Smith",
  "email": "johnsmith@example.com",
  "phone_number": "+244 923 456 789",
  "bi": "123456789LA001",
  "avatar_url": null
}
```

---

### Change Password

Change authenticated user's password.

**Endpoint:** `POST /auth/change-password/`

**Authentication:** Required

**Request Body:**

```json
{
  "current_password": "OldPass123",
  "new_password": "NewSecurePass456"
}
```

**Success Response:** `200 OK`

```json
{
  "message": "Senha alterada com sucesso."
}
```

**Error Response:** `400 Bad Request`

```json
{
  "error": "Senha atual incorreta."
}
```

---

## 🛍️ Product Endpoints

### List Products

Get paginated list of featured products.

**Endpoint:** `GET /products/`

**Authentication:** Not required

**Query Parameters:**

- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20, max: 100)

**Success Response:** `200 OK`

```json
{
  "count": 45,
  "next": "http://api.example.com/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "iPhone 15 Pro",
      "slug": "iphone-15-pro",
      "description": "Latest iPhone model...",
      "image": "http://example.com/media/product_img/iphone.jpg",
      "price": "1299.99",
      "average_rating": 4.5,
      "total_reviews": 128
    }
  ]
}
```

---

### Get Product Detail

Get detailed information about a specific product.

**Endpoint:** `GET /products/{slug}/`

**Authentication:** Not required

**Success Response:** `200 OK`

```json
{
  "id": 1,
  "name": "iPhone 15 Pro",
  "slug": "iphone-15-pro",
  "description": "The iPhone 15 Pro features...",
  "image": "http://example.com/media/product_img/iphone.jpg",
  "price": "1299.99"
}
```

**Error Response:** `404 Not Found`

```json
{
  "error": "Produto não encontrado."
}
```

---

### Search Products

Search products by name, description, or category.

**Endpoint:** `GET /search/`

**Authentication:** Not required

**Query Parameters:**

- `query` (required): Search term
- `page` (optional): Page number
- `page_size` (optional): Items per page

**Example:** `GET /search/?query=iphone&page=1`

**Success Response:** `200 OK`

```json
{
  "count": 12,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "iPhone 15 Pro",
      "slug": "iphone-15-pro",
      "description": "Latest iPhone model...",
      "image": "http://example.com/media/product_img/iphone.jpg",
      "price": "1299.99",
      "average_rating": 4.5,
      "total_reviews": 128
    }
  ]
}
```

---

## 📂 Category Endpoints

### List Categories

Get all product categories.

**Endpoint:** `GET /categories/`

**Authentication:** Not required

**Success Response:** `200 OK`

```json
[
  {
    "id": 1,
    "name": "Electronics",
    "image": "http://example.com/media/category_img/electronics.jpg",
    "slug": "electronics"
  },
  {
    "id": 2,
    "name": "Clothing",
    "image": "http://example.com/media/category_img/clothing.jpg",
    "slug": "clothing"
  }
]
```

---

### Get Category with Products

Get category details with all its products.

**Endpoint:** `GET /categories/{slug}/`

**Authentication:** Not required

**Success Response:** `200 OK`

```json
{
  "id": 1,
  "name": "Electronics",
  "image": "http://example.com/media/category_img/electronics.jpg",
  "products": [
    {
      "id": 1,
      "name": "iPhone 15 Pro",
      "slug": "iphone-15-pro",
      "description": "Latest iPhone model...",
      "image": "http://example.com/media/product_img/iphone.jpg",
      "price": "1299.99",
      "average_rating": 4.5,
      "total_reviews": 128
    }
  ]
}
```

---

## 🛒 Cart Endpoints

### Create Cart

Create a new cart (for anonymous or authenticated users).

**Endpoint:** `POST /cart/`

**Authentication:** Optional

**Request Body:** Empty `{}`

**Success Response:** `201 Created`

```json
{
  "data": {
    "id": 1,
    "cart_code": "abc123XYZ89",
    "cartitems": [],
    "cart_total": "0.00"
  },
  "message": "Carrinho de visitante criado com sucesso."
}
```

---

### Get Cart

Retrieve cart by code (anonymous) or user (authenticated).

**Endpoint:** `GET /cart/`

**Authentication:** Optional

**Query Parameters:**

- `code` (optional): Cart code for anonymous users

**Examples:**

- Anonymous: `GET /cart/?code=abc123XYZ89`
- Authenticated: `GET /cart/` (uses user's cart)

**Success Response:** `200 OK`

```json
{
  "id": 1,
  "cart_code": "abc123XYZ89",
  "cartitems": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "iPhone 15 Pro",
        "slug": "iphone-15-pro",
        "description": "Latest iPhone...",
        "image": "http://example.com/media/product_img/iphone.jpg",
        "price": "1299.99",
        "average_rating": 4.5,
        "total_reviews": 128
      },
      "quantity": 2,
      "sub_total": "2599.98"
    }
  ],
  "cart_total": "2599.98"
}
```

---

### Add to Cart

Add a product to cart.

**Endpoint:** `POST /cart/add/`

**Authentication:** Not required

**Request Body:**

```json
{
  "cart_code": "abc123XYZ89",
  "product_id": 1,
  "quantity": 2
}
```

**Success Response:** `200 OK`

```json
{
  "id": 1,
  "cart_code": "abc123XYZ89",
  "cartitems": [...],
  "cart_total": "2599.98"
}
```

---

### Update Cart Item Quantity

Update quantity of a cart item.

**Endpoint:** `PUT /cart/update/`

**Authentication:** Required

**Request Body:**

```json
{
  "item_id": 1,
  "quantity": 3
}
```

**Success Response:** `200 OK`

```json
{
  "data": {
    "id": 1,
    "product": {...},
    "quantity": 3,
    "sub_total": "3899.97"
  },
  "message": "Item do carrinho atualizado com sucesso!"
}
```

---

### Delete Cart Item

Remove an item from cart.

**Endpoint:** `DELETE /cart/item/{id}/delete/`

**Authentication:** Required

**Success Response:** `204 No Content`

```json
{
  "message": "Item do carrinho excluído com sucesso"
}
```

---

### Merge Carts

Merge anonymous cart into user cart after login.

**Endpoint:** `POST /cart/merge/`

**Authentication:** Required

**Request Body:**

```json
{
  "temp_cart_code": "abc123XYZ89"
}
```

**Success Response:** `200 OK`

```json
{
  "id": 2,
  "cart_code": "userCart123",
  "cartitems": [...],
  "cart_total": "4899.97"
}
```

---

## ⭐ Review Endpoints

### Add Review

Add a review for a product.

**Endpoint:** `POST /reviews/add/`

**Authentication:** Required

**Request Body:**

```json
{
  "product_id": 1,
  "rating": 5,
  "comment": "Excellent product! Highly recommended."
}
```

**Rating values:** 1 (Poor), 2 (Fair), 3 (Good), 4 (Very Good), 5 (Excellent)

**Success Response:** `201 Created`

```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone_number": "+244 923 456 789",
    "bi": "123456789LA001",
    "avatar_url": null
  },
  "rating": 5,
  "comment": "Excellent product! Highly recommended.",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

**Error Response:** `400 Bad Request`

```json
{
  "error": "Você já avaliou este produto"
}
```

---

### Update Review

Update an existing review.

**Endpoint:** `PUT /reviews/{id}/update/`

**Authentication:** Required (must be review owner or staff)

**Request Body:**

```json
{
  "rating": 4,
  "comment": "Updated comment: Still a great product!"
}
```

**Success Response:** `200 OK`

```json
{
  "id": 1,
  "user": {...},
  "rating": 4,
  "comment": "Updated comment: Still a great product!",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T11:45:00Z"
}
```

---

### Delete Review

Delete a review.

**Endpoint:** `DELETE /reviews/{id}/delete/`

**Authentication:** Required (must be review owner or staff)

**Success Response:** `204 No Content`

```json
{
  "message": "Avaliação excluída com sucesso"
}
```

---

## 💝 Wishlist Endpoints

### Get User Wishlist

Retrieve authenticated user's wishlist.

**Endpoint:** `GET /wishlist/`

**Authentication:** Required

**Success Response:** `200 OK`

```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com",
      "phone_number": "+244 923 456 789",
      "bi": "123456789LA001",
      "avatar_url": null
    },
    "product": {
      "id": 1,
      "name": "iPhone 15 Pro",
      "slug": "iphone-15-pro",
      "description": "Latest iPhone model...",
      "image": "http://example.com/media/product_img/iphone.jpg",
      "price": "1299.99",
      "average_rating": 4.5,
      "total_reviews": 128
    },
    "created_at": "2025-01-15T10:30:00Z"
  }
]
```

---

### Add/Remove Wishlist Item (Toggle)

Add or remove a product from wishlist. If product is already in wishlist, it will be removed.

**Endpoint:** `POST /wishlist/add/`

**Authentication:** Required

**Request Body:**

```json
{
  "product_id": 1
}
```

**Success Response (Added):** `201 Created`

```json
{
  "id": 1,
  "user": {...},
  "product": {...},
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Success Response (Removed):** `204 No Content`

```json
{
  "message": "Product removed from wishlist"
}
```

---

### Delete Wishlist Item

Remove a specific item from wishlist.

**Endpoint:** `DELETE /wishlist/{id}/delete/`

**Authentication:** Required

**Success Response:** `204 No Content`

---

## 📦 Order Endpoints

### Create Order

Create an order from user's cart.

**Endpoint:** `POST /orders/create/`

**Authentication:** Required

**Request Body:**

```json
{
  "payment_method": "multicaixa",
  "shipping_address": {
    "street": "Rua da Missão 123",
    "city": "Luanda",
    "province": "Luanda",
    "country": "Angola",
    "postal_code": "1000"
  },
  "notes": "Please deliver in the morning"
}
```

**Payment Methods:**

- `multicaixa`: Multicaixa Express
- `transferencia`: Transferência Bancária
- `dinheiro`: Dinheiro na Entrega

**Success Response:** `201 Created`

```json
{
  "id": 1,
  "message": "Pedido criado com sucesso."
}
```

**Error Response:** `400 Bad Request`

```json
{
  "error": "Seu carrinho está vazio."
}
```

---

### Get User Orders

Retrieve all orders for authenticated user.

**Endpoint:** `GET /orders/`

**Authentication:** Required

**Success Response:** `200 OK`

```json
[
  {
    "id": 1,
    "order_code": "ABC1234567",
    "status": "pending",
    "payment_method": "multicaixa",
    "total_amount": "2599.98",
    "shipping_address": {
      "street": "Rua da Missão 123",
      "city": "Luanda",
      "province": "Luanda",
      "country": "Angola",
      "postal_code": "1000"
    },
    "notes": "Please deliver in the morning",
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z",
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "iPhone 15 Pro",
          "slug": "iphone-15-pro",
          "description": "Latest iPhone model...",
          "image": "http://example.com/media/product_img/iphone.jpg",
          "price": "1299.99",
          "average_rating": 4.5,
          "total_reviews": 128
        },
        "quantity": 2,
        "price": "1299.99"
      }
    ]
  }
]
```

**Order Status Values:**

- `pending`: Pendente
- `processing`: Processando
- `shipped`: Enviado
- `delivered`: Entregue
- `cancelled`: Cancelado

---

### Get Order Detail

Retrieve details of a specific order.

**Endpoint:** `GET /orders/{id}/`

**Authentication:** Required

**Success Response:** `200 OK`

```json
{
  "id": 1,
  "order_code": "ABC1234567",
  "status": "pending",
  "payment_method": "multicaixa",
  "total_amount": "2599.98",
  "shipping_address": {
    "street": "Rua da Missão 123",
    "city": "Luanda",
    "province": "Luanda",
    "country": "Angola",
    "postal_code": "1000"
  },
  "notes": "Please deliver in the morning",
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z",
  "items": [
    {
      "id": 1,
      "product": {...},
      "quantity": 2,
      "price": "1299.99"
    }
  ]
}
```

**Error Response:** `404 Not Found`

```json
{
  "error": "Pedido não encontrado"
}
```

---

## 🔒 Error Responses

### Common Error Codes

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

### Error Response Format

```json
{
  "error": "Error message description"
}
```

Or for validation errors:

```json
{
  "field_name": ["Error message for this field"],
  "another_field": ["Another error message"]
}
```

---

## 📊 Rate Limiting

Currently, there are no rate limits on the API. However, Django Axes provides brute-force protection:

- **Failed login attempts**: 5 attempts before temporary lockout
- **Lockout duration**: 30 minutes

---

## 🔐 Security Headers

The API includes the following security headers in production:

- `Strict-Transport-Security`: HSTS enabled
- `X-Content-Type-Options`: nosniff
- `X-Frame-Options`: DENY
- `X-XSS-Protection`: Enabled

---

## 📝 Notes

### Pagination

List endpoints support pagination with the following parameters:

- `page`: Page number (starts at 1)
- `page_size`: Number of items per page (default: 20, max: 100)

### Date Format

All dates are in ISO 8601 format with UTC timezone:
```
2025-01-15T10:30:00Z
```

### Decimal Numbers

Prices and monetary values are returned as strings to preserve precision:

```json
"price": "1299.99"
```

### Images

Image URLs are absolute URLs pointing to the media server:
```
http://example.com/media/product_img/image.jpg
```

---

## 🧪 Testing

### Using cURL

```bash
# Login
curl -X POST https://infostore-api.com/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"SecurePass123"}'

# Get products (authenticated)
curl https://infostore-api.com/api/v1/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Create order
curl -X POST https://infostore-api.com/api/v1/orders/create/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_method": "multicaixa",
    "shipping_address": {
      "street": "Rua 123",
      "city": "Luanda",
      "province": "Luanda",
      "country": "Angola"
    }
  }'
```

### Using Postman

1. Import the API collection (if available)
2. Set environment variables:
   - `base_url`: Your API base URL
   - `access_token`: Your JWT access token
3. Use `{{base_url}}` and `{{access_token}}` in requests

### Using Python

```python
import requests

# Login
response = requests.post(
    'https://infostore-api.com/api/v1/auth/token/',
    json={'username': 'johndoe', 'password': 'SecurePass123'}
)
tokens = response.json()
access_token = tokens['access']

# Get products
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(
    'https://infostore-api.com/api/v1/products/',
    headers=headers
)
products = response.json()
```

---

## 📞 Support

For API support and questions:
- **GitHub Issues**: [Report issues](https://github.com/emicy963/infostore-api/issues)
- **Email**: [andersonpaulo931@gmail.com](andersonpaulo931@gmail.com)
- **Documentation**: [Full Documentation](https://github.com/emicy963/infostore-api)

---

**Last Updated:** Outubro 2025  
**API Version:** 1.1.1
