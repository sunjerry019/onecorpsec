# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.utils import six, timezone
from django.core import validators
from django.core.mail import send_mail

import os
from pathlib import Path
from shutil import copyfile


# https://medium.com/agatha-codes/options-objects-customizing-the-django-user-model-6d42b3e971a4

# Create your models here
class DatabaseUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, is_staff, is_superuser, reply_to = None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email        = self.normalize_email(email)
        if reply_to:
            reply_to = self.normalize_email(reply_to)
        user         = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Create a template folder for their emails
        emailTemplateDir = "templates/emails/{}".format(username)
        # Create folder if doesn't exist (https://stackoverflow.com/a/273227/3211506)
        os.makedirs(emailTemplateDir, exist_ok=True)

        defaultDir = "templates/emails/default"
        pathlist = Path(defaultDir).glob('**/*')
        for path in pathlist:
            path_in_str = str(path)
            basename    = os.path.basename(path_in_str)
            newfile     = os.path.join(emailTemplateDir, basename)
            if not os.path.exists(newfile):
                copyfile(path_in_str, newfile)

        return user

    def create_user(self, username, email, password, reply_to = None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, reply_to = None, **extra_fields):
        return self._create_user(username, email, password, True, True, **extra_fields)

    def get_by_natural_key(self, _username):
        # Authenticate uses username [https://stackoverflow.com/a/46825451/3211506]
        return self.get(username=_username)

class DatabaseUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[
            validators.RegexValidator(r'^[\w.@+-]+$',
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid'),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # Custom Stuff
    name          = models.CharField(_('name'), max_length=250, blank=True)
    sign_off_name = models.CharField(_('sign off name'), max_length=250, blank=True, help_text="The name used for signing off emails sent from the server. This is usually a short name")
    reply_to      = models.EmailField(_('reply-to email'), blank=True, help_text="Email that people can choose to reply to for any information emails, if different from email")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email", "sign_off_name"]
    # REQUIRED_FIELDS = ['email']


    # objects = UserManager()
    objects = DatabaseUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # DO NOT USE ABSTRACT = TRUE
        # abstract = True
        app_label = 'accounts'

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_short_name(self):
        "Returns the short name for the user."
        return self.sign_off_name

    def __str__(self):
        return self.email
