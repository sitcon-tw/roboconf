from django.http import HttpResponse

def list(request):
    return HttpResponse('Issue Tracker')
    
def create(request):
	return HttpResponse('Create issue')

def detail(request, id):
	return HttpResponse('Issue #%s' % id)
