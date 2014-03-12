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
				'name': u.profile.name(),
				'title': u.profile.title,
				'avatar': u.profile.avatar(),	
			}
			for u in sorted_users(group_id=11)
		],
	})

@login_required
def contacts(request):
	show_details = request.GET.get('details') and request.user.has_perm('auth.change_user')
	return render(request, 'users/contacts.html', {
		'users': sorted_users(),
		'show_details': show_details, 
		'is_trusted': show_details or request.user.groups.filter(id=11).exists(),	# Only show cellphone to staff
	})

#@login_required
def export(request, format=None):
	formats = {
		'html': ('text/html', 'users/export.html'), 
		'csv': ('text/csv', 'users/export.csv'), 
		'xml': ('application/xml', 'users/export.xml'), 
	}

	if format and format not in formats.keys():
		from django.http import Http404
		raise Http404

	users = []
	authorized = request.user.groups.filter(id=11).exists()
	trusted = authorized and request.user.has_perm('auth.change_user')

	for user in sorted_users():
		entity = {
			'id': user.username, 
			'name': user.profile.name(), 
			'title': user.profile.title, 
			'avatar': user.profile.avatar(), 
			'email': user.email, 
		}
		
		if authorized:
			entity['phone'] = user.profile.phone

		if trusted:
			entity['model_id'] = user.id
			entity['last_name'] = user.last_name
			entity['first_name'] = user.first_name
			entity['school'] = user.profile.school
			entity['grade'] = user.profile.grade
			entity['comment'] = user.profile.comment
			entity['groups'] = ' '.join([g.id for g in user.groups.all()])

		users.append(entity)


	content_type, template = formats[format or 'html']
	return render(request, template, { 'users': users }, content_type=content_type)
