from django.db import models
from apps.base.models import BaseModel
from apps.tenants.models import Tenant
from apps.users.models import User


class Framework(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name="frameworks")

    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    source_type = models.CharField(max_length=50)  # RBI, SEBI, ISO

    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)

# Upload docs
    document = models.FileField(upload_to='frameworks/', null=True, blank=True)

    class Meta:
        db_table = "comp_framework"

    def __str__(self):
        return f"{self.name} v{self.version}"


class Obligation(BaseModel):
    framework = models.ForeignKey(Framework, on_delete=models.CASCADE, related_name="obligations")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    reference_code = models.CharField(max_length=100)

    severity = models.CharField(max_length=50)
    periodicity = models.CharField(max_length=50)  # monthly, yearly

    class Meta:
        db_table = "comp_obligation"


class Clause(BaseModel):
    obligation = models.ForeignKey(Obligation, on_delete=models.CASCADE, related_name="clauses")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "comp_clause"


class Control(BaseModel):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    obligation = models.ForeignKey(Obligation, on_delete=models.CASCADE, related_name="controls")

    owner_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    control_type = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    risk_level = models.CharField(max_length=50)

    class Meta:
        db_table = "comp_control"