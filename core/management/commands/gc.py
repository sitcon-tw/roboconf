from django.core.management.base import NoArgsCommand
import notifications.gc as notifications

class Command(NoArgsCommand):
	help = "Cleans up unused database entries."

	def handle_noargs(self, **options):
		print notifications.clean()
