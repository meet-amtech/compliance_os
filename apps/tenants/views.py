from rest_framework import mixins
from apps.base.views import BaseViewSet
from .models import Tenant
from .serializers import TenantSerializer
from rest_framework.permissions import IsAuthenticated


class TenantViewSet(
    BaseViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
):
    serializer_class = TenantSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return Tenant.objects.filter(id=user.tenant_id)
