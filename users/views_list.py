from django.shortcuts import render
from django.contrib.auth.models import User, Group
from users.models import *

def list(request):
	return render(request, 'users_list.html', { 'users': User.objects.all(), 'groups': Group.objects.all() })
