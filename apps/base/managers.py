from django.db.models import QuerySet
from django.db import models
from apps.base.middleware import get_current_tenant


class BaseQuerySet(QuerySet):

    def delete(self):
        return super().update(is_deleted=True, is_active=False)

    def hard_delete(self):
        return super().delete()

    def active(self):
        return self.filter(is_deleted=False, is_active=True)

    def for_tenant(self, tenant):
        if tenant:
            return self.filter(tenant=tenant)
        return self


class BaseManager(models.Manager):

    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()   #  FIXED

        if self.alive_only:
            qs = qs.filter(is_deleted=False, is_active=True)

        tenant = get_current_tenant()

        if tenant and hasattr(self.model, 'tenant'):
            qs = qs.filter(tenant=tenant)

        return qs

    def hard_delete(self):
        return self.get_queryset().hard_delete()