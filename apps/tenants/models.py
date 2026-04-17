from django.db import models
from apps.base.models import BaseModel


class Tenant(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)

    plan = models.CharField(
        max_length=50,
        choices=[
            ("basic", "Basic"),
            ("pro", "Pro"),
            ("enterprise", "Enterprise"),
        ],
        default="basic"
    )

    timezone = models.CharField(max_length=50, default="Asia/Kolkata")

    settings_json = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        db_table = "comp_tenant"

    def __str__(self):
        return f"{self.name} ({self.code})"