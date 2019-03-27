"""
Django settings for dashboard project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import json

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3yuyd@vfyu3i*m09(g)n%tpx(h0vep_4pf@f9l!rh!7xeptg_f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'material', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'htmlemailer'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dashboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dashboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Source for the configuration file
_confLoc = os.path.join(BASE_DIR, "../config.location")
with open(_confLoc, 'r') as f:
    _x = f.readlines()[0].strip()
    if _x[0] == '.':
        _confFile = os.path.join(os.path.dirname(os.path.abspath(_confLoc)), _x)
    else:
        # This is an absolute path
        _confFile = _x

# Obtain the database configuration details
with open(_confFile,'r') as f:
    _conf = json.load(f)

DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.mysql',
        'NAME'      : _conf["database"],
        'USER'      : _conf["user"],
        'PASSWORD'  : _conf["password"],
        'HOST'      : _conf["host"]
    }
}

# HTML Mailer
_send_mail_with      = _conf["DOserver"]["emailUsers"]["default"]["user"]
_send_mail_with_name = _conf["DOserver"]["emailUsers"]["default"]["name"]

# https://stackoverflow.com/a/28143166
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_PORT = 25
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
# EMAIL_USE_TLS = True
# EMAIL_PORT = 143
# EMAIL_HOST = 'mail.onecorpsec.com'
# EMAIL_HOST_USER = _send_mail_with + '@onecorpsec.com'
# EMAIL_HOST_PASSWORD = _conf["DOserver"]["emailUsers"][_send_mail_with]
DEFAULT_FROM_EMAIL = "{} <{}@onecorpsec.com>".format(_send_mail_with_name, _send_mail_with)

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# Accounts and Auth
AUTH_USER_MODEL = 'accounts.DatabaseUser'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# For emails
# EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
