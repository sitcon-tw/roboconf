from django.shortcuts import render
from users.models import *

def index(request):
    team_list = GroupCategory.objects.get(pk=settings.TEAM_GROUPCAT_ID).groups.all()
    context = {
            'teams': filter(lambda x: x in request.user.groups.all(), team_list)
            }

    return render(request, 'index.html', context)
