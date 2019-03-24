#!/usr/bin/env python3

from htmlemailer import send_mail

send_mail(
	"htmlemailer/example",
	"My Site <sunjerry019@gmail.com>",
	["you@recipient.com"],
	{
		"my_message": "Hello & good day to you!"
	})
