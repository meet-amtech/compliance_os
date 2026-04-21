from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from apps.base.views import BaseViewSet
from .models import Framework, Obligation, Clause, Control
from .serializers import (
    FrameworkSerializer,
    ObligationSerializer,
    ClauseSerializer,
    ControlSerializer
)
from rest_framework.exceptions import ValidationError

class FrameworkViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Framework.objects.all()
    serializer_class = FrameworkSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]         #upload

    def get_queryset(self):
        serializer.save(
            tenant=self.request.user.tenant,
            is_active=True  # force active
        )
        return Framework.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant,
            created_by=self.request.user
        )
        user = self.request.user

        if not user or not user.is_authenticated:
            raise ValidationError("User not authenticated")

        if not user.tenant:
            raise ValidationError("User is not assigned to any tenant")

        serializer.save(tenant=user.tenant)

class ObligationViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Obligation.objects.all()
    serializer_class = ObligationSerializer
    permission_classes = [IsAuthenticated]


class ClauseViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Clause.objects.all()
    serializer_class = ClauseSerializer
    permission_classes = [IsAuthenticated]


class ControlViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Control.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        print("🔥 perform_create called")
        print("USER:", self.request.user)
        print("TENANT:", self.request.user.tenant)

        serializer.save(
            tenant=self.request.user.tenant,
            created_by=self.request.user
        )