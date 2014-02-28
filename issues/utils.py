from notifications.models import *
from notifications.utils import get_mail_setting, send_template_mail, format_address, send_template_sms

def send_mail(sender, receiver, template_name, context):
	context['sender'] = sender
	context['receiver'] = receiver
	sender = get_mail_setting('sender', 'issues') % sender.profile.name()
	receiver = format_address(receiver.profile.name(), receiver.email)
	return send_template_mail(sender, receiver, template_name, context)

def send_sms(sender, receiver, template_name, context):
	context['sender'] = sender
	context['receiver'] = receiver
	return send_template_sms('', receiver.profile.phone, template_name, context)
