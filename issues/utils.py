from notifications.models import *
from notifications.utils import get_setting

def get_realname(user):
	return '%s %s' % (sender.last_name, sender.first_name)

'''
Create message from a specific set of sender, receiver, subject and content.
Accepts unicode string.
'''
def send_mail(sender, receiver, subject, content):
	message = Message()
	message.sender = get_setting('sender', 'filter') % get_realname(sender)
	message.receiver = '%s:%s' % (get_realname(receiver), receiver.email)
	message.subject = subject
	message.content = content
	message.save()
	return message
