from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from users.utils import get_avatar_url

def profile(request, username):
	user = get_object_or_404(User, username=username)
	if request.is_ajax():
		from core.api import *
		if user.is_active:
			return render_json(request, {
				'status': 'success',
				'name': user.username,
				'avatar': get_avatar_url(user.email),
				'title': user.profile.title,
			})
		return bad_request(request, {'status': 'invalid'})

	elif not request.user.is_authenticated():
		from django.contrib.auth.views import redirect_to_login
		return redirect_to_login(request.path)

	return render(request, 'users/profile.html', {
		'u': user,
	})
