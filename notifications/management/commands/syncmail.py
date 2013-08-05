from django.core.management.base import NoArgsCommand
from django.core import mail
from django.utils.html import strip_tags
from email.utils import formataddr
from notifications.utils import get_setting, parse_address
from core.markdown import get_markdown
import os

from notifications.models import *

def _parseaddr(nsaddr):
	return formataddr(parse_address(nsaddr))

class Command(NoArgsCommand):
	help = "Checks and sends messages from notification queue."

	def handle_noargs(self, **options):
		emails = Message.objects.filter(method=Message.EMAIL, is_sent=False)
		if emails.count():
			conn = mail.get_connection()
			conn.open()

			default_sender = get_setting('sender', 'default')
			for item in emails.all():
				email = mail.EmailMultiAlternatives(item.subject, connection=conn)
				email.to = [_parseaddr(item.receiver)]

				if item.sender:
					email.from_email = _parseaddr(item.sender)

				email.body = strip_tags(item.content)
				email.attach_alternative(item.content, 'text/html')
				email.send()

				item.is_sent = True
				item.save()

			conn.close()
