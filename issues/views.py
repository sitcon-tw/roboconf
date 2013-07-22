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
def __list(request, dataset, mode):
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
	return __list(request, dataset=Issue.objects.all(), mode='list')

def assigned(request, user_id):
	return __list(request, dataset=Issue.objects.filter(assignee__pk=user_id), mode='assigned')

def created(request, user_id):
	return __list(request, dataset=Issue.objects.filter(creator__pk=user_id), mode='created')

def starred(request, user_id):
	# TODO: Implement "starring" (a.k.a watch issue)
	return redirect(reverse('issues:list'))

@login_required
def detail(request, issue_id):
	issue = get_object_or_404(Issue, pk=issue_id)

	# Check if postback
	action = request.POST.get('action')
	if action == 'assign':
		assignee = request.POST.get('assignee')
		if assignee is not None:	# empty string => unassign
			if len(assignee) > 0:
				try:
					issue.assignee = User.objects.get(id=assignee)
					issue.save_with_history(user=request.user, mode=IssueHistory.ASSIGN, content=assignee)
				except User.DoesNotExist:
					pass			# Just in case we're under attack...
			else:
				issue.assignee = None
				issue.save_with_history(user=request.user, mode=IssueHistory.UNASSIGN)

	elif action == 'set-label':
		old_labels = [l.id for l in issue.labels.all()]
		new_labels = []

		for label_str in request.POST.getlist('labels'):
			try:
				new_labels.append(int(label_str))
			except ValueError:
				pass

		# Remove unused labels
		for label_id in [l for l in old_labels if l not in new_labels]:
			# Old labels won't have integrity issues so eliminate try block
			issue.labels.remove(Label.objects.get(id=label_id))
			issue.save_with_history(user=request.user, mode=IssueHistory.UNLABEL, content=label_id)

		# Add new
		for label_id in [l for l in new_labels if l not in old_labels]:
			try:
				issue.labels.add(Label.objects.get(id=label_id))
				issue.save_with_history(user=request.user, mode=IssueHistory.LABEL, content=label_id)
			except Label.DoesNotExist:
				pass

		issue.save()

	#elif action == 'set-due':
	#	pass

	elif action:
		# Comment on this issue
		content = request.POST.get('content')
		if content:
			issue.save_with_history(user=request.user, content=content)

		# Check if also change state
		if action == 'toggle-state':
			issue.is_open = not issue.is_open
			issue.save_with_history(user=request.user, mode=(IssueHistory.CLOSE if issue.is_open else IssueHistory.REOPEN))

	return render(request, 'issues_detail.html', {
		'issue': issue,
		'labels': Label.objects.all(),
		'users': User.objects.all(),
	})

@login_required
def create(request):
	errors = []
	if 'submit' in request.POST:
		issue = Issue()
		issue.title = request.POST['title']
		issue.content = request.POST['content']
		issue.creator = request.user

		due_time = request.POST.get('due_time', '').strip()
		if len(due_time) > 0:
			try:
				if len(due_time) <= 10:
					due_time = dateparse.parse_date(due_time)
					due_time = datetime.datetime.combine(due_time, datetime.time()) if due_time else None
				else:
					due_time = dateparse.parse_datetime(due_time)
			except ValueError:
				errors.append('date-invalid')

			if due_time:
				issue.due_time = due_time
			else:
				errors.append('date-misformed')

		assignee = request.POST.get('assignee')
		if assignee:	# Empty value => not assigned, no need to set
			try:
				assignee = request.POST.get('assignee')
				issue.assignee = User.objects.get(id=assignee)
			except User.DoesNotExist:
				assignee = None		# Just in case we're under attack...

		if len(errors) < 1:
			issue.save()	# Need to save before we can enforce N to N relationship

			if assignee:
				IssueHistory.objects.create(issue=issue, user=request.user,
											mode=IssueHistory.ASSIGN, content=assignee)
			if due_time:
				IssueHistory.objects.create(issue=issue, user=request.user, 
											mode=IssueHistory.SET_DUE, content=due_time)

			for label_id in request.POST.getlist('labels'):
				try:
					issue.labels.add(Label.objects.get(id=label_id))
					# Add or remove labels has history so we don't worry on history creation
				except Label.DoesNotExist:
					pass

			issue.save()	# Now save the labels
			return redirect(reverse('issues:detail', args=(issue.id,)))

	return render(request, 'issues_create.html', {
		'labels': Label.objects.all(),
		'users': User.objects.all(),
		'errors': errors,
	})
