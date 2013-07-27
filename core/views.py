from django.shortcuts import render

def index(request):
	context = {}
	
	if request.user.is_authenticated():
		context['issues'] = request.user.assigned_issues.filter(is_open=True).all()

	return render(request, 'core_index.html', context)
