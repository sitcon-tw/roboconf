from django.core.management.base import NoArgsCommand
from notifications.models import Message

class Command(NoArgsCommand):
	help = "Checks and sends SMS from notification queue."

	def handle_noargs(self, **options):
		messages = Message.objects.filter(method=Message.SMS, is_sent=False)
		if messages.count():
			for message in messages:
				message.send()
