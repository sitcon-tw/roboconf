from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    context = {}
    context['issues'] = request.user.assigned_issues.filter(is_open=True).all()

    return render(request, 'index.html', context)
