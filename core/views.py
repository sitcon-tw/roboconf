from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def index(request):
    context = {}
    context['submissions'] = request.user.submissions.all()

    return render(request, 'index.html', context)
