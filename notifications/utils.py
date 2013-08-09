from django.conf import settings
from django.template.loader import render_to_string
from notifications.models import *

def format_address(name, addr):
	return '%s:%s' % (
		unicode(name if name is not None else '').strip().replace(':', '-'), 
		unicode(addr if addr is not None else '').strip()
	)

def parse_address(nsaddr):
	if nsaddr is None: return ('', '')
	(name, _, addr) = nsaddr.rpartition(':')
	return (name, addr)

def get_setting(category, value, default=None):
	return settings.NOTIFICATIONS[category].get(value, default)

'''
Create message from a specific set of context.
'''
def send_template_mail(sender, receiver, template_name, context, autosave=True):
	message = Message()
	message.sender = sender
	message.receiver = receiver

	context['sender_address'] = sender
	context['receiver_address'] = receiver
	context['site_url'] = 'http://staff.sitcon.org'
	raw_content = render_to_string(template_name, context).strip()

	subject, _, content = raw_content.partition('\n=====\n')
	message.subject = subject
	message.content = content
	if autosave: message.save()
	return message
