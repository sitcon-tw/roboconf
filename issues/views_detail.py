# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils import timezone
from issues.models import *
from issues.utils import send_mail
from users.utils import get_user_name

def update(issue, user, content='', mode=IssueHistory.COMMENT):
	issue.last_updated = timezone.now()
	issue.save()
	IssueHistory.objects.create(issue=issue, user=user, mode=mode, content=content)

def notify(issue, user, content):
	message_subject = 'Re: [#%s] %s' % (issue.id, issue.title)
	for watcher in issue.starring.all():
		if user == watcher: continue
		send_mail(user, watcher, message_subject, content)

def assign(issue, request):
	if not request.user.has_perm('issues.assign_issue'):
		return	# Audit fail
		
	assignee = request.POST.get('assignee')
	if assignee is not None:					# empty string => unassign
		if len(assignee) > 0:
			try:
				u = User.objects.get(id=assignee)
				issue.assignee = u
				issue.starring.add(u)			# Automatic starring
				update(issue=issue, user=request.user, mode=IssueHistory.ASSIGN, content=assignee)
				notify(issue, request.user, u'* %s 已將此議題指派給 %s *' % (get_user_name(request.user), get_user_name(u)))
			except User.DoesNotExist: pass		# Just in case we're under attack...
		else:
			issue.assignee = None
			update(issue=issue, user=request.user, mode=IssueHistory.UNASSIGN)
			notify(issue, request.user, u'* %s 已撤銷此議題指派的人員*' % (get_user_name(request.user)))

def set_label(issue, request):
	if not (issue.assignee == request.user or request.user.has_perm('issues.label_issue')):
		return	# Audit fail
		
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

	body = [u' %s 已為此議題']
	if len(labels_to_remove) > 0:
		body.append(u'移除標籤* ')
		body.append(u'、'.join([(u'「%s」' % l.name) for l in labels_to_remove]))
		if len(labels_to_add) > 0:
			body.append(u' *，同時')

	if len(labels_to_add) > 0:
		body.append(u'套用標籤* ')
		body.append(u'、'.join([(u'「%s」' % l.name) for l in labels_to_add]))

	notify(issue, request.user, ''.join(body))

def comment(issue, request):
	if not request.user.has_perm('issues.comment_issue'):
		return	# Audit fail

	content = request.POST.get('content')
	if content:
		update(issue=issue, user=request.user, content=content)
		notify(issue, request.user, content)

def toggle_state(issue, request):
	if not request.user.has_perm('issues.toggle_issue'):
		return	# Audit fail

	issue.is_open = not issue.is_open
	update(issue=issue, user=request.user, mode=(IssueHistory.REOPEN if issue.is_open else IssueHistory.CLOSE))
	notify(issue, request.user, (u'* %s 已將此議題結案 *' if issue.is_open else u'* %s 已對此議題提出復議 *') % (get_user_name(request.user)))

def toggle_star(issue, request):
	if issue.starring.filter(id=request.user.id).count():
		issue.starring.remove(request.user)
	else:
		issue.starring.add(request.user)

def edit(issue, request):
	if request.user == issue.creator or request.user.has_perm('issues.change_issue'):
		pass	# Audit success
	else:
		pass	# Audit fail
