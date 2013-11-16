from django.shortcuts import render

def index(request):
	context = {}
	
	if request.user.is_authenticated():
		context['issues'] = request.user.assigned_issues.filter(is_open=True).all()

	return render(request, 'index.html', context)

# since Django 1.5 hasn't include this...
def bad_request(request):
	from django.http import HttpResponseBadRequest
	from django.template import (loader, Context)
	template = loader.get_template('400.html')
	return HttpResponseBadRequest(template.render(Context({})))
