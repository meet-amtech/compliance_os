from rest_framework import serializers
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = '__all__'

        def create(self, validated_data):
            tenant = super().create(validated_data)

            # default settings
            tenant.settings_json = {
                "theme": "light",
                "notifications": True
            }
            tenant.save()

            return tenant