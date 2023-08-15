from rest_framework.routers import DefaultRouter

from store.views import BrandAPIView, CategoryAPIView, ProductAPIView

app_name = 'store'
router = DefaultRouter()
router.register('brand', BrandAPIView, basename='brand')
router.register('category', CategoryAPIView, basename='category')
router.register('product', ProductAPIView, basename='product')
urlpatterns = router.urls
