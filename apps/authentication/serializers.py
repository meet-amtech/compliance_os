from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['email'],
            password=data['password']
        )

        # ❌ Invalid credentials
        if not user:
            raise AuthenticationFailed("Invalid credentials")

        # ❌ Block admin users
        if user.is_superuser or user.is_staff:
            raise AuthenticationFailed(
                "Admin users are not allowed to login via this API"
            )

        # ❌ Inactive user
        if not user.is_active:
            raise AuthenticationFailed("User is inactive")

        # ❌ Tenant check
        if not user.tenant:
            raise AuthenticationFailed("User is not assigned to any tenant")

        # ✅ Generate JWT
        refresh = RefreshToken.for_user(user)

        # ✅ Add tenant info in token
        refresh['tenant_id'] = str(user.tenant.id)
        refresh['tenant_name'] = str(user.tenant.name)
        refresh['tenant_code'] = str(user.tenant.code)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
class CustomTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['tenant_id'] = str(user.tenant.id) if user.tenant else None

        return token