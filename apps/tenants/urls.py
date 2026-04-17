from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TenantViewSet, TenantLoginAPIView

router = DefaultRouter()
router.register('', TenantViewSet, basename='tenant')

urlpatterns = [
    path('login/', TenantLoginAPIView.as_view(), name='tenant-login'),
]

urlpatterns += router.urls