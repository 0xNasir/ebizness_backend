from rest_framework.routers import DefaultRouter

from sales.views import PromoAPIView, ApplyPromoAPIView, CartAPIView

app_name = 'sales'
router = DefaultRouter()
router.register('promo', PromoAPIView, basename='promo')
router.register('promo/apply', ApplyPromoAPIView, basename='apply_promo')
router.register('cart', CartAPIView, basename='cart')
urlpatterns = router.urls
