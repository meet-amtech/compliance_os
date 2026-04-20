from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data['email'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

            # Block admin & super admin
            if user.is_superuser or user.is_staff:
                raise serializers.ValidationError(
                    "Admin users are not allowed to login via this API"
                )

        Blocked:
        - Django Admin users(is_staff)
        - Superusers(is_superuser)

        - Normal application users only allowed

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        refresh = RefreshToken.for_user(user)

        # Include tenant info in JWT
        if user.tenant:
            refresh['tenant_id'] = str(user.tenant.id)
            refresh['tenant_name'] = str(user.tenant.name)
            refresh['tenant_code'] = str(user.tenant.code)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }