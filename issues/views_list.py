from django.shortcuts import render
from issues.models import *

order_mapping = { 'created': 'creation_time', 'due': 'due_time' }

def datasets():
	return {
			'all': Issue.objects,
			'assigned': Issue.objects.filter(assignee__pk=user_id),
			'created': Issue.objects.filter(creator__pk=user_id),
			#'starred': ,
		}

def list(request, mode):
	dataset = datasets()[mode]
	counts = [s.count() for s in dataset]

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
	sorting = { 'asc': is_asc, 'desc': not is_asc, 'order': sorting }

	return render(request, 'issues_list.html', {
		'current_url': request.path,
		'issues': dataset,
		'labels': Label.objects.all(),
		'filters': filters,
		'sorting': sorting,
		'counts': counts,
	})
