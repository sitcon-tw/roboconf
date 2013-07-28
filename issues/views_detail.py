from django.contrib.auth.models import User
from django.utils import timezone
from issues.models import *
from notifications.models import Message

def update(issue, user, content='', mode=IssueHistory.COMMENT):
	issue.last_updated = timezone.now()
	issue.save()
	IssueHistory.objects.create(issue=issue, user=user, mode=mode, content=content)


def assign(issue, request):
	assignee = request.POST.get('assignee')
	if assignee is not None:					# empty string => unassign
		if len(assignee) > 0:
			try:
				issue.assignee = User.objects.get(id=assignee)
				update(issue=issue, user=request.user, mode=IssueHistory.ASSIGN, content=assignee)
			except User.DoesNotExist: pass		# Just in case we're under attack...
		else:
			issue.assignee = None
			update(issue=issue, user=request.user, mode=IssueHistory.UNASSIGN)

def set_label(issue, request):
	old_labels = [l.id for l in issue.labels.all()]
	new_labels = []

	for label_str in request.POST.getlist('labels'):
		try:
			new_labels.append(int(label_str))
		except ValueError: pass

	# Remove unused labels
	# * Old labels won't have integrity issues so eliminate try block
	for label_id in [l for l in old_labels if l not in new_labels]:
		issue.labels.remove(Label.objects.get(id=label_id))
		update(issue=issue, user=request.user, mode=IssueHistory.UNLABEL, content=label_id)

	# Add new labels
	for label_id in [l for l in new_labels if l not in old_labels]:
		try:
			issue.labels.add(Label.objects.get(id=label_id))
			update(issue=issue, user=request.user, mode=IssueHistory.LABEL, content=label_id)
		except Label.DoesNotExist:
			pass

	issue.save()

def comment(issue, request):
	content = request.POST.get('content')
	if content:
		update(issue=issue, user=request.user, content=content)

		message_subject = 'Re: [#%s] %s' % (issue.id, issue.title)
		for watcher in issue.starring.all():
			Message.create_from_user(request.user, watcher, message_subject, content)

def toggle_state(issue, request):
	issue.is_open = not issue.is_open
	update(issue=issue, user=request.user, mode=(IssueHistory.REOPEN if issue.is_open else IssueHistory.CLOSE))

def toggle_star(issue, request):
	if issue.starring.filter(user=request.user).count():
		issue.starring.remove(request.user)
	else:
		issue.starring.add(request.user)
