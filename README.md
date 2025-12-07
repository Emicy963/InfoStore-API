# 🛒 InfoStore - E-commerce REST API

A modern and robust REST API for e-commerce applications built with Django and Django REST Framework.

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](CHANGELOG.md)
![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-3.15-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> 📝 **Novidades da v2.0**: Confira todas as mudanças no [CHANGELOG.md](docs/CHANGELOG.md)

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🔐 Authentication & User Management

- JWT-based authentication with access and refresh tokens
- User registration and login (username or email)
- Profile management (view and update user information)
- Password change functionality
- Secure logout with token blacklisting

### 🛍️ Product Management

- Product listing with pagination
- Product detail views
- Product search functionality
- Category-based product filtering
- Product ratings and reviews system

### 🛒 Shopping Cart

- Anonymous cart support with unique cart codes
- Authenticated user carts
- Cart merging (anonymous to authenticated)
- Add, update, and remove cart items
- Real-time cart totals calculation

### ⭐ Reviews & Ratings

- Users can review products (one review per product)
- Star rating system (1-5 stars)
- Automatic product rating aggregation
- Review update and deletion

### 💝 Wishlist

- Add/remove products to wishlist
- View user wishlist
- Toggle wishlist items

### 📦 Order Management

- Create orders from cart
- Multiple payment methods (Multicaixa, Bank Transfer, Cash on Delivery)
- Order history
- Order detail views with items
- Automatic order code generation

### 🔒 Security Features

- Django Axes for brute-force protection
- CORS configuration
- Secure password validation
- HTTPS enforcement in production
- CSRF protection

## 🛠️ Tech Stack

- **Framework**: Django 4.2
- **API**: Django REST Framework 3.15
- **Authentication**: djangorestframework-simplejwt
- **Security**: django-axes, django-cors-headers
- **Image Processing**: Pillow
- **Environment Management**: django-environ
- **Production Server**: Gunicorn
- **Static Files**: WhiteNoise

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- pip
- virtualenv (recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/Emicy963/infostore-api.git
cd infostore
```

2. **Create and activate virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Environment variables**

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
FRONTEND_URL=http://localhost:3000
```

5. **Run migrations**

```bash
python manage.py migrate
```

6. **Create superuser**

```bash
python manage.py createsuperuser
```

7. **Run development server**

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/v2/`

## 📚 API Documentation

### Base URL

```
http://localhost:8000/api/v2/
```

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v2/auth/register/` | Register new user | No |
| POST | `/api/v2/auth/token/` | Login (obtain tokens) | No |
| POST | `/api/v2/auth/token/refresh/` | Refresh access token | No |
| POST | `/api/v2/auth/logout/` | Logout (blacklist token) | Yes |
| GET | `/api/v2/auth/profile/` | Get user profile | Yes |
| PUT | `/api/v2/auth/profile/` | Update user profile | Yes |
| POST | `/api/v2/auth/change-password/` | Change password | Yes |

### Product Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v2/product/` | List featured products | No |
| GET | `/api/v2/product/{slug}/` | Get product details | No |
| GET | `/api/v2/product/search/?query=` | Search products | No |

### Category Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v2/product/categories/` | List all categories | No |
| GET | `/api/v2/product/categories/{slug}/` | Get category with products | No |

### Cart Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v2/cart/` | Create cart | No |
| GET | `/api/v2/cart/` | Get cart (user or by code) | No |
| POST | `/api/v2/cart/add/` | Add item to cart | No |
| PUT | `/api/v2/cart/update/` | Update cart item quantity | Yes |
| DELETE | `/api/v2/cart/item/{id}/delete/` | Remove cart item | Yes |
| POST | `/api/v2/cart/merge/` | Merge anonymous cart to user | Yes |

### Review Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v2/review/add/` | Add product review | Yes |
| PUT | `/api/v2/review/{id}/update/` | Update review | Yes |
| DELETE | `/api/v2/review/{id}/delete/` | Delete review | Yes |

### Wishlist Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v2/wishlist/` | Get user wishlist | Yes |
| POST | `/api/v2/wishlist/add/` | Toggle wishlist item | Yes |
| DELETE | `/api/v2/wishlist/{id}/delete/` | Remove from wishlist | Yes |

### Order Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v2/order/create/` | Create order from cart | Yes |
| GET | `/api/v2/order/` | Get user orders | Yes |
| GET | `/api/v2/order/{id}/` | Get order details | Yes |

### Example Requests

**Register User**  

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "confirm_password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

**Login**  

```bash
curl -X POST http://localhost:8000/api/v2/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "SecurePass123"
  }'
```

**Get Products**  

```bash
curl http://localhost:8000/api/v2/product/
```

**Add to Cart**  

```bash
curl -X POST http://localhost:8000/api/v2/cart/add/ \
  -H "Content-Type: application/json" \
  -d '{
    "cart_code": "abc123xyz",
    "product_id": 1,
    "quantity": 2
  }'
```

## 🌐 Deployment

### Deploy to Render

1. **Push your code to GitHub**

2. **Create a new Web Service on Render**
   - Connect your GitHub repository
   - Choose the branch to deploy
   - Render will automatically detect the `render.yaml` file

3. **Set environment variables** (if not using render.yaml):
   - `SECRET_KEY`: Django secret key (auto-generated)
   - `DEBUG`: False
   - `ALLOWED_HOSTS`: .onrender.com
   - `FRONTEND_URL`: Your frontend URL
   - `PYTHON_VERSION`: 3.11.0

4. **Deploy**
   - Render will automatically run `build.sh`
   - Your API will be live at `https://your-app.onrender.com`

### Keep-Alive Service

The project includes a cron job configuration in `render.yaml` that pings the API every 10 minutes to prevent the free tier from sleeping.

Alternatively, you can use **UptimeRobot**:

1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Create a new monitor
3. Set URL to: `https://your-app.onrender.com/api/products/`
4. Set interval to 5 minutes

## 📁 Project Structure

```
infostore/
├── apps/
│   ├── accounts/          # User authentication & profiles
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # CustomUser model
│   │   ├── serializers.py # Registration, Profile, Token serializers
│   │   ├── tests.py       # 21 unit tests
│   │   ├── urls.py        # Auth endpoints
│   │   └── views.py       # Register, login, profile, logout
│   │
│   ├── products/          # Product catalog & categories
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # Product, Category models
│   │   ├── serializers.py # Product, Category serializers
│   │   ├── tests.py       # 17 unit tests
│   │   ├── urls.py        # Product, category, search endpoints
│   │   └── views.py       # List, detail, search views
│   │
│   ├── cart/              # Shopping cart management
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # Cart, CartItem models
│   │   ├── serializers.py # Cart serializers
│   │   ├── tests.py       # 20 unit tests
│   │   ├── urls.py        # Cart endpoints
│   │   └── views.py       # Add, update, delete, merge cart
│   │
│   ├── orders/            # Order processing
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # Order, OrderItem models
│   │   ├── serializers.py # Order serializers
│   │   ├── tests.py       # 14 unit tests
│   │   ├── urls.py        # Order endpoints
│   │   └── views.py       # Create, list, detail orders
│   │
│   ├── reviews/           # Product reviews & ratings
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py      # Review model
│   │   ├── serializers.py # Review serializers
│   │   ├── signals.py     # Update product rating on review
│   │   ├── tests.py       # 15 unit tests
│   │   ├── urls.py        # Review endpoints
│   │   └── views.py       # Add, update, delete reviews
│   │
│   └── wishlist/          # User wishlists
│       ├── migrations/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py      # Wishlist model
│       ├── serializers.py # Wishlist serializers
│       ├── tests.py       # 15 unit tests
│       ├── urls.py        # Wishlist endpoints
│       └── views.py       # Add, remove wishlist items
│
├── infostore/             # Project settings
│   ├── __init__.py
│   ├── settings.py        # Django configuration
│   ├── urls.py            # API v2 routing
│   ├── wsgi.py
│   └── asgi.py
│
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded files
├── staticfiles/           # Collected static files (production)
│
├── .env                   # Environment variables (not in git)
├── .env.example           # Environment template
├── .gitignore             # Git ignore rules
├── build.sh               # Production build script
├── CHANGELOG.md           # Version history
├── CONTRIBUTING.md        # Contribution guidelines  
├── LICENSE                # MIT License
├── manage.py              # Django management script
├── pytest.ini             # Pytest configuration
├── README.md              # This file
├── render.yaml            # Render deployment config
└── requirements.txt       # Python dependencies
```

## 🧪 Testing

InfoStore API has comprehensive test coverage with **102 unit tests** across all apps.

### Running Tests

```bash
# Run all tests
pytest apps

# Run tests for specific app
pytest apps/accounts
pytest apps/products
pytest apps/cart
pytest apps/orders
pytest apps/reviews
pytest apps/wishlist

# Run with coverage
pytest apps --cov

# Run with verbose output
pytest apps -v
```

### Test Coverage

- **accounts**: 21 tests (authentication, registration, profile, password changes)
- **products**: 17 tests (list, detail, categories, search)
- **cart**: 20 tests (create, add, update, delete, merge)
- **orders**: 14 tests (create, list, detail, permissions)
- **reviews**: 15 tests (add, update, delete, ratings)
- **wishlist**: 15 tests (add, remove, list, toggle)

All tests cover:

- ✅ Model creation and validation
- ✅ API endpoint responses
- ✅ Authentication and permissions
- ✅ Edge cases and error handling


## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Anderson Cafurica**  

- GitHub: [Emicy963](https://github.com/Emicy963)
- Email: [andersonpaulo931@gmail.com](andersonpaulo931@gmail.com)

## 🙏 Acknowledgments

- Django and DRF communities
- All contributors who help improve this project

---

⭐ If you found this project helpful, please consider giving it a star!
