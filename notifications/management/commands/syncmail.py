# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from django.conf import settings
import smtplib, email, os

from notifications.models import *

class Command(NoArgsCommand):
	help = "Checks and sends messages from notification queue."

	def handle_noargs(self, **options):
		config = settings.NOTIFICATIONS
		emails = Message.objects.filter(method=Message.EMAIL, is_sent=False)
		if emails.count():
			client = smtplib.SMTP(os.environ['EMAIL_SERVER'], os.environ['EMAIL_PORT'])
			client.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASSWORD'])

			default_sender = get_setting('sender', 'default')
			sender_filter = get_setting('sender', 'filter')

			for email in emails.all():
				sender = email.sender if email.sender else default_sender
				client.sendmail(convert_address(sender, sender_filter), 
								convert_address(email.receiver), 
								email.content)
				email.is_sent = True
				email.save()

			client.quit()

	def convert_address(self, expr, use_filter='"%s" <%s>'):
		name, separator, addr = expr.rpartition(':')
		return addr if not separator else use_filter % (name, addr)

	def get_setting(self, category, value):
		return settings.NOTIFICATIONS[category].get(value)
