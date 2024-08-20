from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

router.register(r'customer', views.CustomerViewSet)
router.register(r'driver', views.DriverViewSet)
router.register(r'support', views.StaffViewSet)

urlpatterns = [
    path('users/customer/login/', views.CustomerLoginView.as_view(), name="Customer login"),
    path('users/driver/login/', views.DriverLoginView.as_view(), name="Driver login"),
    path('users/support/login/', views.SupportLoginView.as_view(), name="Support login"),
    path('driver/unassignedDriver/', views.UnassignedDriverListAPIView.as_view(), name="Unassigned Drivers")
]

urlpatterns += router.urls

#urlpatterns = router.urls