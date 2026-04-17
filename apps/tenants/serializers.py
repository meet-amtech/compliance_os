from rest_framework import serializers
from apps.base.serializers import BaseSerializer
from .models import Tenant


class TenantSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta(BaseSerializer.Meta):
        model = Tenant
        fields = '__all__'