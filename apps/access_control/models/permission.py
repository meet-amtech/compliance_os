from django.db import models
from apps.base.models import BaseModel


class Permission(BaseModel):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=150)  # UI display
    description = models.TextField(blank=True)

    # NULL = system permission
    tenant = models.ForeignKey(
        "tenants.Tenant",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="permissions"
    )

    class Meta:
        db_table = "comp_permission"
        unique_together = ("code", "tenant")
        indexes = [
            models.Index(fields=["code"]),
        ]
    
    def __str__(self):
        return f"{self.code} ({self.tenant.name})"