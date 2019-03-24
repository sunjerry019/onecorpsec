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

from django.core.mail import EmailMultiAlternatives
import settings

def send_mail():
 from_email = settings.EMAIL_HOST_USER
 to_email = ['sunjerry019@gmail.com']
 subject = "Any text"
 body = "Hello world"
 msg = EmailMultiAlternatives(subject, body, from_email, to_email)
 msg.send()

send_mail()
