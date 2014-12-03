import notifications.utils as utils
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
		return "%s[%s] %s" % (self.method, self.receiver, self.subject)

	def save(self, *args, **kwargs):
		super(Message, self).save(*args, **kwargs)
		self.send()

	def send(self, **kwargs):
		if self.method == Message.EMAIL:
			from django.conf import settings
			from django.core import mail
			from django.utils import html

			email = mail.EmailMultiAlternatives(self.subject, connection=kwargs.get('connection'))
			email.from_email = utils.to_email_address(self.sender or settings.DEFAULT_NOTIFICATION_SENDER)
			email.to = (utils.to_email_address(self.receiver),)
			email.body = html.strip_tags(self.content)
			email.attach_alternative(self.content, 'text/html')

			try:
				email.send()
			except:
				print('Failed to send email')
			else:
				self.is_sent = True
				super(Message, self).save()

		elif self.method == Message.SMS:
			from notifications.sms import SmsMessage

			sms = SmsMessage()
			sms.to = self.receiver
			sms.text = self.content

			if self.sender:
				sms.from_sender = self.sender

			self.is_sent = sms.send()
			super(Message, self).save()
