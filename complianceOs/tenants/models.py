from django.db import models


class Tenant(models.Model):
    comp_tenant_name = models.CharField(max_length=255)
    comp_tenant_code = models.CharField(max_length=100, unique=True)

    comp_tenant_status = models.CharField(max_length=50, default="active")
    comp_tenant_plan = models.CharField(max_length=50)
    comp_tenant_timezone = models.DateTimeField(auto_now=True)

    settings_json = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comp_tenant_name