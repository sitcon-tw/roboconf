from django.shortcuts import render
from django.contrib.auth.models import User, Group
from users.models import *

def list(request):
	return render(request, 'users_list.html', {
		'users': User.objects.order_by('username').all(),
		'groups': Group.objects.order_by('name').all(),
	})
