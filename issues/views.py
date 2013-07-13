from django.http import HttpResponse, Http404
from django.shortcuts import render

from issues.models import Issue

def list(request):
	issues = Issue.objects.order_by('+id')[:10]
	context = { 'issues': issues }
    return render(request, 'issues/list.html', context)
    
def create(request):
	return HttpResponse('Create issue')

def detail(request, id):
	try:
		issue = Issue.objects.get(pk=id)
	except Issue.DoesNotExist:
		raise Http404
	return render(request, 'issues/detail.html', { 'issue': issue })
