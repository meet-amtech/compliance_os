from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    """
    Base Admin class that handles audit fields (created_by, updated_by)
    automatically from the request object in Django Admin UI.
    """
    list_per_page = 25
    list_display = ('id', 'is_active', 'is_deleted', 'created_at')
    list_filter = ('is_active', 'is_deleted')
    ordering = ('-created_at',)
    list_select_related = ('created_by', 'updated_by')
    readonly_fields = ('id', 'created_at', 'updated_at', 'created_by', 'updated_by')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
