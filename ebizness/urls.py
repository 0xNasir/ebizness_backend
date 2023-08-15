from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from accounts.views import CustomObtainTokenPairView
from store.views import Home

schema_view = get_schema_view(
    openapi.Info(
        title="e-Business API",
        default_version='v1.0',
        description="e-Business is an online business solution with storefront and admin backend to manage product, "
                    "sales, order, etc.",
        terms_of_service="https://www.localhost:8000/policies/terms/",
        contact=openapi.Contact(email="contact@ebizness.io"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home.as_view()),
    path('v1/api/accounts/', include('accounts.urls', namespace='accounts')),
    path('v1/api/store/', include('store.urls', namespace='store')),
    path('v1/api/sales/', include('sales.urls', namespace='sales')),
    path('accounts/', include('rest_framework.urls', namespace='rest_urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('auth/token/', CustomObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = 'store.views.error_404_handler'
