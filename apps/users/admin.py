from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.base.admin import BaseAdmin
from apps.users.models import User

@admin.register(User)
class UserAdmin(BaseAdmin):
    """
    Admin View for User, inheriting from BaseAdmin for standard audit fields.
    """
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_deleted')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'tenant_id')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    
    readonly_fields = BaseAdmin.readonly_fields + ('last_login',)
