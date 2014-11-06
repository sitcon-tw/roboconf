from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.utils import dateparse
from issues.models import *
from issues.utils import send_mail
from users.utils import sorted_users
import datetime
import re

@permission_required('issues.add_issue')
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

			if due_time: issue.due_time = due_time
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
			issue.starring.add(request.user)	# Auto watch

			mentions = set(re.findall(r'(?<=@)[0-9A-Za-z_\-]+', issue.content))
			for mention in mentions:
				try:
					mentionee = User.objects.get(username=mention)
				except User.DoesNotExist:
					continue

				issue.starring.add(mentionee)	# Auto watch
				send_mail(request.user, mentionee, 'mail/issue_mentioned.html', {'issue': issue, 'new_topic': True})

			if assignee:
				IssueHistory.objects.create(issue=issue, user=request.user,
											mode=IssueHistory.ASSIGN, content=assignee)

				issue.starring.add(issue.assignee)	# Auto watch
				send_mail(request.user, issue.assignee, 'mail/issue_assigned.html', {'issue': issue, 'new_topic': True})

			if due_time:
				IssueHistory.objects.create(issue=issue, user=request.user,
											mode=IssueHistory.SET_DUE, content=due_time)


			# Add or remove labels has history so we don't worry on history creation
			for label_id in request.POST.getlist('labels'):
				try:
					issue.labels.add(Label.objects.get(id=label_id))
				except Label.DoesNotExist: pass

			issue.save()	# Now save the labels
			return redirect('issues:detail', issue.id)

	return render(request, 'issues/create.html', {
		'labels': Label.objects.all(),
		'users': sorted_users(User.objects.filter(is_active=True)),
		'errors': errors,
	})
