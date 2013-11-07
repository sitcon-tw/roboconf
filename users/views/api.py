from django.shortcuts import render
from django.contrib.auth.models import User
from core.api import route
from users.utils import get_avatar_url

def get(name):
	try:
		user = User.objects.get(username=name)
	except User.DoesNotExist:
		user = None

	if not user or not user.is_active:
		return {'status': 'invalid'}

	return {
		'status': 'success',
		'name': user.username,
		'avatar': get_avatar_url(user.email),
		'title': user.profile.title,
	}

def list():
	result = {}
	for u in User.objects.filter(is_active=True, groups__id=11):
		result[u.username] = {
			"title": u.profile.title,
			"avatar": get_avatar_url(u.email),
		}

USERS_API_PATTERN = (
	('get', get, ['name']),
	('list', list, []),
)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def api(request):
	return route(request, USERS_API_PATTERN)
