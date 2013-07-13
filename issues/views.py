from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic

from issues.models import Issue

class ListView(generic.ListView):
	template_name = 'issues_list.html'
	context_object_name = 'issues'

	def get_queryset(self):
		return Issue.objects.order_by('id')[:10]

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

	return render(request, 'issues/create.html', {})
