# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import dateparse
from issues.models import *
from notifications.models import Message
import datetime

def create(request):
	errors = []
	
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

		if assignee:
			IssueHistory.objects.create(issue=issue, user=request.user,
										mode=IssueHistory.ASSIGN, content=assignee)

			issue.starring.add(issue.assignee)	# Auto watch
			Message.create_from_user(request.user, issue.assignee, 
				'[#%s] %s' % (issue.id, issue.title), 
				unicode('* %s 已將此議題指派給你 *\n\n%s') % (request.user.username, issue.content)
			)

		if due_time:
			IssueHistory.objects.create(issue=issue, user=request.user, 
										mode=IssueHistory.SET_DUE, content=due_time)


		# Add or remove labels has history so we don't worry on history creation
		for label_id in request.POST.getlist('labels'):
			try:
				issue.labels.add(Label.objects.get(id=label_id))
			except Label.DoesNotExist: pass

		issue.save()	# Now save the labels
		return (issue, [])
	return (None, errors)
