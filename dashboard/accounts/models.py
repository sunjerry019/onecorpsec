from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.utils import six, timezone
from django.core import validators
# from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

# https://medium.com/agatha-codes/options-objects-customizing-the-django-user-model-6d42b3e971a4

# Create your models here
class DatabaseUser(AbstractUser):
    # Add additional fields here
    name          = models.CharField(_('name'), max_length=250, blank=True)
    sign_off_name = models.CharField(_('sign_off_name'), max_length=250, blank=True, help_text="The name used for signing off emails sent from the server. This is usually a short name")
    reply_to      = models.EmailField(_('reply_to'), blank=True, help_text="Email that people can choose to reply to for any information emails, if different from email")

    REQUIRED_FIELDS = ["email", "sign_off_name"]

    class Meta:
        app_label = 'accounts'

    def get_short_name(self):
        "Returns the short name for the user."
        return self.sign_off_name

    def __str__(self):
        return self.email
