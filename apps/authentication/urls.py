from django.urls import path
from .views import LoginAPIView, TenantLoginAPIView, MeAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # User JWT login
    path('login/', LoginAPIView.as_view(), name='user-login'),

    # Tenant JWT login
    path('tenant/login/', TenantLoginAPIView.as_view(), name='tenant-login'),

    # Get or update current authenticated user
    path('me/', MeAPIView.as_view(), name='me'),

    # JWT refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]