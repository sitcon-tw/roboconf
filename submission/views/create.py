from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from submission.models import Submission

@login_required
def create(request):
	context = {
			'user': request.user,
			}

	if request.POST.get('submit'):
		receiver_target = request.POST.get('receiver', '').split(',')
		if 'staff' in receiver_target:
			for user in User.objects.exclude(email='', is_active=False):
				receivers[user.email] = user.profile.name()

		if request.POST.get('receivers'):
			additional_receivers = request.POST.get('receivers').strip().split('\n')
			for entry in additional_receivers:
				if ':' in entry:
					name, addr = parse_address(entry)
					receivers[addr] = name
				else:
					receivers[entry] = ''

		messages = []

	return render(request, 'submission/create.html', context)
