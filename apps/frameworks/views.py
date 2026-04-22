from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from apps.base.views import BaseViewSet
from .models import Framework, Obligation, Clause, Control, Evidence
from .serializers import (
    FrameworkSerializer,
    ObligationSerializer,
    ClauseSerializer,
    ControlSerializer
)
from rest_framework.exceptions import ValidationError
from .serializers import EvidenceSerializer

# -------------------- Framework --------------------
class FrameworkViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Framework.objects.all()
    serializer_class = FrameworkSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # upload

    def get_queryset(self):
        serializer.save(
            tenant=self.request.user.tenant,
            is_active=True  # force active
        )
        return Framework.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):

        user = self.request.user

        if not user or not user.is_authenticated:
            raise ValidationError("User not authenticated")

        if not user.tenant:
            raise ValidationError("User is not assigned to any tenant")

        serializer.save(tenant=user.tenant)

        serializer.save(
            tenant=self.request.user.tenant,
            created_by=self.request.user
        )

# -------------------- Obligation --------------------
class ObligationViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Obligation.objects.all()
    serializer_class = ObligationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Obligation.objects.filter(
            framework__tenant=self.request.user.tenant,
            is_deleted=False
        )

    def perform_create(self, serializer):
        user = self.request.user
        framework = serializer.validated_data.get("framework")

        if not framework:
            raise ValidationError("Framework is required")

        if framework.tenant != self.request.user.tenant:
            raise Exception("Invalid tenant access")

        serializer.save(
            is_active=True,
            created_by=self.request.user
        )

# -------------------- Clause --------------------
class ClauseViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Clause.objects.all()
    serializer_class = ClauseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Clause.objects.filter(
            obligation__framework__tenant=self.request.user.tenant,
            is_deleted=False
        )

    def perform_create(self, serializer):
        user = self.request.user
        obligation = serializer.validated_data.get("obligation")

        if not obligation:
            raise ValidationError("Obligation is required")

        if obligation.framework.tenant != self.request.user.tenant:
            raise Exception("Invalid tenant access")

        serializer.save(
            is_active=True,
            created_by=self.request.user
        )

# -------------------- Control --------------------

class ControlViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        return Control.objects.filter(
            clause__obligation__framework__tenant=user.tenant,
            is_deleted=False
        )

    def perform_create(self, serializer):
        user = self.request.user
        clause = serializer.validated_data.get("clause")

        if not clause:
            raise ValidationError("Clause is required")

        if clause.obligation.framework.tenant != user.tenant:
            raise ValidationError("Invalid tenant access")

        serializer.save(created_by=user)

    def perform_create(self, serializer):
        print("perform_create called")
        print("USER:", self.request.user)
        print("TENANT:", self.request.user.tenant)

        serializer.save(
            is_active=True,
            # tenant=self.request.user.tenant,
            created_by=self.request.user
        )

#---------------Evidence-------------------

class EvidenceViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Evidence.objects.all()
    serializer_class = EvidenceSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Evidence.objects.filter(
            control__clause__obligation__framework__tenant=self.request.user.tenant,
            is_deleted=False
        )

    def perform_create(self, serializer):
        control = serializer.validated_data.get("control")

        # Tenant safety check
        if control.clause.obligation.framework.tenant != self.request.user.tenant:
            raise Exception("Invalid tenant access")

        serializer.save(
            is_active=True,
            created_by=self.request.user)

#------------------tasks---------------
class TaskViewSet(BaseViewSet, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(
            control__clause__obligation__framework__tenant=self.request.user.tenant,
            is_deleted=False
        )

    def perform_create(self, serializer):
        control = serializer.validated_data.get("control")

        if control.clause.obligation.framework.tenant != self.request.user.tenant:
            raise Exception("Invalid tenant access")

        serializer.save(is_active = True,
                        created_by=self.request.user)

