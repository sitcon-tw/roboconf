from django.shortcuts import render, get_object_or_404

from issues.models import Issue

def list(request):
	issues = Issue.objects.order_by('+id')[:10]
	return render(request, 'issues/list.html', { 'issues': issues })
    
def create(request):
	return render(request, 'issues/create.html', {})

def detail(request, id):
	issue = get_object_or_404(Issue, pk=id)
	return render(request, 'issues/detail.html', { 'issue': issue })
