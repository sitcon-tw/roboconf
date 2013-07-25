from django.shortcuts import render

def index(request):
	return render(request, 'core_index.html', {
		'issues': request.user.assigned_issues.filter(is_open=True).all(),
	})
