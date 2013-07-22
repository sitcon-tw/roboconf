from django.shortcuts import render
from issues.models import *

order_mapping = { 'created': 'creation_time', 'due': 'due_time' }

def list(request, mode, user_id=None):
	counts = {
			'all': Issue.objects.count(),
			'assigned': Issue.objects.filter(assignee__pk=request.user.id).count(),
			'created': Issue.objects.filter(creator__pk=request.user.id).count(),
			#'starred': '',
		}

	dataset = None
	if mode == 'list': dataset = Issue.objects
	elif mode == 'assigned': dataset = Issue.objects.filter(assignee__pk=user_id)
	elif mode == 'created': dataset = Issue.objects.filter(creator__pk=user_id)
	#elif mode == 'starred':

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

	return render(request, 'issues_list.html', {
		'current_url': request.path,
		'issues': dataset.all(),
		'labels': Label.objects.all(),
		'filters': filters,
		'sorting': sorting,
		'counts': counts,
	})
