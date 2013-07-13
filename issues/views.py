from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from issues.models import Issue

def list(request):
	issues = Issue.objects.order_by('id')[:10]
	return render(request, 'issues/list.html', { 'issues': issues })
    
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

def detail(request, id):
	issue = get_object_or_404(Issue, pk=id)
	return render(request, 'issues/detail.html', { 'issue': issue })
