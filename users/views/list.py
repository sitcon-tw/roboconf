from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from core.api.decorators import api_endpoint, ajax_required
from core.api.views import render_json
from users.utils import sorted_users, sorted_categories

formats = {
	'html': ('text/html', 'users/export.html'),
	'csv': ('text/csv', 'users/export.csv'),
	'xml': ('application/xml', 'users/export.xml'),
	'vcard': ('text/vcard', 'users/export.vcf'),
}

def list(request):
	if not request.user.is_authenticated():
		from django.contrib.auth.views import redirect_to_login
		return redirect_to_login(request.path)
	elif not request.user.profile.is_authorized():
		return redirect('index')

	filters = request.GET.getlist('find')
	groups = request.GET.get('g')
	trusted = request.user.profile.is_trusted()
	users = apply_filter(filters=filters, groups=groups, trusted=trusted)

	return render(request, 'users/list.html', {
		'users': sorted_users(users),
		'categories': sorted_categories,
		'filters': filters,
		'params': request.GET.urlencode(),
	})

def apply_filter(filters, groups, users=None, trusted=False):
	users = users or User.objects.all()
	if 'disabled' in filters and trusted:
		users = users.filter(is_active=False)
	elif 'all' not in filters or not trusted:
		users = users.filter(is_active=True)

	if 'non_staff' in filters:
		users = users.exclude(groups=settings.STAFF_GROUP_ID)

	if groups:
		to_include, to_exclude = [], []
		for g in groups.split(','):
			try:
				g = int(g)
			except ValueError: pass
			else:
				filters.append(g)
				if g >= 0:
					to_include.append(g)
				else:
					to_exclude.append(-g)

		if to_include:
			users = users.filter(groups__in=to_include)

		if to_exclude:
			users = users.exclude(groups__in=to_exclude)

	return users

@api_endpoint(public=True)
@ajax_required(redirect_url='users:list')
def ajax(request):
	return render_json(request, {
		'status': 'success',
		'users': [
			{
				'id': u.username,
				'name': u.profile.name,
				'title': u.profile.title,
				'avatar': u.profile.avatar,
			}
			for u in sorted_users(User.objects.filter(is_active=True, groups=11))
		],
	})

@login_required
def contacts(request):
	return render(request, 'users/contacts.html', {
		'users': sorted_users(User.objects.filter(is_active=True)),
		'authorized': request.user.profile.is_authorized(),
		'show_details': request.GET.get('details') and request.user.profile.is_trusted(),
	})

@login_required
def export(request, format=None):
	if format and format not in formats.keys():
		from django.http import Http404
		raise Http404

	filters = request.GET.getlist('find')
	groups = request.GET.get('g')
	authorized = request.user.profile.is_authorized()
	trusted = request.user.profile.is_trusted()
	users = apply_filter(filters=filters, groups=groups, trusted=trusted)

	users_output = []
	for user in sorted_users(users):
		entity = {
			'id': user.username,
			'name': user.profile.name,
			'title': user.profile.title,
			'avatar': user.profile.avatar,
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
			entity['residence'] = user.profile.residence
			entity['shirt_size'] = user.profile.shirt_size
			entity['diet'] = user.profile.diet
			entity['bio'] = user.profile.bio or None
			entity['comment'] = user.profile.comment
			entity['groups'] = ' '.join([str(g.id) for g in user.groups.all()])

		users_output.append(entity)

	content_type, template = formats[format or 'html']
	return render(request, template, { 'users': users_output }, content_type=content_type)
