from notifications.models import *
from notifications.utils import get_setting, get_realname
from django.template.loader import render_to_string

'''
Create message from a specific set of context.
Accepts unicode string.
'''
def send_mail(sender, receiver, template_name, context):
	message = Message()
	message.sender = get_setting('sender', 'issues') % get_realname(sender)
	message.receiver = '%s:%s' % (get_realname(receiver), receiver.email)

	context['sender'] = sender
	context['receiver'] = receiver
	raw_content = render_to_string(template_name, context).strip()

	subject, _, content = raw_content.partition('\n=====\n')
	message.subject = subject
	message.content = content
	message.save()
	return message
