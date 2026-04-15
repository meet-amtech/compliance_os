from django.contrib import admin
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ("id", "comp_tenant_name", "comp_tenant_code", "comp_tenant_status", "comp_tenant_plan", "created_at")
    search_fields = ("comp_tenant_name", "comp_tenant_code")
    list_filter = ("comp_tenant_status", "comp_tenant_plan")