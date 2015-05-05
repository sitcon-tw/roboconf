from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from issues.models import Issue, IssueHistory, Label
from issues.utils import send_mail, filter_mentions, parse_date
from users.utils import sorted_users

@permission_required('issues.add_issue')
def create(request):
	errors = []

	if 'submit' in request.POST:

		issue = Issue()
		issue.title = request.POST['title']
		issue.content = request.POST['content']
		issue.creator = request.user

		due_time = request.POST.get('due_time', '').strip()
		if len(due_time):
			try:
				due_time = parse_date(due_time)
				if due_time:
					issue.due_time = due_time
				else:
					errors.append('date-misformed')
			except ValueError:
				errors.append('date-invalid')

		assignee = request.POST.get('assignee')
		if assignee:	# Empty value => not assigned, no need to set
			try:
				issue.assignee = User.objects.get(id=assignee)
			except User.DoesNotExist:
				assignee = None		# Just in case we're under attack...

		if not errors:
			issue.save()	# Need to save before we can enforce N to N relationship
			issue.starring.add(request.user)	# Auto watch

			mentions, extra_receivers = filter_mentions(issue.content)
			mentions -= set(request.user)
			for user in mentions:
				issue.starring.add(user)	# Auto watch
				send_mail(request.user, user, 'mail/issue_created.html', {'issue': issue})
			for receiver in extra_receivers:
				send_mail(request.user, receiver, 'mail/issue_created.html', {'issue': issue})

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
