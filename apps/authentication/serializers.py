from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Serializer to inject additional claims and perform extra validation.
    """
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        user = self.user
        
        # Superuser / staff may not have a tenant, but 
        if not user.tenant:
            raise AuthenticationFailed(
                _("User does not belong to any active tenant."),
                code="missing_tenant"
            )
        
        # Verify explicit user active status from our custom properties or built-in
        if not user.is_active:
            raise AuthenticationFailed(
                _("User account is inactive. Please contact support."),
                code="user_inactive"
            )

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the JWT payload
        token['email'] = user.email
        token['tenant_id'] = str(user.tenant.id) if user.tenant else None
        
        # Add role if exists
        token['role'] = getattr(user, 'role', None) if hasattr(user, 'role') else (
            "admin" if user.is_superuser or user.is_staff else "user"
        )

        return token
