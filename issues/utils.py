import re
from django.conf import settings
from django.db.models import Q
from notifications.utils import format_address, send_template_mail, send_template_sms
from users.models import User, Group

def send_mail(sender, receiver, template_name, context):
	context['sender'] = sender
	context['receiver'] = receiver
	sender = settings.USER_ISSUE_SENDER.format(sender.profile.name)
	if isinstance(receiver, User):
		receiver = format_address(receiver.profile.name, receiver.email)
	return send_template_mail(sender, receiver, template_name, context)

def send_sms(sender, receiver, template_name, context):
	context['sender'] = sender
	context['receiver'] = receiver
	return send_template_sms('', receiver.profile.phone, template_name, context)

def filter_mentions(content):
	mention_tokens = set(re.findall(u'(?<=@)[0-9A-Za-z\u3400-\u9fff\uf900-\ufaff_\\-]+', content))
	mentions, extra_receivers = [], []
	for mention in mention_tokens:
		try:
		mentionee = User.objects.filter(Q(username__istartswith=mention) | Q(profile__display_name__iexact=mention)).first()
		if mentionee:
			mentions.append(mentionee)
		else:
			mention_group = Group.objects.filter(name__istartswith=mention).first()
			if mention_group:
				mentions.extend(User.objects.filter(group=mention_group))
	if settings.BROADCAST_MAGIC_TOKEN in mention_tokens:
		extra_receivers.append(settings.BROADCAST_EMAIL)
	return set(mentions), extra_receivers

def is_issue_urgent(issue):
	# Label 1 stands for urgent in current staff system
	return issue.labels.filter(id=settings.URGENT_ISSUE_ID).exists()
