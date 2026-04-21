from django.urls import path
from .views import LoginAPIView, MeAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # User JWT login
    path('login/', LoginAPIView.as_view(), name='user-login'),

    # Get or update current authenticated user
    path('user/', MeAPIView.as_view(), name='user'),

    # JWT refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
