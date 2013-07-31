from django.db import models
from django.utils import timezone

class Message(models.Model):
	EMAIL = '@'
	SMS = '+'
	METHOD_CHOICES = (
		(EMAIL, 'E-Mail'),
		(SMS, 'SMS'),
	)

	method = models.CharField(max_length=1, choices=METHOD_CHOICES, default=EMAIL)
	sender = models.CharField(max_length=160, blank=True, default='')	# In sender & receiver field, 
	receiver = models.CharField(max_length=160)		# use ':' to separate between name and address/number
	subject = models.CharField(max_length=128)
	content = models.TextField()
	creation_time = models.DateTimeField(editable=False, default=timezone.now)
	is_sent = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s[%s] %s" % (method, receiver, subject)
