#!/usr/bin/env python3

# https://www.stavros.io/posts/standalone-django-scripts-definitive-guide/
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# from htmlemailer import send_mail
#
# send_mail(
# 	"htmlemailer/example",
# 	"My Site <yudong@onecorpsec.com>",
# 	["sunjerry019@gmail.com"],
# 	{
# 		"my_message": "Hello & good day to you!"
# 	})

import sys
sys.path.insert(0, 'dashboard')
import settings
from django.core.mail import send_mail

# https://docs.djangoproject.com/en/dev/topics/email/#send-mail
send_mail(
    'Subject here',
    'Here is the message.',
    settings.DEFAULT_FROM_EMAIL,
    ['sunjerry019@gmail.com'],
    fail_silently=False
)
