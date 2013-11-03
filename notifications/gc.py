from notifications.models import Message
from django.utils import timezone
from datetime import timedelta

def clean():
	# Cleaning out old messages two weeks ago
	before_date = timezone.now() - timedelta(days=14)
	emails = Message.objects.filter(method=Message.EMAIL, is_sent=True, 
									creation_time__lt=before_date)
	count = emails.count()
	emails.delete()
	return '%d email notifications cleaned' % count
	