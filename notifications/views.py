from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from notifications.models import Message

@login_required
def list(request):
	if not request.user.has_perm('notifications.create_message'):
		return redirect(reverse('core:index'))
	return render(request, 'notifications_list.html', {'messages': Message.objects.filter(is_sent=False) })

@login_required
def create(request):
	if not request.user.has_perm('notifications.create_message'):
		return redirect(reverse('notifications:list'))
	return render(request, 'notifications_create.html', {})
