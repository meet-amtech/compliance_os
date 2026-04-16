from rest_framework import mixins
from apps.base.views import BaseViewSet
from .models import Tenant
from .serializers import TenantSerializer


class TenantViewSet(
    BaseViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer