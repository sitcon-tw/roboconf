from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.settings.base import SUBMISSION_END
import datetime

@login_required
def index(request):
    context = {}
    context['submissions'] = request.user.submissions.all()
    context['expired'] = SUBMISSION_END < datetime.datetime.now()

    return render(request, 'index.html', context)
