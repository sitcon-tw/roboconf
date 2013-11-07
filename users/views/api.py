from django.shortcuts import render
from django.contrib.auth.models import User
from core.api import route

USERS_API_PATTERN = (
	('get', get, ['name']),
)

def api(request):
	return route(request, USERS_API_PATTERN)

def get(name):
	try:
		user = User.objects.get(username=name)
	except User.DoesNotExist:
		user = None

	if not user or not user.is_active:
		return {'status': 'invalid'}

	from users.utils import get_avatar_url
	return {
		'status': 'success',
		'name': user.username,
		'avatar': get_avatar_url(user.email),
		'title': user.profile.title,
	}
