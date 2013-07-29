from django.core.management.base import NoArgsCommand
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from smtplib import SMTP
from core.markdown import get_markdown
from notifications.utils import get_setting
import os

from notifications.models import *

def format_unicode(text):
	return Header(text.encode('utf-8'), 'UTF-8')

class Command(NoArgsCommand):
	help = "Checks and sends messages from notification queue."

	def handle_noargs(self, **options):
		emails = Message.objects.filter(method=Message.EMAIL, is_sent=False)
		if emails.count():
			client = SMTP(os.environ['EMAIL_SERVER'], os.environ['EMAIL_PORT'])
			client.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASSWORD'])

			default_sender = get_setting('sender', 'default')

			for email in emails.all():
				s_name, _, s_email = (email.sender if email.sender else default_sender).rpartition(':')
				r_name, _, r_email = (email.receiver).rpartition(':')

				part = MIMEMultipart('alternative')
				part['Subject'] = format_unicode(email.subject)
				part['From'] = formataddr((str(format_unicode(s_name)), s_email))
				part['To'] = formataddr((str(format_unicode(r_name)), r_email))

				text_content = get_setting('template', 'text', '%s') % email.content
				html_content = get_setting('template', 'html', '%s') % get_markdown(email.content)
				part.attach(MIMEText(text_content.encode('utf-8'), 'text', 'UTF-8'))
				part.attach(MIMEText(html_content.encode('utf-8'), 'html', 'UTF-8'))

				client.sendmail(s_email, r_email, part.as_string())

				email.is_sent = True
				email.save()

			client.quit()

