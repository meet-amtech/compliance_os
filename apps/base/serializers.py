from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for all models.
    Handles:
    - Read-only audit fields
    - Common validation
    - Standard error format
    """

    class Meta:
        abstract = True
        read_only_fields = (
            'id',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by'
        )

    def validate(self, attrs):
        # Prevent empty update (PUT/PATCH with no data)
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