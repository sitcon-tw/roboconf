# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone
from core.utils import *
from issues.models import *
from notifications.models import Message

def update(issue, user, content='', mode=IssueHistory.COMMENT):
	issue.last_updated = timezone.now()
	issue.save()
	IssueHistory.objects.create(issue=issue, user=user, mode=mode, content=content)

def notify(issue, user, content):
	message_subject = 'Re: [#%s] %s' % (issue.id, issue.title)
	for watcher in issue.starring.all():
		if user == watcher: continue
		Message.create_from_user(user, watcher, message_subject, content)

def assign(issue, request):
	assignee = request.POST.get('assignee')
	if assignee is not None:					# empty string => unassign
		if len(assignee) > 0:
			try:
				u = User.objects.get(id=assignee)
				issue.assignee = u
				issue.starring.add(u)			# Automatic starring
				update(issue=issue, user=request.user, mode=IssueHistory.ASSIGN, content=assignee)
				notify(issue, request.user, U('* %s 已將此議題指派給 %s *') % (request.user.username, u.username))
			except User.DoesNotExist: pass		# Just in case we're under attack...
		else:
			issue.assignee = None
			update(issue=issue, user=request.user, mode=IssueHistory.UNASSIGN)
			notify(issue, request.user, U('* %s 已撤銷此議題指派的人員*') % (request.user.username))

def set_label(issue, request):
	old_labels = [l.id for l in issue.labels.all()]
	new_labels = []

	for label_str in request.POST.getlist('labels'):
		try:
			new_labels.append(int(label_str))
		except ValueError: pass

	# Remove unused labels
	labels_to_remove = [l for l in old_labels if l not in new_labels]
	labels_to_add = [l for l in new_labels if l not in old_labels]

	# * Old labels won't have integrity issues so eliminate try block
	for label_id in labels_to_remove:
		issue.labels.remove(Label.objects.get(id=label_id))
		update(issue=issue, user=request.user, mode=IssueHistory.UNLABEL, content=label_id)

	# Add new labels
	for label_id in labels_to_add:
		try:
			issue.labels.add(Label.objects.get(id=label_id))
			update(issue=issue, user=request.user, mode=IssueHistory.LABEL, content=label_id)
		except Label.DoesNotExist:
			pass

	issue.save()

	body = [U('* %s 已為此議題')]
	if len(labels_to_remove) > 0:
		body.append(U('移除標籤* '))
		body.append(U('、').join([(U('「%s」') % l.name) for l in labels_to_remove]))
		if len(labels_to_add) > 0:
			body.append(U(' *，同時'))

	if len(labels_to_add) > 0:
		body.append(U('套用標籤* '))
		body.append(U('、').join([(U('「%s」') % l.name) for l in labels_to_add]))

	notify(issue, request.user, ''.join(body))

def comment(issue, request):
	content = request.POST.get('content')
	if content:
		update(issue=issue, user=request.user, content=content)
		notify(issue, request.user, content)

def toggle_state(issue, request):
	issue.is_open = not issue.is_open
	update(issue=issue, user=request.user, mode=(IssueHistory.REOPEN if issue.is_open else IssueHistory.CLOSE))
	notify(issue, request.user, U('* %s 已將此議題結案 *' if issue.is_open else '* %s 已對此議題提出復議 *') % (request.user.username))

def toggle_star(issue, request):
	if issue.starring.filter(id=request.user.id).count():
		issue.starring.remove(request.user)
	else:
		issue.starring.add(request.user)
