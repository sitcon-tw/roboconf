import re
from django.conf import settings
from django.db.models import Q
from notifications.utils import format_address, send_template_mail, send_template_sms
from users.models import User

def send_mail(sender, receiver, template_name, context):
	context['sender'] = sender
	context['receiver'] = receiver
	sender = settings.ISSUES_FROM_EMAIL % sender.profile.name()
	receiver = format_address(receiver.profile.name(), receiver.email)
	return send_template_mail(sender, receiver, template_name, context)

def send_sms(sender, receiver, template_name, context):
	context['sender'] = sender
	context['receiver'] = receiver
	return send_template_sms('', receiver.profile.phone, template_name, context)

def filter_mentions(content):
	mention_tokens = set(re.findall(u'(?<=@)[0-9A-Za-z\u3400-\u9fff\uf900-\ufaff_\\-]+', content))
	mentions = []
	for mention in mention_tokens:
		try:
			mentionee = User.objects.get(Q(username__istartswith=mention) | Q(profile__display_name__iexact=mention))
			mentions.append(mentionee)
		except User.DoesNotExist:
			continue
	return mentions
