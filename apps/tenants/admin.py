from django.contrib import admin
from apps.base.admin import BaseAdmin
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(BaseAdmin):
    list_display = BaseAdmin.list_display + (
        "name",
        "code",
        "plan",
        "timezone",
    )

    search_fields = ("name", "code")
    list_filter = BaseAdmin.list_filter + ("plan",)