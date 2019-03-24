#!/usr/bin/env python3

from htmlemailer import send_mail

send_mail(
	"htmlemailer/example",
	"My Site <yudong@onecorpsec.com>",
	["sunjerry019@gmail.com"],
	{
		"my_message": "Hello & good day to you!"
	})
