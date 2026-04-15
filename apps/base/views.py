from rest_framework import viewsets

class BaseViewSet(viewsets.GenericViewSet):
    """
    Standard base viewset that guarantees consistent ordering if not explicitly provided.
    """
    def get_queryset(self):
        queryset = super().get_queryset()

        if not queryset.query.order_by:
            # If the queryset doesn't already have an ordering, enforce one.
            if hasattr(self.queryset.model, 'created_at'):
                return queryset.order_by('-created_at')
            else:
                return queryset.order_by('-pk')
        return queryset
