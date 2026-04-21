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

class BaseViewSet(viewsets.ModelViewSet):

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant,
            created_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
