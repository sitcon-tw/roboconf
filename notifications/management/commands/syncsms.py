from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.utils.html import strip_tags
from notifications.sms import SmsMessage
from notifications.models import *

class Command(NoArgsCommand):
	help = "Checks and sends SMS from notification queue."

	def handle_noargs(self, **options):
		messages = Message.objects.filter(method=Message.SMS, is_sent=False)
		if messages.count():
			for message in messages:
				sms = SmsMessage()

				if message.sender:
					sms.from_sender = message.sender
				else:
					sms.from_sender = settings.DEFAULT_SMS_SENDER

				receiver = message.receiver
				if receiver.startswith('0') and not receiver.startswith('00'):
					sms.to = settings.DEFAULT_SMS_COUNTRY_CODE + receiver[1:]
				else:
					sms.to = receiver
	
				sms.text = strip_tags(message.content)

				message.is_sent = sms.send()
				message.save()
