from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'vehicles', views.VehicleViewSet)
router.register(r'booking', views.BookingViewSet)

urlpatterns = router.urls