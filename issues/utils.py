from notifications.models import *
from notifications.utils import get_mail_setting, send_template_mail, format_address, send_template_sms
from users.utils import get_user_name

def send_mail(sender, receiver, template_name, context):
	context['sender'] = sender
	context['receiver'] = receiver
	sender = get_mail_setting('sender', 'issues') % get_user_name(sender)
	receiver = format_address(get_user_name(receiver), receiver.email)
	return send_template_mail(sender, receiver, template_name, context)

def send_sms(sender, receiver, template_name, context):
	context['sender'] = sender
	context['receiver'] = receiver
	return send_template_sms('', receiver.profile.phone, template_name, context)
