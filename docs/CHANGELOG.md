# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-07

### 🎉 Major Release - Modular Architecture

This release represents a complete architectural overhaul from v1.x monolithic structure to a modular, maintainable codebase.

### ✨ Added

#### Modular App Structure
- **accounts**: User authentication, registration, profile management
- **products**: Product catalog, categories, search functionality
- **cart**: Shopping cart with anonymous and authenticated user support
- **orders**: Order processing and management
- **reviews**: Product reviews and ratings system
- **wishlist**: User wishlist functionality

#### Comprehensive Testing
- 102 unit tests covering all API endpoints
- Model tests for data integrity
- API endpoint tests for authentication, CRUD operations, and permissions
- Edge case and error handling tests
- Test coverage for all 6 apps

#### API Documentation
- Complete API endpoint documentation
- Request/response examples
- Authentication flow documentation
- Error response documentation

#### Security Enhancements
- JWT token blacklisting support
- Django Axes for brute-force protection
- Improved CORS configuration
- Production security headers
- Password validation improvements

### 🔄 Changed

#### Architecture
- **Breaking**: Migrated from single `apiApp` to 6 specialized apps
- **Breaking**: API versioning now uses `/api/v2/` prefix
- Improved code organization and separation of concerns
- Better maintainability and testability

#### Dependencies
- Updated Django to 4.2.23
- Updated djangorestframework to 3.15.2
- Added pytest and pytest-django for testing
- Added black for code formatting
- Removed unused dependencies

### 🐛 Fixed

- Fixed duplicate `staticfiles` key in STORAGES configuration
- Removed obsolete logger reference to deleted `apiApp`
- Fixed URL patterns ordering in products app
- Corrected serializer validation logic
- Fixed order model `payment_method` field defaults

### 📚 Documentation

- Updated README.md with v2.0 architecture
- Updated API_REFERENCE.md with v2 endpoints
- Updated QUICK_START.md for modular structure
- Created .env.example template
- Improved API endpoint documentation
- Added comprehensive testing guide

### 🔧 Configuration

- Improved .gitignore patterns
- Added pytest configuration
- Better environment variable management
- Production-ready settings

---

## [1.1.1] - 2025-10-17

### Added

- Initial release of InfoStore API
- User authentication with JWT tokens
- User registration and login (email or username)
- User profile management
- Password change functionality
- Product listing with pagination
- Product detail views
- Product search functionality
- Category management
- Shopping cart for anonymous and authenticated users
- Cart merging functionality
- Product reviews and ratings system
- Automatic product rating aggregation
- Wishlist functionality
- Order creation and management
- Multiple payment methods support
- Security features with Django Axes
- CORS configuration
- WhiteNoise for static file serving
- Comprehensive API documentation

### Security

- JWT token authentication
- Brute-force protection with Django Axes
- Secure password validation
- HTTPS enforcement in production
- CSRF protection
- Secure cookie settings

---

## [Unreleased]

### Planned

- Email notifications
- Order status tracking
- Admin dashboard enhancements
- Product inventory management
- Advanced filtering options
- Payment gateway integration (Stripe, PayPal)
- Invoice generation
- Customer support system
- Real-time notifications (WebSockets)

---

## Migration Guide v1 → v2

### For Developers

1. **Update API URLs**: All endpoints now use `/api/v2/` prefix instead of `/api/`
2. **App Structure**: Code is now organized in 6 specialized apps instead of single `apiApp`
3. **Testing**: Run tests with `pytest apps` instead of `python manage.py test`
4. **Environment**: Create `.env` file from `.env.example`
5. **Imports**: Update any imports from `apps.apiApp` to the specific new app names

### Database Migrations

```bash
python manage.py migrate
```

All migrations are backward compatible with existing data.

### API Changes

- Authentication endpoints moved to `/api/v2/auth/`
- Product endpoints moved to `/api/v2/product/`
- Cart endpoints moved to `/api/v2/cart/`
- Order endpoints moved to `/api/v2/order/`
- Review endpoints moved to `/api/v2/review/`
- Wishlist endpoints moved to `/api/v2/wishlist/`

---

**Full Changelog**: https://github.com/Emicy963/InfoStore-API/compare/v1.1.1...v2.0.0
