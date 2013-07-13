from django.http import HttpResponse
from django.template import RequestContext, loader

from issues.models import Issue

def list(request):
	issues = Issue.objects.order_by('+id')[:10]
	template = loader.get_template('issues/list.html')
	context = RequestContext(request, {
			'issues': issues,
		})
    return HttpResponse(template.render(context))
    
def create(request):
	return HttpResponse('Create issue')

def detail(request, id):
	return HttpResponse('Issue #%s' % id)
