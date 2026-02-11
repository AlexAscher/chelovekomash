from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from shop.views import (
    CategoryViewSet,
    BrandViewSet,
    ProductViewSet,
    ProductImageViewSet,
)

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("brands", BrandViewSet)
router.register("products", ProductViewSet)
router.register("images", ProductImageViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),

    path("api/", include(router.urls)),
    path("api/users/", include("users.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
