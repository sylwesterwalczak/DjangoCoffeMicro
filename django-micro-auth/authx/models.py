from django.db import models
from django.conf import settings

from django.contrib.admin.models import LogEntryManager
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    use_in_migrations = True


class CustomUser(AbstractBaseUser,PermissionsMixin):
    """ User class model used for authentication"""
    username = models.CharField(max_length=255, unique=True, blank=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=2, null=True, blank=True)

    objects = UserManager()

    class Meta:
        managed = False
        db_table = settings.AUTH_USER_TABLE
        

    USERNAME_FIELD = 'username'



class NoLogEntryManager(LogEntryManager):
    """Manager disabling logging logic"""

    def __init__(self, model=None):
        super().__init__()
        self.model = model

    def log_action(self, *args, **kwargs):
        return None

    def get_queryset(self):
        return super().get_queryset().none()