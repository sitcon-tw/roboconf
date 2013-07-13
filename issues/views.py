from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic

from issues.models import Issue, Label

order_mapping = { 'created': 'creation_time', 'due': 'due_time' }

def list(request, dataset=None, mode='list'):
	if not dataset:
		dataset = Issue.objects.all()

	# Filter
	is_open = not (request.GET.get('state') == 'closed')
	dataset.filter(is_open=is_open)

	label = request.GET.get('label')
	if label and str(label).isdigit():
		dataset.filter(labels__pk=label)

	# Sort
	is_asc = (request.GET.get('direction') == 'asc')
	sorting = request.GET.get('sort', 'created')
	dataset.order_by(('' if is_asc else '-') + order_mapping[sorting])

	return render(request, 'issues_list.html', {
		'current_url': request.path,
		'issues': dataset,
		'labels': Label.objects.all(),
		'sorting': sorting,
		'is_asc': is_asc,
		'is_open': is_open,
		'mode': mode,
	})

def assigned(request, user_id):
	return list(request, dataset=Issue.objects.filter(assignee__pk=user_id), mode='assigned')

def created(request, user_id):
	return list(request, dataset=Issue.objects.filter(creator__pk=user_id), mode='created')

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
