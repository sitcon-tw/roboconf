from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.models import *
from users.utils import get_user_sorting_key

def sorted_users(group_id=None):
	users = User.objects.filter(is_active=True)
	if group_id:
		users = users.filter(groups__id=group_id) 
	return sorted(users, key=get_user_sorting_key)

@login_required
def list(request):
	group = request.GET.get('g', '')
	return render(request, 'users_list.html', {
		'users': sorted_users(group_id=(None if not group.isdigit() else group)),
		'categories': GroupCategory.objects.all(),
		'filter': group,
	})

@login_required
def contacts(request):
	dataset = User.objects.filter(is_active=True)
	return render(request, 'users_contacts.html', {
		'users': sorted_users(),
		'show_details': request.user.groups.filter(id=11).exists(),	# Only show cellphone to staff
	})
