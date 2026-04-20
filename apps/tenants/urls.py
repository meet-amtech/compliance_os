from rest_framework.routers import DefaultRouter
from .views import TenantViewSet

router = DefaultRouter()
router.register(r'tenant', TenantViewSet, basename='tenant')

urlpatterns = router.urls