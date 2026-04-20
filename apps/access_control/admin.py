from django.contrib import admin
from .models.permission import Permission
from .models.role import Role, RolePermission, UserRole 

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "tenant", "is_active", "is_deleted")
    list_filter = ("tenant", "is_active", "is_deleted")
    search_fields = ("name", "tenant__name")


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "tenant", "is_active", "is_deleted")
    list_filter = ("tenant", "is_active", "is_deleted")
    search_fields = ("code", "name", "tenant__name")
    readonly_fields = ("created_at",)


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "permission", "is_active", "is_deleted")
    list_filter = ("role__tenant", "role", "permission", "is_active", "is_deleted")
    search_fields = (
        "role__name",
        "permission__code",
        "permission__name",
        "role__tenant__name",
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "is_active", "is_deleted")
    list_filter = ("role__tenant", "user__email", "role", "is_active", "is_deleted")
    search_fields = (
        "user__email",
        "role__name",
        "role__tenant__name",
    )
