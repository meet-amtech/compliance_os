from django.db import IntegrityError
from rest_framework import mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.access_control.models import Permission, Role
from apps.access_control.serializers import PermissionSerializer, RoleSerializer
from apps.base.views import BaseViewSet


class TenantScopedViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]

    def _get_user_tenant(self):
        tenant = getattr(self.request.user, "tenant", None)
        if tenant is None:
            raise ValidationError({"tenant": "Authenticated user is not assigned to a tenant."})
        return tenant

    def _handle_integrity_error(self, exc):
        raise ValidationError({"detail": "Constraint violation. Ensure unique values within tenant."}) from exc


class RoleViewSet(
    TenantScopedViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = RoleSerializer

    def get_queryset(self):
        tenant = self._get_user_tenant()
        return Role.objects.filter(tenant=tenant, is_deleted=False)

    def perform_create(self, serializer):
        tenant = self._get_user_tenant()
        try:
            serializer.save(tenant=tenant)
        except IntegrityError as exc:
            self._handle_integrity_error(exc)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError as exc:
            self._handle_integrity_error(exc)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PermissionViewSet(
    TenantScopedViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = PermissionSerializer

    def get_queryset(self):
        tenant = self._get_user_tenant()
        return Permission.objects.filter(tenant=tenant, is_deleted=False)

    def perform_create(self, serializer):
        tenant = self._get_user_tenant()
        try:
            serializer.save(tenant=tenant)
        except IntegrityError as exc:
            self._handle_integrity_error(exc)

    def perform_update(self, serializer):
        try:
            serializer.save()
        except IntegrityError as exc:
            self._handle_integrity_error(exc)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
