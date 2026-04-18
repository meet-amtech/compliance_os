from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'tenant',
            'is_active',
            'created_at'
        ]
        read_only_fields = ['id', 'tenant', 'created_at']