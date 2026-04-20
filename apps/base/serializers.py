from rest_framework import serializers

class BaseSerializer(serializers.Serializer):
    """
    Standard serializer mixin/base for all models.
    Enforces read-only audit fields and standardizes validation errors.
    """
    class Meta:
        # Standard read-only fields for audit & tracking
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        if not attrs and self.instance:
            raise serializers.ValidationError("Empty update not allowed")
        return attrs

    def is_valid(self, raise_exception=False):
        try:
            return super().is_valid(raise_exception=raise_exception)
        except serializers.ValidationError as exc:
            raise serializers.ValidationError({
                "status": "error",
                "errors": exc.detail
            })
