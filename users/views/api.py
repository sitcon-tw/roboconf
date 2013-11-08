from api.utils import *
from users.utils import get_avatar_url
from django.contrib.auth.models import User

def api(request):
	if request.method == 'GET':
		return get(request)
	else:
		return not_allowed(request, ['GET'])

def get(request):
	name = request.GET.get('name')
	if name:
		try:
			user = User.objects.get(username=name)
			if user.is_active:
				return render(request, {
					'status': 'success',
					'name': user.username,
					'avatar': get_avatar_url(user.email),
					'title': user.profile.title,
				})
		except User.DoesNotExist: pass
		return bad_request(request, {'status': 'invalid'})
	else:
		result = {}
		for u in User.objects.filter(is_active=True, groups__id=11):
			result[u.username] = {
				"title": u.profile.title,
				"avatar": get_avatar_url(u.email),
			}
		return render(request, result)
