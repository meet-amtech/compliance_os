from django.urls import path
from .views import MeAPIView

urlpatterns = [
    path('user/', MeAPIView.as_view(), name='user'),
]