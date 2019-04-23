#!/usr/bin/env python3

# https://www.stavros.io/posts/standalone-django-scripts-definitive-guide/

import os
os.environ["DJANGO_SETTINGS_MODULE"] = "dashboard.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import dashboard.settings as settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

class Mail():
	def __init__(self):
		plaintext = get_template('emails/email.txt')
		htmly     = get_template('emails/email.html')

		d ={ 'username': "bluhb" }

		subject, from_email, to = 'hello', settings.DEFAULT_FROM_EMAIL, 'sunyudong@theenglishtuitioncorner.com'
		text_content = plaintext.render(d)
		html_content = htmly.render(d)
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()

Mail()

# send_mail(
# 	"htmlemailer/example",
# 	settings.DEFAULT_FROM_EMAIL,
# 	['sunyudong@theenglishtuitioncorner.com'],
# 	{
# 		"my_message": "Hello & good day to you!"
# 	}
# )

# https://docs.djangoproject.com/en/dev/topics/email/#send-mail
