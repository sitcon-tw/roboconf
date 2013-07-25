from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from users.models import *

def profile(request, id):
	u = get_object_or_404(User, pk=id)
	return render(request, 'users_profile.html', {
		'u': u,
	})
