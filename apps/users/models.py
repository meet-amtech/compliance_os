from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from apps.base.models import BaseModel
from apps.users.managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """
    Custom User Model for Compliance OS.
    Inherits from BaseModel which provides ID (UUID), timestamps, and audit info.
    """
    tenant_id = models.UUIDField(null=True, blank=True, db_index=True, help_text=_("Placeholder for Multi-Tenancy"))
    
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    
    # is_active is inherited from BaseModel, but AbstractBaseUser expects it.
    # We will let BaseModel handle it, it defaults to True.

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # Email & Password are required by default

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ['-created_at']
        db_table = 'comp_user'

    def __str__(self):
        return str(self.email)
        
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.email
