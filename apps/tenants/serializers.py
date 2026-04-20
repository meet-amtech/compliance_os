from rest_framework import serializers
from apps.base.serializers import BaseSerializer
from .models import Tenant


class TenantSerializer(BaseSerializer, serializers.ModelSerializer):
    
    class Meta(BaseSerializer.Meta):
        model = Tenant
        fields = ['id', 'name', 'code', 'plan', 'timezone', 'settings_json']
        read_only_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by', 'plan')