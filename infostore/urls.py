from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.apiApp.urls")),
    path("api/v2/auth/", include("apps.accounts.urls")),
    path("api/v2/product/", include("apps.products.urls")),
    path("api/v2/cart/", include("apps.cart.urls")),
    path("api/v2/review/", include("apps.reviews.urls")),
    path("api/v2/wishlist/", include("apps.wishlist.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
