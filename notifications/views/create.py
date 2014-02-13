from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from notifications.models import Message
from notifications.utils import *
from users.utils import get_user_name

@permission_required('notifications.add_message')
def create(request):
	context = {}

	if request.POST.get('submit'):
		# TODO: Send SMS

		sender = ''
		receivers = {}

		if request.POST.get('sender_email'):
			sender = format_address(request.POST.get('sender_name'), request.POST.get('sender_email'))
		
		receiver_target = request.POST.get('receiver', '').split(',')
		if 'staff' in receiver_target:
			for user in User.objects.exclude(email=''):
				receivers[user.email] = get_user_name(user)

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
					'reply_to': request.POST.get('reply_address'),
				},
				autosave=False,
			)
			messages.append(message)

		Message.objects.bulk_create(messages)
		context['status'] = 'success'

	return render(request, 'notifications/create.html', context)
