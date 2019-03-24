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
from django.core.mail import get_connection

# https://docs.djangoproject.com/en/dev/topics/email/#send-mail
print(send_mail(
    'Subject here',
    'Here is the message.',
    "yudong@onecorpsec.com",
    ['sunyudong@theenglishtuitioncorner.com'],
    fail_silently=False,
	connection=get_connection(backend='django.core.mail.backends.smtp.EmailBackend', fail_silently=False, username="", password="")
))
