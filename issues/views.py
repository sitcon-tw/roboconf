from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from views_list import *
from views_detail import *
from views_create import *
from issues.models import *

@login_required
def list(request):
	return __list(request, dataset=Issue.objects.all(), mode='list')

@login_required
def assigned(request, user_id):
	return __list(request, dataset=Issue.objects.filter(assignee__pk=user_id), mode='assigned')

@login_required
def created(request, user_id):
	return __list(request, dataset=Issue.objects.filter(creator__pk=user_id), mode='created')

@login_required
def starred(request, user_id):
	# TODO: Implement "starring" (a.k.a watch issue)
	return redirect(reverse('issues:list'))

@login_required
def detail(request, issue_id):
	issue = get_object_or_404(Issue, pk=issue_id)

	action = request.POST.get('action')		# Check if postback
	if action == 'assign':
		__assign(issue, request)
	elif action == 'set-label':
		__set_label(issue, request)
	#elif action == 'set-due':
		#pass
	elif action:
		content = request.POST.get('content')
		if content: __comment(issue, request)
		if action == 'toggle-state':
			__toggle_state(issue, request)

	return render(request, 'issues_detail.html', {
		'issue': issue,
		'labels': Label.objects.all(),
		'users': User.objects.all(),
	})

@login_required
def create(request):
	errors = []

	if 'submit' in request.POST:
		(issue, errors) = __create(request)
		if issue: return redirect(reverse('issues:detail', args=(issue.id,)))

	return render(request, 'issues_create.html', {
		'labels': Label.objects.all(),
		'users': User.objects.all(),
		'errors': errors,
	})
