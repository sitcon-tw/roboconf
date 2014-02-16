from django.core.management.base import NoArgsCommand
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

				sms.to = message.receiver	
				sms.text = strip_tags(message.content)

				message.is_sent = sms.send()
				message.save()
