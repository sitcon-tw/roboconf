from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic

from issues.models import Issue

order_mapping = { 'created': 'creation_time', 'due': 'due_time' }

def list(request, dataset=None, action='list'):
	context = list_context()
	if not dataset:
		dataset = Issue.objects.all()

	# Filter
	state = not (request.GET.get('state') == 'closed')
	dataset.filter(is_open=state)

	label = request.GET.get('label')
	if label and str(label).isdigit():
		dataset.filter(labels__pk=label)

	# Sort
	direction = (request.GET.get('direction') == 'asc')
	sorting = request.GET.get('sort', 'created')
	dataset.order_by(('' if direction else '-') + order_mapping[sorting])

	context['current_url'] = request.path 
	context['issues'] = dataset
	context['sorting'] = sorting
	context['is_asc'] = direction
	context['is_open'] = state
	context['mode'] = action
	return render(request, 'issues_list.html', context)

def assigned(request, user_id):
	return list(request, dataset=Issue.objects.filter(assignee__pk=user_id), action='assigned')

def created(request, user_id):
	return list(request, dataset=Issue.objects.filter(creator__pk=user_id), action='created')

def starred(request, user_id):
	# TODO: Implement "starring" (a.k.a watch issue)
	return HttpResponseRedirect(reverse('issues:list'))

class DetailView(generic.DetailView):
	model = Issue
	template_name = 'issues_detail.html'

#@login_required
def create(request):
	if 'submit' in request.POST:
		# TODO: Check permissions
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('issues:list'))

		i = Issue()
		i.title = request.POST['title']
		i.content = request.POST['content']
		i.creator = request.user
		i.save()

		return HttpResponseRedirect(reverse('issues:detail', args=(i.id,)))

	return render(request, 'issues_create.html', {})
