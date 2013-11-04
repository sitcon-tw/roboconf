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

@login_required
def contacts(request):
	dataset = User.objects.filter(is_active=True)
	priority = [3, 1, 6, 5, 8, 2, 11]	# Sort by group type, team lead -> staff -> consultant
	def key(user):
		groups = [g.id for g in user.groups.all()]
		identity = ''.join([str(1 - groups.count(i)) for i in priority])	# Sort by identity first
		return '%s%s' % (identity, user.profile.display_name)
	users = sorted(dataset, key=key)
	return render(request, 'users_contacts.html', {
		'users': users,
		'show_details': request.user.groups.filter(id=11).exists(),	# Only show cellphone to staff
	})
