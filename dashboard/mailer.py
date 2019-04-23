#!/usr/bin/env python3

"""
mailer.py
This python module sends mails using django.core.mail and templates from templates/emails/

If you want to change email contents, or add additional dynamic information, update the
corresponding .html and .txt files and use the "row" as necessary

All tags are declared in the context

"""

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
	def __init__(self, reply_to, row):
		# row is a zipped dictionary of the mysql entry for that company

		self.row = row
		self.headers = { 'Auto-Submitted': 'auto-generated' }
		self.reply_to = reply_to
		self.context = {
			'addressed_to' 	: self.row["addresseeName"] if self.row["addresseeName"] else self.row["coyName"],
			"coyname"		: self.row["coyName"],
			"coyregno"		: self.row["coyRegNo"]
		}
		self.to  = [ x.strip() for x in self.row["toEmail"].split(",") ]
		self.cc  = [ x.strip() for x in self.row["ccEmail"].split(",") ] + [ self.reply_to ]
		self.bcc = [ x.strip() for x in self.row["bccEmail"].split(",") ]

		self.defaultoptions = {
			"subject"		: "[OneCorpSec] No Subject",
			"body"	 		: "This email contains no content.",
			"from_email"	: settings.DEFAULT_FROM_EMAIL,
			"headers"		: self.headers,
			"to"			: self.to,
			"cc"			: self.cc,
			"bcc"			: self.bcc,
			"reply_to"		: self.reply_to
		}

	def send_acra(self):
		subject = '[OneCorpSec] ACRA/AGM Reminder for {}'.format(self.row["coyname"])
		plaintext = get_template('emails/agm_acra.txt')
		htmly     = get_template('emails/agm_acra.html')

		d = self.context
		# Add additional contexts
		d.update({
			"subject"		: subject,
			"fin_endmonth" 	: self.row["fin_endMonth"],
			"fin_endYear"	: self.row["fin_endYear"]
		})

		text_content = plaintext.render(d)
		html_content = htmly.render(d)

		options = {
			"subject"		: subject,
			"body"	 		: text_content
		}

		return self.sendmail(options, html_content)

	def sendmail(self, addOptions, html_content):
		options = {**self.defaultoptions, **addOptions}

		msg = EmailMultiAlternatives(**options)
		msg.attach_alternative(html_content, "text/html")
		return msg.send()

# send_mail(
# 	"htmlemailer/example",
# 	settings.DEFAULT_FROM_EMAIL,
# 	['a@example.com'],
# 	{
# 		"my_message": "Hello & good day to you!"
# 	}
# )

# https://docs.djangoproject.com/en/dev/topics/email/#send-mail
