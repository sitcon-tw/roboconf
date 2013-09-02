from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.models import *

@login_required
def list(request):
	dataset = User.objects
	group = request.GET.get('g')
	if group and str(group).isdigit():
		dataset = dataset.filter(groups__pk=group)

	return render(request, 'users_list.html', {
		'users': dataset.order_by('username').filter(is_active=True).all(),
		'categories': GroupCategory.objects.all(),
		'filter': filter,
	})
