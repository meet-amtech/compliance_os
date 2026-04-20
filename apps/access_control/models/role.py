from django.db import models
from apps.base.models import BaseModel
from .permission import Permission


class Role(BaseModel):
    name = models.CharField(max_length=100)

    tenant = models.ForeignKey(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="roles"
    )

    class Meta:
        db_table = "comp_role"
        unique_together = ("name", "tenant")

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"


class RolePermission(BaseModel):
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_permissions"
    )

    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name="permission_roles"
    )

    class Meta:
        db_table = "comp_role_permission"
        unique_together = ("role", "permission")
    
    def __str__(self):
        return f"{self.role.name} - {self.permission.name} at {self.role.tenant.name}"


class UserRole(BaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="user_roles"
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name="role_users"
    )

    class Meta:
        db_table = "comp_user_role"
        unique_together = ("user", "role")
    
    def __str__(self):
        return f"{self.user.email} - {self.role.name} at {self.role.tenant.name}"