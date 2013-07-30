from django.core.management.base import NoArgsCommand
from django.core import mail
from email.utils import formataddr
from notifications.utils import get_setting
from core.markdown import get_markdown
import os

from notifications.models import *

def _parseaddr(nsaddr):
	(name, _, addr) = nsaddr.rpartition(':')
	return formataddr((name, addr))

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

				text_content = get_setting('template', 'text', '%s') % item.content
				html_content = get_setting('template', 'html', '%s') % get_markdown(item.content)

				email.body = text_content
				email.attach_alternative(html_content)
				email.send()

				item.is_sent = True
				item.save()
