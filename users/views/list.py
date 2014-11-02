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

	users = User.objects.all()
	filters = request.GET.getlist('find')
	groups = request.GET.get('g')
	trusted = is_trusted_user(request.user)

	if 'disabled' in filters and trusted:
		users = users.filter(is_active=False)
	elif 'all' not in filters or not trusted:
		users = users.filter(is_active=True)

	if groups:
		groups = [int(g) for g in groups.split(',') if g.isdigit()]
		to_include = [g for g in groups if g >= 0]
		to_exclude = [-g for g in groups if g < 0]

		if to_include:
			users = users.filter(groups__in=to_include)

		if to_exclude:
			users = users.exclude(groups__in=to_exclude)

		filters += groups

	return render(request, 'users/list.html', {
		'users': sorted_users(users),
		'categories': sorted_categories,
		'filters': filters,
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
			for u in sorted_users(Users.objects.filter(is_active=True, groups=11))
		],
	})

@login_required
def contacts(request):
	return render(request, 'users/contacts.html', {
		'users': sorted_users(),
		'authorized': is_authorized_user(request.user),
		'show_details': request.GET.get('details') and is_trusted_user(request.user),
	})

#@login_required
def export(request, format=None):
	formats = {
		'html': ('text/html', 'users/export.html'),
		'csv': ('text/csv', 'users/export.csv'),
		'xml': ('application/xml', 'users/export.xml'),
		'vcard': ('text/vcard', 'users/export.vcf'),
	}

	if format and format not in formats.keys():
		from django.http import Http404
		raise Http404

	users = []
	authorized = is_authorized_user(request.user)
	trusted = is_trusted_user(request.user)
	user_source = User.objects.filter(is_active=True) if not trusted else User.objects.all()

	for user in sorted_users(user_source):
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
			entity['groups'] = ' '.join([str(g.id) for g in user.groups.all()])

		users.append(entity)


	content_type, template = formats[format or 'html']
	return render(request, template, { 'users': users }, content_type=content_type)
