from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# upload doc
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('tenants/', include('apps.tenants.urls')),
    path('api/auth/', include('apps.authentication.urls')),

    # JWT AUTH (STANDARD)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #frameworks
    path('api/frameworks/', include('apps.frameworks.urls')),
]

# if settings.DEBUG:

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)