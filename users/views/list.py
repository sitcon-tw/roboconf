from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from core.api.decorators import api_endpoint, ajax_required
from core.api.views import render_json
from users.models import *
from users.utils import *

def list(request):
	if not request.user.is_authenticated():
		from django.contrib.auth.views import redirect_to_login
		return redirect_to_login(request.path)

	group = request.GET.get('g', '')
	group = None if not group.isdigit() else int(group)
	return render(request, 'users/list.html', {
		'users': sorted_users(group_id=group),
		'categories': GroupCategory.objects.all(),
		'filter': group,
	})

@api_endpoint(public=True)
@ajax_required(redirect_url='users:list')
def ajax(request):
	return render_json(request, {
		'status': 'success',
		'users': [
			{
				'id': u.username,
				'name': get_user_name(u),
				'title': u.profile.title,
				'avatar': get_avatar_url(u.email),	
			}
			for u in sorted_users(group_id=11)
		],
	})

@login_required
def contacts(request):
	dataset = User.objects.filter(is_active=True)
	return render(request, 'users/contacts.html', {
		'users': sorted_users(),
		'show_details': request.user.groups.filter(id=11).exists(),	# Only show cellphone to staff
	})
