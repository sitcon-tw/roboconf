from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from notifications.models import Message
from notifications.utils import *
from users.utils import get_user_name

@login_required
def list(request):
	if not request.user.has_perm('notifications.add_message'):
		return redirect(reverse('core:index'))
	return render(request, 'notifications_list.html', {'messages': Message.objects.filter(is_sent=False) })

@login_required
def create(request):
	if not request.user.has_perm('notifications.add_message'):
		return redirect(reverse('notifications:list'))

	context = {}

	if request.POST.get('submit'):
		# TODO: Send SMS

		sender = (format_address(request.POST.get('sender_name'), 
								request.POST.get('sender_email')) 
					if 'sender_email' in request.POST
					else get_setting('sender', 'default'))
		receivers = {}
		
		receiver_target = request.POST.get('receiver', '').split(',')
		if 'staff' in receiver_target:
			for user in User.objects.exclude(email=''):
				receivers[user.email] = get_user_name(user)

		if 'mailing_list' in receiver_target:
			for addr in get_setting('receiver', 'mailing_lists', []):
				receivers[addr] = ''

		if request.POST.get('receivers'):
			additional_receivers = request.POST.get('receivers').strip().split('\n')
			for entry in additional_receivers:
				if ':' in entry:
					name, addr = parse_address(entry)
					receivers[addr] = name
				else:
					receivers[entry] = ''

		messages = []

		for email, name in receivers.iteritems():
			message = send_template_mail(
				sender, 
				format_address(name, email), 
				'mail/notification_general.html', 
				{
					'subject': request.POST.get('subject'),
					'content': request.POST.get('content'),
					'reply_to': request.POST.get('reply_to'),
				},
				autosave=False,
			)
			messages.append(message)

		Message.objects.bulk_create(messages)
		context['status'] = 'success'

	return render(request, 'notifications_create.html', context)
