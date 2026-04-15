from django.db.models import QuerySet
from django.db import models

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


class BaseManager(models.Manager):
    """
    Custom Manager to handle soft deletes globally.
    """
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(BaseManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return BaseQuerySet(self.model).active()
        return BaseQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()
