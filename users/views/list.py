from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.models import *

@login_required
def list(request):
	users = User.objects
	if 'g' in request.GET:
		try:
			g = Group.objects.get(id=request.GET['g'])
			users = g.users
		except ValueError, Group.DoesNotExist: pass

	return render(request, 'users_list.html', {
		'users': users.order_by('username').filter(is_active=True).all(),
		'categories': GroupCategory.objects.all(),
		'filter': filter,
	})
