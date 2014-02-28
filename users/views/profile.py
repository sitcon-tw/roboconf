from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from core.api.decorators import api_endpoint
from core.api.views import *

@api_endpoint(public=True)
def profile(request, username):
	user = get_object_or_404(User, username=username)
	if request.is_ajax():
		if user.is_active:
			return render_json(request, {
				'status': 'success', 
				'user': {
					'id': user.username, 
					'name': user.profile.name(),
					'title': user.profile.title,
					'avatar': user.profile.avatar(),
				}
			})
		return bad_request(request, {'status': 'invalid'})

	elif not request.user.is_authenticated():
		from django.contrib.auth.views import redirect_to_login
		return redirect_to_login(request.path)

	return render(request, 'users/profile.html', {
		'u': user,
	})
