# ⚡ Quick Start Guide

Get your InfoStore API up and running in 10 minutes!

## 🎯 What You'll Need

- [ ] Python 3.11+ installed
- [ ] Git installed
- [ ] Code editor (VS Code recommended)
- [ ] Terminal/Command prompt

---

## 🚀 Local Development Setup

### Step 1: Clone & Setup

```bash
# Clone the repository
git clone https://github.com/emicy963/infostore-api.git
cd infostore-api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Configuration

```bash
# Copy environment example
cp .env.example .env

# Edit .env file with your settings
# Minimum required:
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
FRONTEND_URL=http://localhost:3000
```

**Generate a secure SECRET_KEY:**

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 3: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
# Follow the prompts to set username, email, and password
```

### Step 4: Load Sample Data (Optional)

Create some test data through Django admin:

```bash
# Start the server
python manage.py runserver

# Open browser and go to: http://localhost:8000/admin
# Login with superuser credentials
# Add some categories and products
```

### Step 5: Test the API

```bash
# API is running at: http://localhost:8000/api/v2/

# Test endpoints:
# Products: http://localhost:8000/api/v2/product/
# Categories: http://localhost:8000/api/v2/product/categories/
# Register: POST http://localhost:8000/api/v2/auth/register/
```

---

## 🌐 Deploy to Render (Production)

### Step 1: Prepare Repository

```bash
# Make sure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

**Required files checklist:**
- [x] `requirements.txt`
- [x] `build.sh` (make it executable)
- [x] `render.yaml`
- [x] `.gitignore` (don't commit .env)

```bash
# Make build.sh executable (important!)
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 3: Deploy Using Blueprint

1. **Click "New +" → "Blueprint"**
2. **Connect your repository**
   - Select: `infostore`
   - Branch: `main`
3. **Review Services**
   - Web Service: `infostore-api`
   - Cron Job: `infostore-keepalive`
4. **Click "Apply"**

Render will automatically:

- Detect `render.yaml`
- Set up environment variables
- Run build script
- Deploy your API

### Step 4: Configure Environment Variables

If using manual setup (not blueprint):

1. Go to your web service
2. Click "Environment"
3. Add variables:

   ```
   SECRET_KEY = (Auto-generate)
   DEBUG = False
   ALLOWED_HOSTS = .onrender.com
   FRONTEND_URL = https://your-frontend.com
   PYTHON_VERSION = 3.15.3
   ```

### Step 5: Wait for Deployment

- First deployment takes 5-10 minutes
- Watch the logs for any errors
- Your API will be live at: `https://infostore-api.onrender.com`

### Step 6: Update Cron Job URL

1. Go to your cron job service
2. Update the start command with your actual URL:

   ```bash
   curl https://infostore-api.onrender.com/api/v2/product/
   ```

### Step 7: Test Production API

```bash
# Test your live API
curl https://infostore-api.onrender.com/api/v2/product/

# Expected response: List of products with pagination
```

---

## 🔧 Common Setup Issues

### Issue: `pip install` fails

**Solution:**

```bash
# Upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: `SECRET_KEY` error

**Solution:**

```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Add it to your .env file
```

### Issue: Database errors

**Solution:**

```bash
# Delete database and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: `build.sh: Permission denied` on Render

**Solution:**

```bash
# Make build.sh executable locally
git update-index --chmod=+x build.sh
git commit -m "Fix build.sh permissions"
git push
```

### Issue: CORS errors in frontend

**Solution:**
Add your frontend URL to `settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend-url.com"  # Add this
]
```

---

## 📱 Next Steps After Setup

### 1. Add Sample Data

```bash
python manage.py shell

from apps.products.models import Category, Product

# Create category
category = Category.objects.create(name="Electronics")

# Create product
Product.objects.create(
    name="iPhone 15 Pro",
    description="Latest iPhone model with amazing features",
    price=1299.99,
    category=category,
    featured=True
)
```

### 2. Test All Endpoints

```bash
# Register a user
curl -X POST http://localhost:8000/api/v2/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123",
    "confirm_password": "TestPass123",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:8000/api/v2/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123"
  }'
```

### 3. Set Up Keep-Alive (Choose one)

**Option A: Render Cron Job (Already configured in render.yaml)**  

```yaml
# Already in render.yaml
- type: cron
  name: infostore-keepalive
  schedule: "*/10 * * * *"
  startCommand: "curl https://your-app.onrender.com/api/v2/product/"
```

**Option B: UptimeRobot (Free alternative)**  

1. Sign up at [uptimerobot.com](https://uptimerobot.com)
2. Add new monitor:
   - Type: HTTP(s)
   - URL: `https://your-app.onrender.com/api/v2/product/`
   - Interval: 5 minutes

### 4. Update Frontend

Update your frontend to use the production API:

```javascript
// In your frontend config
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? 'https://infostore-api.onrender.com/api/v2'
  : 'http://localhost:8000/api/v2';
```

---

## 🎓 Learning Resources

### Essential Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Render Documentation](https://render.com/docs)

### Useful Tutorials

- Django REST Framework Tutorial: [Official Guide](https://www.django-rest-framework.org/tutorial/quickstart/)
- JWT Authentication: [SimpleJWT Docs](https://django-rest-framework-simplejwt.readthedocs.io/)

---

## 🆘 Getting Help

**Found a bug?**
[Open an issue](https://github.com/yourusername/infostore/issues)

**Have a question?**
Check the [API Reference](API_REFERENCE.md) or [Full README](README.md)

**Need deployment help?**
See [Deployment Guide](DEPLOYMENT.md)

---

## ✅ Deployment Checklist

Before going live:

- [ ] All tests pass locally
- [ ] Environment variables are set
- [ ] `DEBUG = False` in production
- [ ] Secret key is secure and random
- [ ] CORS origins are configured
- [ ] Static files are collected
- [ ] Database migrations are up to date
- [ ] Keep-alive service is configured
- [ ] API endpoints are tested
- [ ] Documentation is updated
- [ ] Frontend is pointing to production API

---

## 🎉 You're All Set

Your InfoStore API is now running! Start building your e-commerce frontend or mobile app.

**API Base URL (Local):** `http://localhost:8000/api/v2/`  
**API Base URL (Production):** `https://infostore-api.onrender.com/api/v2/`

**Admin Panel:** `http://localhost:8000/admin/`

Happy coding! 🚀
