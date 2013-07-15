from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import dateparse
import datetime

from issues.models import Issue, Label, IssueHistory

order_mapping = { 'created': 'creation_time', 'due': 'due_time' }

@login_required
def list_common(request, dataset, mode):
	# Filter
	is_open = not (request.GET.get('state') == 'closed')
	dataset = dataset.filter(is_open=is_open)

	label = request.GET.get('label')
	if label and str(label).isdigit():
		dataset = dataset.filter(labels__pk=label)

	# Sort
	is_asc = (request.GET.get('direction') == 'asc')
	sorting = request.GET.get('sort', 'created')
	dataset = dataset.order_by(('' if is_asc else '-') + order_mapping[sorting])

	return render(request, 'issues_list.html', {
		'current_url': request.path,
		'issues': dataset,
		'labels': Label.objects.all(),
		'sorting': sorting,
		'is_asc': is_asc,
		'is_open': is_open,
		'mode': mode,
	})

def list(request):
	return list_common(request, dataset=Issue.objects.all(), mode='list')

def assigned(request, user_id):
	return list_common(request, dataset=Issue.objects.filter(assignee__pk=user_id), mode='assigned')

def created(request, user_id):
	return list_common(request, dataset=Issue.objects.filter(creator__pk=user_id), mode='created')

def starred(request, user_id):
	# TODO: Implement "starring" (a.k.a watch issue)
	return redirect(reverse('issues:list'))

@login_required
def detail(request, issue_id):
	issue = get_object_or_404(Issue, pk=issue_id)
	mode = ''

	# Check if postback
	if 'action' in request.POST:
		action = request.POST['action']
		if action == 'assign':
			if 'assignee' in request.POST:
				try:
					issue.assignee = User.objects.get(id=request.POST.get('assignee'))
					issue.save()
				except User.DoesNotExist:
					pass	# Just in case we're under attack...

		elif action == 'set-label':
			pass
		else:
			# Comment on this issue
			content = request.POST['content']
			if not content:
				mode = 'error-no-content'
			else:
				entry = IssueHistory(issue=issue, user=request.user)
				entry.content = content
				entry.save()

			# Check if also change state
			if action == 'toggle-state':
				entry = IssueHistory(issue=issue, user=request.user)
				entry.mode = IssueHistory.CLOSE if issue.is_open else IssueHistory.REOPEN
				entry.save()

				issue.is_open = not issue.is_open
				issue.save()

	return render(request, 'issues_detail.html', {
		'issue': issue,
		'users': User.objects.all(),
		'mode': mode,
	})

@login_required
def create(request):
	if 'submit' in request.POST:
		i = Issue()
		i.title = request.POST['title']
		i.content = request.POST['content']
		i.creator = request.user

		if 'due_time' in request.POST:
			try:
				due_time = request.POST['due_time'].strip()
				if len(due_time) <= 10:
					due_time = datetime.datetime.combine(dateparse.parse_date(due_time), datetime.time())
				else:
					due_time = dateparse.parse_datetime(due_time)

				if due_time:
					i.due_time = due_time
				else:
					pass	# Do some warnings here
			except ValueError:
				pass		# Do some warnings here

		if 'assignee' in request.POST:
			try:
				i.assignee = User.objects.get(id=request.POST.get('assignee'))
			except User.DoesNotExist:
				pass	# Just in case we're under attack...

		for label_id in request.POST.getlist('labels'):
			try:
				i.labels.add(Label(id=label_id))
			except Label.DoesNotExist:
				pass	# Never mind...

		i.save()

		return redirect(reverse('issues:detail', args=(i.id,)))

	return render(request, 'issues_create.html', {
		'labels': Label.objects.all(),
		'users': User.objects.all(),
	})
