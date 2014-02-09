from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from users.models import *
from users.utils import *
from core.decorators import api_endpoint

def sorted_users(group_id=None):
	users = User.objects.filter(is_active=True)
	if group_id:
		users = users.filter(groups__id=group_id) 
	return sorted(users, key=get_user_sorting_key)

@api_endpoint(public=True)
def list(request):
	if request.is_ajax():
		from core.api import *

		result = {}
		for u in User.objects.filter(is_active=True, groups__id=11):
			result[u.username] = {
				"name": get_user_name(u),
				"title": u.profile.title,
				"avatar": get_avatar_url(u.email),
			}
		
		return render_json(request, result)
	
	elif not request.user.is_authenticated():
		from django.contrib.auth.views import redirect_to_login
		return redirect_to_login(request.path)

	group = request.GET.get('g', '')
	group = None if not group.isdigit() else int(group)
	return render(request, 'users/list.html', {
		'users': sorted_users(group_id=group),
		'categories': GroupCategory.objects.all(),
		'filter': group,
	})

@login_required
def contacts(request):
	dataset = User.objects.filter(is_active=True)
	return render(request, 'users/contacts.html', {
		'users': sorted_users(),
		'show_details': request.user.groups.filter(id=11).exists(),	# Only show cellphone to staff
	})
