from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Tenant

class TenantLoginSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate(self, data):
        try:
            tenant = Tenant.objects.get(code=data['code'])
        except Tenant.DoesNotExist:
            raise serializers.ValidationError("Invalid tenant code")

        # Issue a JWT token that includes tenant info
        refresh = RefreshToken()
        refresh['tenant_id'] = str(tenant.id)
        refresh['tenant_code'] = tenant.code

        return {
            'tenant_id': str(tenant.id),
            'tenant_code': tenant.code,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class TenantSerializer(serializers.ModelSerializer):
        class Meta:
            model = Tenant
            fields = '__all__'