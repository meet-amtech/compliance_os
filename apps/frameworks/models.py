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
    # tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    # obligation = models.ForeignKey(Obligation, on_delete=models.CASCADE, related_name="controls")
    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    control_code = models.CharField(max_length=100, unique=True)

    clause = models.ForeignKey(Clause,on_delete=models.CASCADE, related_name="controls")

    owner_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    control_type = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    risk_level = models.CharField(max_length=50)

    class Meta:
        db_table = "comp_control"

class Evidence(BaseModel):
    control = models.ForeignKey(Control, on_delete=models.CASCADE, related_name="evidences")
    file = models.FileField(upload_to="evidence/")
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Evidence for {self.control.control_code}"

class Task(BaseModel):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    control = models.ForeignKey(
        Control,
        on_delete=models.CASCADE,
        related_name="tasks"
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    due_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    def __str__(self):
        return self.title