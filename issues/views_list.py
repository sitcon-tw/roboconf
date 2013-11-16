from django.shortcuts import render
from issues.models import *
from django.utils import timezone

order_mapping = { 'created': 'creation_time', 'due': 'due_time' }

def list(request, mode, user_id=None):
	if request.is_ajax():
		from core.api import not_implemented
		return not_implemented(request, {'error': 'not_implemented'})
		
	# Code here is just for demonstration purpose!
	# We'll need to move these into separate model
	if 'issues' in request.POST:
		issue_objs = []
		for issue_id in request.POST.get('issues').split(','):
			try:
				i = Issue.objects.get(id=issue_id)
				issue_objs.append(i)
			except ValueError, Issue.DoesNotExist: pass

		action = request.POST.get('action')
		if action == 'archive':
			# Do some archive
			for i in issue_objs:
				i.last_updated = timezone.now()
				i.save()

	counts = {
			'all': Issue.objects.count(),
			'assigned': Issue.objects.filter(assignee__pk=request.user.id).count(),
			'created': Issue.objects.filter(creator__pk=request.user.id).count(),
			'starred': Issue.objects.filter(starring__pk=request.user.id).count(),
		}

	dataset = None
	if mode == 'list': dataset = Issue.objects
	elif mode == 'assigned': dataset = Issue.objects.filter(assignee__pk=user_id)
	elif mode == 'created': dataset = Issue.objects.filter(creator__pk=user_id)
	elif mode == 'starred': dataset = Issue.objects.filter(starring__pk=user_id)

	is_open = not (request.GET.get('state') == 'closed')
	counts['open'] = dataset.filter(is_open=True).count()
	counts['closed'] = dataset.filter(is_open=False).count()
	dataset = dataset.filter(is_open=is_open)

	label = request.GET.get('label')
	if label and str(label).isdigit():
		dataset = dataset.filter(labels__pk=label)

	# Sort
	is_asc = (request.GET.get('direction') == 'asc')
	sort_order = request.GET.get('sort', 'created')
	dataset = dataset.order_by(('' if is_asc else '-') + order_mapping[sort_order])

	filters = { 'is_open': is_open, 'mode': mode }
	sorting = { 'asc': is_asc, 'desc': not is_asc, 'order': sort_order }

	return render(request, 'issues/list.html', {
		'current_url': request.path,
		'issues': dataset.all(),
		'labels': Label.objects.all(),
		'filters': filters,
		'sorting': sorting,
		'counts': counts,
	})
