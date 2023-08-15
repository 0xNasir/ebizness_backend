from rest_framework.routers import DefaultRouter

from accounts.views import StaffProfileAPIView, CustomerProfileAPIView, ChangePasswordAPIView, RemoveFavouriteAPIView

app_name = 'accounts'
router = DefaultRouter()
router.register('staff', StaffProfileAPIView, basename='staff')
router.register('customer', CustomerProfileAPIView, basename='staff')
router.register('customer/favourites', RemoveFavouriteAPIView, basename='remove_favourite')
router.register('changePassword', ChangePasswordAPIView, basename='changePassword')
urlpatterns = router.urls
