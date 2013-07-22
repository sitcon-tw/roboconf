from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import views_list as _list
import views_detail as _detail
import views_create as _create
from issues.models import *

@login_required
def list(request):
	return _list.list(request, 'list')

@login_required
def assigned(request, user_id):
	return _list.list(request, 'assigned')

@login_required
def created(request, user_id):
	return _list.list(request, 'created')

@login_required
def starred(request, user_id):
	# TODO: Implement "starring" (a.k.a watch issue)
	return redirect(reverse('issues:list'))

@login_required
def detail(request, issue_id):
	issue = get_object_or_404(Issue, pk=issue_id)

	action = request.POST.get('action')		# Check if postback
	if action == 'assign':
		_detail.assign(issue, request)
	elif action == 'set-label':
		_detail.set_label(issue, request)
	#elif action == 'set-due':
		#pass
	elif action:
		content = request.POST.get('content')
		if content: _detail.comment(issue, request)
		if action == 'toggle-state':
			_detail.toggle_state(issue, request)

	return render(request, 'issues_detail.html', {
		'issue': issue,
		'labels': Label.objects.all(),
		'users': User.objects.all(),
	})

@login_required
def create(request):
	errors = []

	if 'submit' in request.POST:
		(issue, errors) = _create.create(request)
		if issue: return redirect(reverse('issues:detail', args=(issue.id,)))

	return render(request, 'issues_create.html', {
		'labels': Label.objects.all(),
		'users': User.objects.all(),
		'errors': errors,
	})
