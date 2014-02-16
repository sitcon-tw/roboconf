from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from core.api.decorators import api_endpoint, ajax_required
from core.api.views import *
from issues.models import Issue, Label

@api_endpoint
@ajax_required(redirect_url='issues:list')
def ajax(request):
	return not_implemented(request, {'error': 'not_implemented'})

@login_required
def list(request, filter=None):
	dataset = Issue.objects
	counts = {
		'all': Issue.objects.count(),
	}

	# 1st phase filtering
	if not filter: filter = {}
	if 'assignee' in filter:
		dataset = dataset.filter(assignee__id=filter['assignee'])
	if 'creator' in filter:
		dataset = dataset.filter(creator__id=filter['creator'])
	if 'starring' in filter:
		dataset = dataset.filter(starring__id=filter['starring'])
	
	# 1st phase counting
	counts['open'] = dataset.filter(is_open=True).count()
	counts['closed'] = dataset.filter(is_open=False).count()

	# 2nd phase parameter parsing
	filter['is_open'] = not (request.GET.get('state') == 'closed')

	label = request.GET.get('label')
	if label and str(label).isdigit():
		filter['label'] = label

	sort_order = request.GET.get('direction')
	if request.GET.get('sort') == 'due':
		filter['due_time'] = '-' if sort_order == 'desc' else '+'
	else:
		filter['creation_time'] = '+' if sort_order == 'asc' else '-'

	# 2nd phase filtering
	dataset = dataset.filter(is_open=filter['is_open'])
	if 'label' in filter:
		dataset = dataset.filter(label__id=filter['label'])
	if 'due_time' in filter:
		dataset = dataset.order_by('due_time' if filter['due_time'] == '+' else '-due_time')
	if 'creation_time' in filter:
		dataset = dataset.order_by('creation_time' if filter['creation_time'] == '+' else '-creation_time')

	return render(request, 'issues/list.html', {
		'issues': dataset.all(),
		'labels': Label.objects.all(),
		'filter': filter,
		'counts': counts,
	})

@login_required
def assigned(request, user_id):
	return list(request, {'assignee': user_id})

@login_required
def created(request, user_id):
	return list(request, {'creator': user_id})

@login_required
def starred(request, user_id):
	return list(request, {'starring': user_id})
