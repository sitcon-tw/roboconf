from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.models import *

@login_required
def list(request):
	users = User.objects.order_by('username').filter(is_active=True)
	filter = request.GET.get('g', '')
	if filter.isdigit():
		users = users.filter(group__pk=filter)

	return render(request, 'users_list.html', {
		'users': users.all(),
		'categories': GroupCategory.objects.all(),
		'filter': filter,
	})
