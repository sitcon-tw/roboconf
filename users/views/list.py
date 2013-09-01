from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.models import *

@login_required
def list(request):
	return render(request, 'users_list.html', {
		'users': User.objects.order_by('username').filter(is_active=True).all(),
		'groups': Group.objects.order_by('name').all(),
	})
