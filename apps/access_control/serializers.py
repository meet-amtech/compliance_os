from rest_framework import serializers

from apps.base.serializers import BaseSerializer
from apps.access_control.models import Permission, Role


class RoleSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta(BaseSerializer.Meta):
        model = Role
        fields = ["id", "name", "tenant", "created_at", "updated_at", "created_by", "updated_by"]
        read_only_fields = BaseSerializer.Meta.read_only_fields + ["id", "tenant", "created_at", "updated_at", "created_by", "updated_by"]

    def validate_name(self, value):
        request = self.context.get("request")
        tenant = getattr(request.user, "tenant", None) if request else None
        if tenant is None:
            raise serializers.ValidationError("Authenticated user is not assigned to a tenant.")

        queryset = Role.objects.filter(name=value, tenant=tenant)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Role with this name already exists for this tenant.")
        return value


class PermissionSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta(BaseSerializer.Meta):
        model = Permission
        fields = [
            "id",
            "code",
            "name",
            "description",
            "tenant",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = ("id", "tenant", "created_at", "updated_at", "created_by", "updated_by")

    def validate_code(self, value):
        request = self.context.get("request")
        tenant = getattr(request.user, "tenant", None) if request else None
        if tenant is None:
            raise serializers.ValidationError("Authenticated user is not assigned to a tenant.")

        queryset = Permission.objects.filter(code=value, tenant=tenant)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError("Permission with this code already exists for this tenant.")
        return value
