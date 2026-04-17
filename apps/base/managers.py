from django.db.models import QuerySet
from django.db import models
from apps.base.middleware import get_current_tenant


class BaseQuerySet(QuerySet):
    """
    Custom QuerySet for models with soft-delete capabilities.
    """

    def delete(self):
        """
        Soft delete the records.
        """
        return super(BaseQuerySet, self).update(is_deleted=True, is_active=False)

    def hard_delete(self):
        """
        Permanently remove records from the database.
        """
        return super(BaseQuerySet, self).delete()

    def active(self):
        """
        Filter to only include active and non-deleted records.
        """
        return self.filter(is_deleted=False, is_active=True)

    # NEW: tenant filtering
    def for_tenant(self, tenant):
        if tenant:
            return self.filter(tenant=tenant)
        return self


class BaseManager(models.Manager):
    """
    Custom Manager to handle soft deletes globally + tenant isolation.
    """

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(BaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        qs = BaseQuerySet(self.model)

        # Soft delete filter
        if self.alive_only:
            qs = qs.active()

        # AUTO TENANT FILTER (CORE SaaS LOGIC)
        tenant = get_current_tenant()

        # Only apply if model has tenant field
        if tenant and hasattr(self.model, 'tenant'):
            qs = qs.filter(tenant=tenant)

        return qs

    def hard_delete(self):
        return self.get_queryset().hard_delete()