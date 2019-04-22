#!/usr/bin/env python3

# https://www.stavros.io/posts/standalone-django-scripts-definitive-guide/

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "dashboard.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import dashboard.settings
from htmlemailer import send_mail

class Mail():
	def __init__(self):
		pass


# send_mail(
# 	"htmlemailer/example",
# 	settings.DEFAULT_FROM_EMAIL,
# 	['sunyudong@theenglishtuitioncorner.com'],
# 	{
# 		"my_message": "Hello & good day to you!"
# 	}
# )

# https://docs.djangoproject.com/en/dev/topics/email/#send-mail
