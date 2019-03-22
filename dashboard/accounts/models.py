from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here
class DatabaseUser(AbstractUser):
    # Add additional fields here
    name          = models.CharField(_('name'), max_length=250, blank=True)
    sign_off_name = models.CharField(_('sign_off_name'), max_length=250, blank=True, help_text="The name used for signing off emails sent from the server. This is usually a short name")
    reply_to      = models.CharField(_('reply_to'), max_length=254, blank=True, help_text="Email that people can choose to reply to for any information emails.")

    def get_short_name(self):
        "Returns the short name for the user."
        return self.sign_off_name

    def __str__(self):
        return self.email
