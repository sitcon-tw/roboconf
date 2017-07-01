from django.shortcuts import render
from users.models import *

def index(request):
    context = {
            'teams': GroupCategory.objects.get(pk=settings.TEAM_GROUPCAT_ID).groups.all()
            }

    return render(request, 'index.html', context)
