import uuid
import logging
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.base.managers import BaseManager
from apps.base.middleware import get_current_user

logger = logging.getLogger(__name__)

class BaseModel(models.Model):
    """
    Abstract Base Model providing:
    - UUID as primary key
    - Automatic creation/modification timestamps
    - Automatic `created_by`/`updated_by` user audit trails
    - Soft delete capability (`is_active`, `is_deleted`)
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(_("Created Date"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("Last Updated Date"), auto_now=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='%(app_label)s_%(class)s_created_related', 
        null=True,
        blank=True,
        on_delete=models.SET_NULL,  # Prevent deleting user from deleting audit logs
        help_text=_("User who created this record")
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='%(app_label)s_%(class)s_updated_related', 
        null=True,
        blank=True, 
        on_delete=models.SET_NULL,  # Prevent deleting user from deleting audit logs
        help_text=_("User who last updated this record")
    )
    
    is_active = models.BooleanField(default=True, db_index=True)
    is_deleted = models.BooleanField(default=False, db_index=True)
    
    objects = BaseManager()
    all_objects = BaseManager(alive_only=False)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def hard_delete(self):
        super().delete()

    def delete(self, *args, **kwargs):
        """Soft delete the instance."""
        self.is_deleted = True
        self.is_active = False
        self.save(update_fields=['is_deleted', 'is_active', 'updated_at', 'updated_by'])

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user:
            # We must be careful if the user object passed is the correct instance 
            # and not an AnonymousUser (already handled in middleware).
            if not self.pk:
                self.created_by = user
            self.updated_by = user
        super().save(*args, **kwargs)
